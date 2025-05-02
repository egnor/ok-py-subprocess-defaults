"""
Minor utilities and wrappers for the Python subprocess library
"""

import dataclasses
import logging
import os
import shutil
import subprocess

@dataclasses.dataclass
class SubprocessDefaults:
    args_prefix: list = dataclasses.field(default_factory=list)
    check: bool = True
    cwd: str = ""
    env: dict = dataclasses.field(default_factory=dict)
    log_level: int = logging.INFO  # use logging.NOTSET to disable

    def run(self, *args, **kw):
        """Wraps subprocess.run, applying the defaults in this object."""

        args = map(path_str, [*self.args_prefix, *args])

        kw = {
            "check": self.check,
            "cwd": _path_str(self.cwd) if self.cwd else None,
            "env": {
                **os.environ,
                **{ k: _path_str(v) for k, v in self.env.items() } },
            },
            **kw,
        }

        if self.log_level > logging.NOTSET:
            command_text = " ".join(shutil.quote(arg) for arg in args)
            logging.log(self.log_level, "🐚 %s", command_text)

        return subprocess.run(*args, **kw)

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
