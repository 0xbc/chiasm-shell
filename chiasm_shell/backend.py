"""
Backend superclass for assembler/disassembler - handles common functions.

:author: Ben Cheney
:license: MIT
"""
from __future__ import absolute_import

from cmd import Cmd
import logging

from chiasm_shell.config import get_backends

l = logging.getLogger('chiasm_shell.backend')

class Backend(Cmd):
    """
    Backend - common functions shared by both assembler and disassembler.
    """
    def __init__(self):
        """
        Create a new Backend instance.
        """
        Cmd.__init__(self)
        self._init_backend()
        self.launch_module = None

    def _init_backend(self):
        """
        _init_backend is responsible for setting the prompt
        """
        raise NotImplementedError("Backends need to implement _init_backend")

    def clear_state(self):
        """
        Optional interface to reset internal backend state.
        """
        pass

    def default(self, line):
        raise NotImplementedError("Backends need to implement default hanlders")

    def get_arch(self):
        """
        Optional interface to display the current architecture.
        """
        pass

    def do_quit(self, dummy_args):
        """
        Quits chiasm shell - return to system prompt.
        """
        raise SystemExit

    def do_exit(self, dummy_args):
        """
        Quits chiasm shell - return to system prompt.
        """
        raise SystemExit

    def cmdloop(self, intro=None):
        """
        Overridden cmdloop to catch CTRL-Cs
        """
        try:
            Cmd.cmdloop(self, intro)
        except KeyboardInterrupt:
            l.info("type \'quit\' or \'exit\' to exit")
            self.cmdloop()

    def do_switch(self, arg):
        """
        Switch to another chiasm backend (type lsbackends to see what's available).
        """
        if arg.strip() == '':
            l.error("usage: switch <backend>")
            return False
        backends = get_backends()
        if arg in backends:
            new_backend = backends[arg]
            new_backend.clear_state()
            self.launch_module = backends[arg]
            return True # True = quit this backend's loop
        else:
            l.error("backend %s not found", arg)
            self.launch_module = None

    def do_lsbackends(self, dummy_args):
        """
        List the chiasm backends currently available.
        """
        l.info(", ".join(get_backends().keys()))

    def postcmd(self, stop, line):
        """
        Just overridden for debugging purposes.
        """
        l.debug("i'm in postcmd, line is %s", line)
        return stop
