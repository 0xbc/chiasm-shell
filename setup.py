"""
Chiasm Shell setup.

:author: Ben Cheney
:license: MIT
"""
from __future__ import print_function, absolute_import
from setuptools import setup

def disable_sandbox():
    """
    When capstone/keystone is installed as a dependency, setuptools
    throws a SandboxViolation when it tries to create a
    directory for its shared library. Just disable the
    sandbox as a hacky workaround for now.

    nb.
    """

    try:
        from setuptools.sandbox import DirectorySandbox
        def violation(operation, *args, **_):
            """
            Print stup for DirectorySandbox violation function.
            """
            print("SandboxViolation (disabled): {} {}".format(operation, args))

        # pylint: disable=W0212
        DirectorySandbox._violation = violation
    except ImportError:
        pass

disable_sandbox()

setup(
    name='chiasm-shell',
    description='CLI for assembly/disassembly powered by Keystone/Capstone.',
    long_description=open('README.md').read(),
    version=open('chiasm_shell/VERSION').read().strip(),
    url='https://github.com/0xbc/chiasm-shell',
    download_url='https://github.com/0xbc/chiasm-shell/tarball/1.0.0a1',
    author='Ben Cheney',
    author_email='ben.cheney@gmail.com',
    license='MIT',
    packages=['chiasm_shell'],
    package_data={'chiasm_shell': ['chiasm_shell/VERSION']},
    include_package_data=True,
    install_requires=[
        'keystone-engine',
        'capstone'
    ],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'chiasm-shell = chiasm_shell.chiasm_shell:main',
        ]
    },
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Security',
        'Topic :: Software Development :: Assemblers',
        'Topic :: Software Development :: Dissasemblers',
    ),
    keywords = ['disassembler', 'assembler'],
)
