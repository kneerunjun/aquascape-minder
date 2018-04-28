#!/usr/bin/python3
import signal,time,multiprocessing

class GracefulExit(Exception):
    def __init__(self,*args,**kwargs):
        super(GracefulExit, self).__init__(args, kwargs)

def signal_handler(signum, frame):
    raise GracefulExit()
def subprocess_function():
    try:
        sem = multiprocessing.Semaphore()
        print ("Acquiring semaphore")
        sem.acquire()
        print ("Semaphore acquired")
        print ("Blocking on semaphore - waiting for SIGTERM")
        sem.acquire()
    except GracefulExit:
        print ("Subprocess exiting gracefully")

if __name__ == "__main__":
    # Use signal handler to throw exception which can be caught to allow
    # graceful exit.
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    # Start a subprocess and wait for it to terminate.
    p = multiprocessing.Process(target=subprocess_function)
    p.start()
    print ("Subprocess pid: {0}".format( p.pid))
    p.join()
