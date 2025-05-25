# ok-subprocess-defaults for Python

Trivial wrapper for [Python subprocess.run](https://docs.python.org/3/library/subprocess.html#subprocess.run) with defaults and logging.

You probably won't want to use this. Just call `subprocess.run` directly (it's perfectly lovely), write your own trivial helper, or use one of these libraries:
- [sh](https://github.com/amoffat/sh) - call any shell command as if it were a function
- [Plumbum](https://github.com/tomerfiliba/plumbum) - shell-like syntax for Python
- [zxpy](https://github.com/tusharsadhwani/zxpy) - `~` string operator to run shell commands
- [shellpy](https://github.com/lamerman/shellpy) - `\`` string operator to run shell commands
- [shell](https://github.com/toastdriven/shell) - another wrapper for subprocess
- [pipepy](https://github.com/kbairak/pipepy) - pipe operators and function wrappers for shell commands
- [python-shell](https://github.com/ATCode-space/python-shell) - another shell command runner

But, this is my wrapper, and it does these things:
- Lets you set defaults for `cwd` and `env` (added to `os.environ`)
- Checks command return (`check=True`) by default
- Uses explicit argument vectors (`shell=False`) by default
- Logs commands (with proper escaping) for transparency
- Includes easy-peasy wrapper functions to capture stdout as text or lines
- Converts [Path](https://docs.python.org/3/library/pathlib.html)-like
  arguments to strings
- Passes through all `subprocess.run` keyword arguments

Collectively, this is what I want for subprocesses -- tiny tweaks to `subprocess.run` (or actually `subprocess.check_call`) for one-liner brevity. Your mileage almost certainly will vary.

# Usage

Add this package as a dependency:
- `pip install ok-subprocess-defaults`
- OR just copy `ok_subprocess_defaults.py` (it has no dependencies)

Import the module, create an `ok_subprocess_defaults.SubprocessDefaults` object, and use it to run commands:
```python
import logging
import ok_subprocess_defaults
...
sub = ok_subprocess_defaults.SubprocessDefaults()
...
logging.basicConfig(level=logging.INFO)  # to show the logging
...
sub.run("echo", "Hello World!")
```
Note that command arguments are individual function arguments; otherwise, usage is the same as [subprocess.run](https://docs.python.org/3/library/subprocess.html#subprocess.run) including keyword arguments and return value.

The logging output looks like this:
```
$ python test.py
INFO:root:🐚 echo 'Hello World!'
Hello World!
```
Note that arguments are escaped so you can cut-and-paste the command.

## Configuring defaults

`SubprocessDefaults` objects have public properties to set defaults for
commands run through that object:
- `args_prefix` (list of string or Path-like) - prepended to all commands run
- `check` (bool) - default for subprocess `check` (default true)
- `cwd` (string or Path-like) - default for subprocess `cwd` (default empty)
- `env` (string dict) - merged with `os.environ` as default subprocess `env`
- `log_level` (int) - level for command logging (default `logging.INFO`) 

## Capturing output

`SubprocessDefaults` objects have some wrappers to the basic `.run` to
capture output in convenient ways:
- `.stdout_text(args, ...)` - returns captured stdout as a text string
- `.stdout_lines(args, ...)` - returns captured stdout split into lines

For more specific output capture or processing, keyword arguments passed to
`run` or any of the wrappers above are passed on to `subprocess.run`.
