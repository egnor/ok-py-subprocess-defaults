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
- Checks command return (`check=True`) by default
- Uses explicit argument vectors (`shell=False`) by default
- Includes easy-peasy wrapper functions to capture stdout as text or lines
- Logs all commands run, escaped for cut-and-paste rerunning
- Lets you set defaults for `cwd` and `env` (merged with `os.environ`)
- Converts [Path-like](https://docs.python.org/3/library/pathlib.html) arguments to strings
- Passes through all `subprocess.run` keyword arguments

Collectively, this is what I want for subprocesses -- tweaks to `subprocess.run` (or actually `subprocess.check_call`) to make it super easy to [never](https://databio.org/posts/shell_scripts.html) [write](https://news.ycombinator.com/item?id=26682981) [shell](https://samgrayson.me/essays/stop-writing-shell-scripts/) [scripts](https://pythonspeed.com/articles/shell-scripts/) [again](https://dev.to/taikedz/your-bash-scripts-are-rubbish-use-another-language-5dh7). Your mileage will almost certainly vary!

# Usage

Add this package as a dependency:
- `pip install ok-subprocess-defaults`
- OR just copy the `ok_subprocess_defaults/` module (it has no dependencies)

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

`SubprocessDefaults` objects have properties that set defaults for `.run(...)`:
- `.args_prefix` (list of string or Path-like) - prepended to all commands run
- `.check` (bool) - default for `check` arg (default true)
- `.cwd` (string or Path-like) - default for `cwd` arg (default empty)
- `.env` (string dict) - merged with `os.environ` as default `env` arg
- `.log_level` (int) - level for command logging (default `logging.INFO`) 

## Capturing output

`SubprocessDefaults` objects have some utility wrappers to capture output:
- `.stdout_text(args, ...)` - returns captured stdout as a text string
- `.stdout_lines(args, ...)` - returns captured stdout split into lines

For more specific output capture or processing, keyword arguments passed to
`run` or any of the wrappers above are passed on to `subprocess.run`.
