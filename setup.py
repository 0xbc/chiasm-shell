"""
Chiasm Shell setup.

:author: Ben Cheney
:license: MIT
"""
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
            print("SandboxViolation (disabled): {}".format(args))

        DirectorySandbox._violation = violation
    except ImportError:
        pass

disable_sandbox()

setup(
    name='chiasm-shell',
    description='CLI for assembly/disassembly with Keystone/Capstone.',
    long_description=open('README.md').read(),
    version=open('chiasm_shell/VERSION').read().strip(),
    url='http://github.com/0xbc/chiasm-shell',
    author='Ben Cheney',
    author_email='ben.cheney@gmail.com',
    license='MIT',
    packages=['chiasm_shell'],
    install_requires=[
        'keystone-engine',
        'capstone'
    ],
    scripts=[
        'scripts/chiasm-shell'
    ],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'chiasm_shell = chiasm_shell:main',
        ]
    },
    classifiers=(
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Security',
    ),
)
