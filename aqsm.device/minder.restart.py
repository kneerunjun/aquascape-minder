#!/usr/bin/python3
import os, time, threading
from edgedetect import WaitOnFallingEdgeT
from minder import GracefulExit,Interruption

DEBOUNCE_MS = 10000 # any successive fallen edge signals within 4000 ms are all neglected
LAST_RESTART = 0
def restart_service(channel):
    global LAST_RESTART
    justnow = int(round(time.time() * 1000))
    if justnow-LAST_RESTART > DEBOUNCE_MS:
        os.system("sudo systemctl stop minder.service")
        time.sleep(6)
        os.system("sudo systemctl start minder.service")            #this may also trigger some restart since it involves GPIO cleanup
        LAST_RESTART=int(round(time.time() * 1000))
if __name__ == "__main__":
    try:
        gExit = GracefulExit()
        edgeWaitKill  = threading.Event()
        edgeWait  = WaitOnFallingEdgeT(chn=12,cb=restart_service,termevnt=edgeWaitKill)
        edgeWait.start()
        edgeWait.join()
    except Interruption as interr:
        edgeWaitKill.set()
