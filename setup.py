try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def disable_sandbox():
    """
    When keystone is installed as a dependency, setuptools
    throws a SandboxViolation when it tries to create a
    directory for its shared library. Just disable the
    sandbox as a hacky workaround for now.
    """

    try:
        from setuptools.sandbox import DirectorySandbox
        def violation(operation, *args, **_):
            print "SandboxViolation (ignored): %s" % (args,)

        DirectorySandbox._violation = violation
    except ImportError:
        pass

disable_sandbox()

setup(name='chiasm-shell',
      version='0.1',
      url='http://github.com/0xbc/chiasm-shell',
      author='Ben Cheney',
      author_email='ben.cheney@gmail.com',
      license='MIT',
      packages=['chiasm-shell'],
      install_requires=[
          'keystone-engine',
      ],
      scripts=['scripts/chiasm-shell'],
      zip_safe=False)
