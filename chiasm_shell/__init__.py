"""
Global data for chiasm_shell module..

:author: Ben Cheney
:license: MIT
"""
# logging setup - do something fancy here later on, colours etc
import logging
#import config as c

logging.basicConfig(format='%(message)s',level=logging.INFO)

#l = logging.getLogger('chiasm_shell')

#class ChiasmShell(object):
#    def run(self):
#        backend = c.get_backends()[c.get_default_backend()]
#        l.info("Chiasm Shell - {}".format(c.__VERSION__))
#        while True:
#    	    l.debug("outer loop spinning up a new shell")
#    	    l.info("Current arch is {}".format(backend.get_arch()))
#            backend.cmdloop()
#    	    if backend.launch_module is not None:
#    	        backend = backend.launch_module
#    	    else:
#    	        break
#    
#if __name__ == '__main__':
#    ChiasmShell().start()
