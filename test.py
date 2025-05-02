import logging
import ok_subprocess_defaults

logging.basicConfig(level=logging.INFO)
sub = ok_subprocess_defaults.SubprocessDefaults()
sub.run("echo", "Hello World!")
