"""
Chiasm Shell backend and version configuration.

:author: Ben Cheney
:license: MIT
"""

BACKENDS = None

def get_backends():
    global BACKENDS
    if BACKENDS is None:
        # deferred import to avoid circular dependency hell
        from assembler import Assembler
        from disassembler import Disassembler
        BACKENDS = {
         'asm' : Assembler(),
         'disasm' : Disassembler()
        }
    return BACKENDS

def get_default_backend():
    return 'asm'

import os
__VERSION__ = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'VERSION')).read().strip()
