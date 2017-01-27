"""
Handles assembler functionality, powered by the Keystone engine.

:author: Ben Cheney
:license: MIT
"""
from __future__ import absolute_import

import logging
import re

from chiasm_shell.backend import Backend

l = logging.getLogger('chiasm_shell.assembler')

try:
    import keystone as ks
except ImportError as e:
    l.error("*** KEYSTONE IMPORT FAILURE ***")
    l.error("If you thought you'd already installed keystone-engine,")
    l.error("please ensure that you've got CMake and any other")
    l.error("Keystone dependencies installed on your system and")
    l.error("then try and build it/pip install it again.")
    l.error("Consult http://www.keystone-engine.org/docs/ for specifics.")
    raise e

class Assembler(Backend):
    """
    Assembler - uses keystone to print opcodes from assembly input
    """
    def __init__(self):
        """
        Create a new Assembler instance.
        """
        self._ks = None
        self._last_encoding = None
        self._arch = None
        self.mode = None
        self.modes = None
        self.valid_archs = None
        Backend.__init__(self)

    def _init_backend(self):
        """
        _init_backend is responsible for setting the prompt, custom init stuff.
        """
        self.prompt = 'asm> '
        self._build_dicts()
        self._arch = ('x86', '32')
        self._set_arch(*self._arch)
        self._last_encoding = None

    def _build_dicts(self):
        """
        Build dicts of valid arch and known mode values.
        """
        regex_arch = re.compile(r'^KS_ARCH_\S+$')
        regex_mode = re.compile(r'^KS_MODE_\S+$')
        d = ks.__dict__
        self.valid_archs = {a: d[a] for a in d.keys()
                            if re.match(regex_arch, a) and ks.ks_arch_supported(d[a])}
        self.modes = {m: d[m] for m in d.keys() if re.match(regex_mode, m)}

    def clear_state(self):
        self._last_encoding = None

    def _set_arch(self, arch, *modes):
        """
        Try and set the current architecture
        """
        try:
            a = self.valid_archs[''.join(['KS_ARCH_', arch.upper()])]
            if a is None:
                l.error("Invalid architecture selected - run lsarch for valid options")
                return False
            ms = [self.modes[''.join(['KS_MODE_', m.upper()])] for m in modes]
        except KeyError:
            l.error("ERROR: Invalid architecture or mode string specified")
            return False
        try:
            _ks = ks.Ks(a, sum(ms))
            self._arch = (arch, modes)
            l.debug("Architecture set to %s, mode(s): %s", arch, ', '.join(modes))
            self._ks = _ks
        except ks.KsError as e:
            l.error("ERROR: %s", e)
            return False
        return True

    def get_arch(self):
        return "{}, mode(s): {}".format(self._arch[0], ', '.join(self._arch[1]))

    def default(self, line):
        """
        Default behaviour - if no other commands are detected,
        try and assemble the current input according to the
        currently set architecture.

        :param line: Current line's text to try and assemble.
        """
        try:
            encoding, dummy_insn_count = self._ks.asm(line)
            self._last_encoding = encoding
            l.info("".join('\\x{:02x}'.format(opcode) for opcode in encoding))
        except ks.KsError as e:
            l.error("ERROR: %s", e)

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

    def do_count(self, dummy_args):
        """
        Prints the number of bytes emitted by the last successful encoding
        (or nothing if no successful encodings have occurred yet.)
        """
        if self._last_encoding is not None:
            l.info(len(self._last_encoding))
