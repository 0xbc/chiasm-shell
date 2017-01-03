"""
Handles disassembler functionality, powered by the Capstone engine.

:author: Ben Cheney
:license: MIT
"""
from __future__ import absolute_import

import logging
import re
import binascii
import capstone as cs

from chiasm_shell.backend import Backend

l = logging.getLogger('chiasm_shell.disassembler')

class Disassembler(Backend):
    """
    Disassembler - uses caspstone to print assembly from opcode input
    """
    def __init__(self):
        """
        Create a new Disassembler instance.
        """
        self._last_decoding = None
        self._cs = None
        self._firstaddr = None
        self._arch = None
        self.valid_archs = None
        self.modes = None
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
        self._firstaddr = 0x1000

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
            l.error("ERROR: Invalid architecture or mode string specified")
            return False
        try:
            _cs = cs.Cs(a, sum(ms))
            self._arch = (arch, modes)
            l.debug("Architecture set to %s, mode(s): %s", arch, ', '.join(modes))
            self._cs = _cs
        except cs.CsError as e:
            l.error("ERROR: %s", e)
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
        # quick, brittle hack to enforce backslash encoding for now
        regex = re.compile('^(\\\\x[a-fA-F0-9]{2})+$')
        if not regex.match(line.strip()):
            l.error("\\xXX\\xXX... is the only valid input format (XX = hex digits)")
            return

        try:
            self._last_decoding = []
            stripped_line = re.sub(r'\\x([0-9a-fA-F]+)', r'\1', line)
            for (addr, size, mn, op_str) in \
                    self._cs.disasm_lite(binascii.a2b_hex(stripped_line), self._firstaddr):
                self._last_decoding.append((addr, size, mn, op_str))
                disas_str = "0x{:x}:\t{}\t{}".format(addr, mn, op_str)
                l.info(disas_str)
        except cs.CsError as e:
            l.error("ERROR: %s", e)
        except ValueError:
            l.error("\\xXX\\xXX... is the only valid input format (XX = hex digits)")

    def do_lsarch(self, dummy_args):
        """
        Lists the architectures available in the installed version of keystone.
        """
        for a in self.valid_archs:
            l.info(a[8:].lower())

    def do_setarch(self, args):
        """
        Set the current architecture.

        :param args: Lowercase string representing the requested architecture.
        """
        a = args.split()
        if len(a) < 2:
            l.error("Need to specify at least arch and one mode")
            return
        arch = a[0]
        modes = a[1:]
        if self._set_arch(arch, *modes) is True:
            l.info("Architecture set to %s, mode(s): %s", arch, ', '.join(modes))

    def do_lsmodes(self, dummy_args):
        """
        Lists the known modes across all architectures.
        Note that not all modes apply to all architectures.
        """
        for a in sorted(self.modes):
            l.info(a[8:].lower())

    def do_setfirstaddr(self, args):
        """
        Sets the hex address of the first instruction in the buffer to be disassembled.
        """
        a = args.split()
        if len(a) < 1:
            return
        try:
            addr = int(a[0], 16)
            self._firstaddr = addr
        except ValueError:
            l.error("Input not recognised as a valid hex value - start address not changed")
