#!/usr/bin/python3
import time, pdb,json,sys, threading, logging, hardware, subprocess, signal
from collections import namedtuple
from queue import Queue
import cloudlink, schedules

logging.basicConfig(filename="aqsm.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
def error_log(message):
    pass
    print(message)
def config_from_json():
    return {
        "delays":{
            "interrupt":1,
            "downlinking":5,
            "uplinking":2,
            "sensing":2,
            "display":1
        }
    }
def check_configure(config):
    return True
class Interruption(Exception):
    pass
class GracefulExit():
    '''This helps in handling the system signals for the module and upon receving such signal would fire a custom Exception - which in turn signals any of program to quit and goto exception handling. In short it converts the system signal into a python interruption
    '''
    def __init__(self, *args, **kwargs):
        signal.signal(signal.SIGINT, self.upon_signal)
        signal.signal(signal.SIGTERM, self.upon_signal)
        signal.signal(signal.SIGHUP, self.upon_signal)
    def upon_signal(self, signum, frame):
        raise Interruption
# ref :https://stackoverflow.com/questions/419163/what-does-if-name-main-do#419185
def display_loop(sb, ke):
    disp = hardware.AqsmOLED()
    while not ke.wait(1):
        disp.display_status(sb)
    disp.shutd()
def temp_loop(sb, ke):
    tmtr = hardware.AqsmThermometer()
    while not ke.wait(10):
        tmtr.measure(sb)
if __name__ == "__main__":
    try:
        threaded_tasks =[] # for housing all the threaded tasks
        killEvent  = threading.Event()  # to signal all the threaded tasks to flush and shutdown
        gExit  = GracefulExit() # this handles the Ctrl +C and system signals and raises the exception here in the main thread - Interruption
        sb = hardware.SwitchBoard()         # this operates on all the moving parts, thread safe
        sched = schedules.Scheduler(sb)     # this sets up the calendar trigger, at crons in the day
        # subprocess.call(["./setsysdatefromweb.sh"])
        t_disp  = threading.Thread(target=display_loop, args=(sb,killEvent))
        threaded_tasks.append(t_disp)
        t_temp  = threading.Thread(target=temp_loop, args=(sb,killEvent))
        threaded_tasks.append(t_temp)
        t_disp.start()                      #displaying loop starts with this
        t_temp.start()                      # measuring the temp starts with this
        for t in threaded_tasks:
            t.join()
        # all the threads have returned, we can start shutdown sequence
        sched.shutd()
        sb.shutd()
        hardware.flush()
        sys.exit(0)
    except Interruption as interr:
        #incase of SIG interruption the code in the main thread would end up here
        print("System interruption, shutting down !")
        killEvent.set()
        sched.shutd()
        sb.shutd()
        hardware.flush()
        sys.exit(0)
