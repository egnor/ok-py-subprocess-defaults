"""
Minor utilities and wrappers for the Python subprocess library
"""

import dataclasses
import logging
import os
import shlex
import subprocess

@dataclasses.dataclass
class SubprocessDefaults:
    """Default values for subprocess.run, plus some convenience methods."""

    args_prefix: list = dataclasses.field(default_factory=list)
    """Arguments (including command) to prepend to args for run methods."""

    check: bool = True
    """Default subprocess.run setting, True to raise on non-zero exit codes."""

    cwd: str = ""
    """Default directory for subprocess."""

    env: dict = dataclasses.field(default_factory=dict)
    """Default environment variables **added** to os.environ for subprocess."""

    log_level: int = logging.INFO
    """Logging level to print commands, or logging.NOTSET to disable."""

    def run(self, *args, **kw):
        """Wraps subprocess.run (with args directly listed), logging the
        command (per log_level) and applying defaults from this object."""

        args = [_path_str(a) for a in [*self.args_prefix, *args]]

        kw = {
            "check": self.check,
            "cwd": _path_str(self.cwd) if self.cwd else None,
            "env": {
                **os.environ,
                **{ k: _path_str(v) for k, v in self.env.items() },
            },
            **kw,
        }

        if self.log_level and self.log_level > logging.NOTSET:
            command_text = " ".join(shlex.quote(arg) for arg in args)
            logging.log(self.log_level, "🐚 %s", command_text)

        return subprocess.run(args, **kw)

    def stdout_text(self, *args, **kw):
        """Like run, but captures and directly returns stdout text."""

        kw = { "stdout": subprocess.PIPE, "text": True, **kw }
        return self.run(*args, **kw).stdout

    def stdout_lines(self, *args, **kw):
        """Like stdout_text, but splits the text into lines."""

        return self.stdout_text(*args, **kw).splitlines()

    def copy(self):
        """Returns a copy of this object with the same defaults."""

        return dataclasses.replace(
            self, args_prefix=self.args_prefix.copy(), env=self.env.copy()
        )


def _path_str(path_or_str):
    if isinstance(path_or_str, str):
        return path_or_str
    if isinstance(path_or_str, os.PathLike):
        return str(path_or_str)
    raise TypeError(
        f"Expected str or os.PathLike, got {path_or_str!r}"
    )
