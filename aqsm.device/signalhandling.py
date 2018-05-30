# this was written to handle ssystem signals , and provide specialized interruption errors
# developer     : kneerunjun@gmail
# redesigned    : 30 MAY 2018 , India

import signal
class Interruption(Exception):
    pass
class GracefulExit():
    '''This helps in handling the system signals for the module and upon receving such signal would fire a custom Exception - which in turn signals any of program to quit and goto exception handling. In short it converts the system signal into a python interruption
    '''
    def __init__(self, *args, **kwargs):
        # setting up the signal masking and listeners.
        signal.signal(signal.SIGINT, self.upon_signal)
        signal.signal(signal.SIGTERM, self.upon_signal)
        signal.signal(signal.SIGHUP, self.upon_signal)
    def upon_signal(self, signum, frame):
        raise Interruption
