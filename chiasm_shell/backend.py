"""
Backend superclass for assembler/disassembler - handles common functions.

:author: Ben Cheney
:license: MIT
"""

from cmd import Cmd
import logging

from config import get_backends

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
        raise NotImplementedError, "Backends need to implement _init_backend"

    def default(self, line):
        raise NotImplementedError, "Backends need to implement default hanlders"

    def get_arch(self):
	pass

#    def do_help(self, arg):
#        if arg == 'quit' or arg == 'exit':
#            l.info("closes chiasm-shell")
#        else:
#            Cmd.do_help(self, arg)

    def do_quit(self, args):
        """
        Quits chiasm shell - return to system prompt.
        """
        raise SystemExit

    def do_exit(self, args):
        """
        Quits chiasm shell - return to system prompt.
        """
        raise SystemExit

    def cmdloop(self):
        try:
            Cmd.cmdloop(self)
        except KeyboardInterrupt as e:
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
        if backends.has_key(arg):
            self.launch_module = backends[arg]
	    return True # True = quit this backend's loop
        else:
            l.error("backend {} not found".format(arg))
	    self.launch_module = None
    
    def do_lsbackends(self, arg):
        """
        List the chiasm backends currently available.
        """
        l.info(", ".join(get_backends().keys()))
		
    def postcmd(self, stop, line):
	l.debug("i'm in postcmd, line is {}".format(line))
	return stop
