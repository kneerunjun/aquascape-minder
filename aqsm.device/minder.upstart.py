#!/usr/bin/python3
import signal,time,os, sys
from minder import GracefulExit,Interruption
from multiprocessing import Process
def start_minder():
    '''All what we are doing here is spawning the minder program
    This does not return till you have the actual minder.py return from sensing and scheduling
    '''
    os.system("/home/pi/src/aquascape-minder/aqsm.device/minder.py")
if __name__ == "__main__":
    try:
        gExit = GracefulExit()
        tasks = []
        task = Process(target=start_minder)
        task.start()
        tasks.append(task)
        for t in tasks:
            t.join()
        sys.exit(0)
    except Interruption as interr:
        # this is when we have an actual interruption on the service,
        # either when minder.upstart was Ctrl+C or the service was called off using systemctl
        # we call off minder.py too by sending a SIGINT signal and then exiting the system
        os.kill(task.pid, signal.SIGINT)
        sys.exit(1)
