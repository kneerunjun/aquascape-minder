#!/usr/bin/python3
# This helps to configure the program output to either the screen or an actual file , depending on the object chosen to send the messages
# developer     : kneerunjun@gmail
# redesigned    : 30 MAY 2018 , India

import threading
class TermLogger():
    '''Works as a thread safe terminal logger, able to print simple messages on the command line
    '''
    def __init__(self):
        self._lck  = threading.Lock()
    def log(self, message):
        self._lck.acquire()
        print(message)
        self._lck.release()
    def shutd(self):
        pass
