#!/usr/bin/env python

from keystone import *

from cmd import Cmd
import re

class ChiasmShell(Cmd):
    """
    ChiasmShell main class - uses Cmd to provide a basic prompt.
    """
    def __init__(self):
        """
        Create a new ChiasmShell instance.
        """
        Cmd.__init__(self)
        self._build_dicts()
        # defaults to X86, 32-bit
        # TODO: make this configurable
        self._set_arch('x86', '32')

    def _build_dicts(self):
        """
        Build dicts of valid arch and known mode values.
        """
        regex_arch = re.compile(r'^KS_ARCH_\S+$')
        regex_mode = re.compile(r'^KS_MODE_\S+$')
        g = globals()
        self.valid_archs = {a: g[a] for a in g.keys()
                            if re.match(regex_arch, a) and ks_arch_supported(g[a])}
        self.modes = {m: g[m] for m in g.keys() if re.match(regex_mode, m)}

    def _set_arch(self, arch, *modes):
        """
        Try and set the current architecture
        """
        try:
            a = self.valid_archs[''.join(['KS_ARCH_', arch.upper()])]
            if a is None:
                print "Invalid architecture selected - run lsarch for valid options"
                return
            ms = [self.modes[''.join(['KS_MODE_', m.upper()])] for m in modes]
        except KeyError:
            print "ERROR: Invalid architecture or mode string specified"
            return
        try:
            ks = Ks(a, sum(ms))
            self.ks = ks
        except KsError as e:
            print "ERROR: %s" %e

    def default(self, line):
        """
        Default behaviour - if no other commands are detected,
        try and assemble the current input according to the
        currently set architecture.

        :param line: Current line's text to try and assemble.
        """
        try:
            # Initialize engine in X86-32bit mode
            encoding, count = self.ks.asm(line)
            print "".join('\\x{:02x}'.format(opcode) for opcode in encoding)
        except KsError as e:
            print "ERROR: %s" %e

    def do_lsarch(self, args):
        """
        Lists the architectures available in the installed version of keystone
        """
        for a in self.valid_archs:
            print a[8:].lower()

    def do_setarch(self, args):
        """
        Set the current architecture.

        :param args: Lowercase string representing
        """
        a = args.split()
        if len(a) < 2:
            print "Need to specify at least arch and one mode"
            return
        arch = a[0]
        modes = a[1:]
        self._set_arch(arch, *modes)

    def do_lsmodes(self, args):
        """
        Lists the known modes across all archs
        """
        for a in sorted(self.modes):
            print a[8:].lower()

    def do_help(self, arg):
        if arg == 'quit' or arg == 'exit':
            print "closes chiasm-shell"
        elif arg == 'lsarch':
            print "lists the available architectures"
        elif arg == 'setarch':
            print "sets the current architecture (format: arch mode(s), all separated by spaces)"
        elif arg == 'lsmodes':
            print "lists the available modes (warning - not all apply to every arch)"
        else:
            Cmd.do_help(self, arg)

    def cmdloop(self):
        try:
            Cmd.cmdloop(self)
        except KeyboardInterrupt as e:
            print "type \'quit\' or \'exit\' to exit"
            self.cmdloop()

    def do_quit(self, args):
        raise SystemExit

    def do_exit(self, args):
        raise SystemExit

if __name__ == '__main__':
    shell = ChiasmShell()
    shell.prompt = 'chiasm> '
    shell.cmdloop()
