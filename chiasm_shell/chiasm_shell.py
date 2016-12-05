#!/usr/bin/env python
"""
Main class and method for chiasm shell.

:author: Ben Cheney
:license: MIT
"""
import logging

import config as c

l = logging.getLogger('chiasm_shell.chiasm_shell')

if __name__ == '__main__':
    backend = c.get_backends()[c.get_default_backend()]
    l.info("Chiasm Shell - {}".format(c.__VERSION__))
    while True:
	l.debug("outer loop spinning up a new shell")
	l.info("Current arch is {}".format(backend.get_arch()))
    	backend.cmdloop()
	if backend.launch_module is not None:
	    backend = backend.launch_module
	else:
	    break
