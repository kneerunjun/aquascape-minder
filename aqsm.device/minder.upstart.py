#!/usr/bin/python3
import signal,time,os, sys, threading
from signalhandling import GracefulExit,Interruption
from multiprocessing import Process
def start_minder():
    os.system("/home/pi/src/aquascape-minder/aqsm.device/minder.py")

if __name__ == "__main__":
    try:
        gExit = GracefulExit()
        startMinderProc = Process(target=start_minder)
        startMinderProc.start()
        startMinderProc.join()
        sys.exit(0)
    except Interruption as interr:
        # this is when we have an actual interruption on the service,
        # either when minder.upstart was Ctrl+C or the service was called off using systemctl
        # we call off minder.py too by sending a SIGINT signal and then exiting the system
        os.kill(startMinderProc.pid, signal.SIGINT)
        sys.exit(1)
