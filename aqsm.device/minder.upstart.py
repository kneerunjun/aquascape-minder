#!/usr/bin/python3
import signal,time,os, sys
from minder import GracefulExit,Interruption
from multiprocessing import Process
def start_minder():
    '''All what we are doing here is spawning the minder program
    '''
    os.system("/home/pi/src/aquascape-minder/aqsm.device/minder.py")
if __name__ == "__main__":
    try:
        gExit = GracefulExit()
        tasks = []
        task = Process(target=start_minder)
        task.start()
        print("We have the task started at {0}".format(task))
        tasks.append(task)
        for t in tasks:
            t.join()
        sys.exit(0)
    except Interruption as interr:
        os.kill(task.pid, signal.SIGINT)
        sys.exit(1)
