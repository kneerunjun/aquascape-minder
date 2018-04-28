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
            "sensing":2
        }
    }
def check_configure(config):
    return True
class SensingT(threading.Thread):
    '''Worker thread that does all the sensing on the device
    '''
    def __init__(self,ke,cfg):
        super(SensingT,self).__init__()
        self.killEvent  = ke
        self.config = cfg
    def run(self):
        while not self.killEvent.wait(1):
            print("Monitoring now..")
            time.sleep(self.config["delays"]["sensing"])
class InterruptT(threading.Thread):
    '''Worker thread that waits in anticipation of any hardware interrupt.
    Upon an interrupt this would trigger an event that in turn requests all threads to exit
    '''
    def __init__(self,ke,cfg):
        super(InterruptT,self).__init__()
        self.killEvent  = ke
        self.config = cfg
    def run(self):
        count = 10000
        while count !=0:
            count=count-1
            time.sleep(self.config["delays"]["interrupt"])
        print("We have an interrupt, perhaps an hardware interrupt")
        self.killEvent.set()        # this point where we ask all the other threads to exit
        return 0
class Interruption(Exception):
    pass
class GracefulExit():
    def __init__(self, *args, **kwargs):
        signal.signal(signal.SIGINT, self.upon_signal)
        signal.signal(signal.SIGTERM, self.upon_signal)
        signal.signal(signal.SIGHUP, self.upon_signal)
    def upon_signal(self, signum, frame):
        raise Interruption
# ref :https://stackoverflow.com/questions/419163/what-does-if-name-main-do#419185
if __name__ == "__main__":
    try:
        logging.info("aqsm.device.minder :Running Aquascape minder")
        # subprocess.call(["./setsysdatefromweb.sh"])
        config =config_from_json()              # loads the configuration from a json file
        hardware.init()
        killEvent  = threading.Event()
        gExit  = GracefulExit()
        sensing = SensingT(ke=killEvent,cfg=config)
        sensing.start()
        if schedules.sched !=None:
            schedules.sched.start()
        print("Running minder.py now!")
        sensing.join()
    except Interruption as interr:
        killEvent.set()
        schedules.sched.shutdown()
        hardware.flush()
        print("Exiting minder.py")
        sys.exit(1)
