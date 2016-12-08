# chiasm-shell
Python-based interactive assembler/disassembler CLI, powered by [Keystone]/[Capstone].

- Architecture support for assembly/disassembly is defined by what you've built into your local Keystone/Capstone install.

## Why did you make this?
I wanted to quickly view some opcodes with [metasm-shell.rb], but I didn't have a Metasploit install handy. I didn't really want to mess around with Ruby either, so I figured that writing my own replacement was a good excuse to play with Keystone and Capstone.

## How do I install it?
```sh
mkvirtualenv chiasm-shell # optional
git clone https://github.com/0xbc/chiasm-shell
cd chiasm-shell
python setup.py install # assumes you have Capstone and Keystone build toolchains installed
```

## How do I run it?
```sh
chiasm-shell
# or, from the repo base directory:
python -m chiasm_shell.chiasm_shell
```

## How do I use it?

[keystone]: <http://www.keystone-engine.org/>
[capstone]: <http://www.capstone-engine.org/>
[metasm-shell.rb]: <https://github.com/jjyg/metasm/blob/master/samples/metasm-shell.rb>
