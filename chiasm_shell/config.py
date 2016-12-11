"""
Chiasm Shell backend and version configuration.

:author: Ben Cheney
:license: MIT
"""
from __future__ import absolute_import
import os

BACKENDS = None

def get_backends():
    """
    Returns a list of the available backends.
    """
    global BACKENDS
    if BACKENDS is None:
        # deferred import to avoid circular dependency hell
        from chiasm_shell.assembler import Assembler
        from chiasm_shell.disassembler import Disassembler
        BACKENDS = {
            'asm' : Assembler(),
            'disasm' : Disassembler()
        }
    return BACKENDS

def get_default_backend():
    """
    Returns the backend instantiated by default by the ChiasmShell class.
    """
    return 'asm'

__VERSION__ = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'VERSION')).read().strip()
