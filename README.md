# chiasm-shell
====

[![Latest Release](https://img.shields.io/pypi/v/chiasm-shell.svg)](https://pypi.python.org/pypi/chiasm-shell)

Python-based interactive assembler/disassembler CLI, powered by [Keystone]/[Capstone].

## Why did you make this?
I wanted to quickly view some opcodes with [metasm-shell.rb], but I didn't have a Metasploit install handy. I didn't really want to mess around with Ruby either, so I figured that writing my own replacement was a good excuse to play with Keystone and Capstone.

## How do I install it?
```bash
pip install chiasm-shell
# OR
mkvirtualenv chiasm-shell # optional
git clone https://github.com/0xbc/chiasm-shell
cd chiasm-shell
python setup.py install # assumes you have Capstone and Keystone 
                        # build toolchains installed, which includes CMake.
```

## How do I run it?
```bash
chiasm-shell
# or, from the repo base directory:
python -m chiasm_shell.chiasm_shell
```

## How do I use it?
- When the prompt is `asm>`, you're using the interactive assembler backend (Keystone).
  - Input one or more assembly statements separated by a semi-colon. x86 uses Intel syntax only at the moment.
- When the prompt is `disasm>`, you're using the interactive disassembler backend (Capstone).
  - Input one or more bytes represented by \xXX, where XX is a hex value.
- To switch backends, use `switch asm` or `switch disasm`.
- To change architecture, use `setarch <arch> <mode(s)>`.
  - e.g. `setarch x86 64`.
  - You can use more than one mode, separated by spaces.
  - Use `lsarch` and `lsmode` to view supported architectures and modes for the current backend
  - At the moment, you need to know what modes are relevant to each architecture - check the Keystone/Capstone source if you're not sure.
- Type `help` to see a list of commands; `help <cmd>` to see the docstring for `cmd`.

## Example usages
```
asm> inc eax; xor ebx, ebx
\x40\x31\xdb
```

```
disasm> \x40\x31\xdb
0x1000: inc     eax
0x1001: xor     ebx, ebx
```

## It's broken/I have a suggestion/etc.
Please get in touch/raise an issue/PR/etc!

## Known Issues
- None at this time.

## TODO
- Syntax highlighting and/or tab completion for assembly
- Intelligent mode selection
- Support different input/output formats
- Test suite

[keystone]: <http://www.keystone-engine.org/>
[capstone]: <http://www.capstone-engine.org/>
[metasm-shell.rb]: <https://github.com/jjyg/metasm/blob/master/samples/metasm-shell.rb>
