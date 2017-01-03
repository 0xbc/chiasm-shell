#!/usr/bin/env python
"""
Main class and method for chiasm shell.

:author: Ben Cheney
:license: MIT
"""
from __future__ import absolute_import

import logging

import chiasm_shell.config as config

l = logging.getLogger('chiasm_shell.chiasm_shell')

class ChiasmShell(object):
    """
    Utility class for kicking off the shell.
    """
    def run(self):
        """
        Creates the default backend and starts the loop.
        """
        backend = config.get_backends()[config.get_default_backend()]
        info_str = "Chiasm Shell - {}".format(config.__VERSION__)
        l.info(info_str)
        while True:
            l.debug("outer loop spinning up a new shell")
            l.info("Current arch is %s", backend.get_arch())
            backend.cmdloop()
            if backend.launch_module is not None:
                backend = backend.launch_module
            else:
                break

def main():
    """
    Public method for starting Chiasm Shell.
    """
    ChiasmShell().run()

if __name__ == '__main__':
    main()
