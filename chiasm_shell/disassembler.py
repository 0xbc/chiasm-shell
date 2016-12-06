"""
Handles disassembler functionality, powered by the Capstone engine.

:author: Ben Cheney
:license: MIT
"""

import capstone as cs
import logging
import re
import binascii

from backend import Backend

l = logging.getLogger('chiasm_shell.disassembler')

class Disassembler(Backend):
    """
    Disassembler - uses caspstone to print assembly from opcode input
    """
    def __init__(self):
        """
        Create a new Disassembler instance.
        """
        Backend.__init__(self)

    def _init_backend(self):
        """
        _init_backend is responsible for setting the prompt, custom init stuff.
        """
        self.prompt = 'disasm> '
        self._build_dicts()
    	self._arch = ('x86', '32')
        self._set_arch(*self._arch)
    	self._last_decoding = None

    def _build_dicts(self):
        """
        Build dicts of valid arch and known mode values.
        """
        regex_arch = re.compile(r'^CS_ARCH_\S+$')
        regex_mode = re.compile(r'^CS_MODE_\S+$')
        d = cs.__dict__
        self.valid_archs = {a: d[a] for a in d.keys()
                            if re.match(regex_arch, a) and cs.cs_support(d[a])}
        self.modes = {m: d[m] for m in d.keys() if re.match(regex_mode, m)}

    def clear_state(self):
        self._last_decoding = None

    def _set_arch(self, arch, *modes):
        """
        Try and set the current architecture
        """
        try:
            a = self.valid_archs[''.join(['CS_ARCH_', arch.upper()])]
            if a is None:
                l.error("Invalid architecture selected - run lsarch for valid options")
                return False
            ms = [self.modes[''.join(['CS_MODE_', m.upper()])] for m in modes]
        except KeyError:
            print l.error("ERROR: Invalid architecture or mode string specified")
            return False
        try:
            _cs = cs.Cs(a, sum(ms))
	        self._arch = (arch, modes)
            l.debug("Architecture set to {}, mode(s): {}".format(arch, ', '.join(modes)))
            self._cs = _cs
        except cs.CsError as e:
            l.error("ERROR: %s" %e)
            return False
        return True

    def get_arch(self):
	    return "{}, mode(s): {}".format(self._arch[0], ', '.join(self._arch[1]))

    def default(self, line):
        """
        Default behaviour - if no other commands are detected,
        try and disassemble the current input according to the
        currently set architecture and modes..

        :param line: Current line's text to try and disassemble.
        """
        try:
            self._last_decoding = []
            for (addr, size, mn, op_str) in self._cs.disasm_lite(line.decode('string_escape'), 0x1000):
	        self._last_decoding.append((addr, size, mn, op_str))
                l.info("0x{:x}:\t{}\t{}".format(addr, mn, op_str))
        except cs.CsError as e:
            l.error("ERROR: %s" %e)

    def do_lsarch(self, args):
        """
        Lists the architectures available in the installed version of keystone.
        """
        for a in self.valid_archs:
            print a[8:].lower()

    def do_setarch(self, args):
        """
        Set the current architecture.

        :param args: Lowercase string representing the requested architecture.
        """
        a = args.split()
        if len(a) < 2:
            print "Need to specify at least arch and one mode"
            return
        arch = a[0]
        modes = a[1:]
        if self._set_arch(arch, *modes) is True:
            l.info("Architecture set to {}, mode(s): {}".format(arch, ', '.join(modes)))

    def do_lsmodes(self, args):
        """
        Lists the known modes across all architectures. Note that not all modes apply to all architectures.
        """
        for a in sorted(self.modes):
            l.info(a[8:].lower())
