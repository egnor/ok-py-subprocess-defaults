"""
Minor utilities and wrappers for the Python subprocess library
"""

import contextlib
import dataclasses
import logging
import os
import shutil
import subprocess

@dataclasses.dataclass
class _SubprocessDefaults:
    args_prefix: list = dataclasses.field(default_factory=list)
    cwd: str = ""
    env: dict = dataclasses.field(default_factory=dict)
    log_level: int = logging.INFO

_global_defaults = _SubprocessDefaults()


def run(*args, **kw):
    """Wraps subprocess.run, with some differences:

    - uses defaults established in os_subprocess_util.update_defaults
    - defaults check=True (pass check=False to override)
    - logs the command (call update_defaults(log_level=NOTSET) to disable)
    """

    args = [*_global_defaults.args_prefix, *map(_check_str, args)]
    kw = {
        "check": True,
        "cwd": _global_defaults.cwd or None,
        "env": { **os.environ, **_global_defaults.env },
        **kw,
    }

    if _global_defaults.log_level > logging.NOTSET:
        command_text = " ".join(shutil.quote(arg) for arg in args)
        logging.log(_global_defaults.log_level, "🐚 %s", command_text)

    return subprocess.run(*args, **kw)


def stdout_text(*args, **kw):
    """Similar to run, but captures and returns stdout text."""

    return run(*args, {stdout: subprocess.PIPE, text: True, **kw}).stdout


def stdout_lines(*args, **kw):
    """Similar to stdout_text, but splits the text into lines."""

    return stdout_text(*args, **kw).splitlines()


@contextlib.contextmanager
def update_defaults(*, cwd=None, env=None, log_level=None, args_prefix=None):
    """Updates global defaults for run and friends.
    Returns a context manager that restores old defaults when exited
    (just ignore the return value if restoration isn't needed).

    :param cwd: str or PathLike, default working directory
    :param env: str-str dict, variables to set in the default environment
    :param log_level: int, the logging level to use (default logging.INFO)
    :param args_prefix: list of str, prefix to add to all commands

    All parameters may be None to leave the corresponding default unchanged.
    """

    old_defaults = _global_defaults
    _global_defaults = dataclasses.replace(_global_defaults)
    if args_prefix is not None:
        _global_defaults.args_prefix = [*map(_check_str, args_prefix)]
    if cwd is not None:
        _global_defaults.cwd = _check_str(cwd)
    if log_level is not None:
        _global_defaults.log_level = log_level
    if env:
        _global_defaults.env = global_defaults.env.copy()
        for k, v in env.items():
            if v is not None:
                _global_defaults.env[_check_str(k)] = _check_str(v)
            else:
                _global_defaults.env.pop(k, None)

    yield None

    _global_defaults = old_defaults


def _check_str(value):
    if isinstance(value, os.PathLike):
        return value.__fspath__()
    if isinstance(value, str):
        return value
    raise TypeError(f"Expected str or PathLike, got {value!r}")
