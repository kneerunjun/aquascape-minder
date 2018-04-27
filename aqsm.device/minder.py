#!/usr/bin/python3
import time, pdb,json,sys, threading, logging, hardware, subprocess
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
def start_loops(config):
    '''Function to start all loops and also wait till all the loops are complete
    This returns 0 /1 back to the main function so that system level exit can be enabled
    config          : dictionary containing the configuration of the loops
    '''
    try:
        killEvent  = threading.Event()          # this helps halt all other worker threads
        # monitoring = SensingT(ke=killEvent,cfg=config)     # sensing thread
        # uplinking = cloudlink.UplinkingT(ke=killEvent,cfg=config)       # uploading to cloud thread
        # downlinking=cloudlink.DownlinkingT(ke=killEvent,cfg=config)     # downloading changes from the cloud
        interrupt  = InterruptT(ke=killEvent,cfg=config)      # this runs till there is an h/w interrupt
        # monitoring.start()
        # uplinking.start()
        # downlinking.start()
        interrupt.start()
        if schedules.sched !=None:
            schedules.sched.start()
        # joining all threads
        # monitoring.join()
        # uplinking.join()
        # downlinking.join()
        interrupt.join()
        # join the threaded loops here..
        print("Exiting looping sequence..")
        return 0                                # if exited with no issues you can return 0
    except Exception as e:
        print(str(e))
        error_log("failed to start tasks on the device")
        return 1                                # so that the main function knows it has error on exit
# ref :https://stackoverflow.com/questions/419163/what-does-if-name-main-do#419185
if __name__ == "__main__":
    logging.info("aqsm.device.minder :Running Aquascape minder")
    # subprocess.call(["./setsysdatefromweb.sh"])
    try:
        hardware.init()
        config =config_from_json()              # loads the configuration from a json file
        if(check_configure(config)==True):      # ascertaining if the configuration is correct
            ok =start_loops(config)
            hardware.flush()
            sys.exit(ok)       # we are to spin out all the tasks here
        else:
            error_log("Invalid configuration")  # config read , but invalid
            hardware.flush()
            sys.exit(1)
    except (KeyboardInterrupt, SystemExit):
        # this is when the user is trying to force stop the entire execution
        print("Exiting out from minder.py")
        hardware.flush()
        sys.exit(1)
    except Exception as e:
        print(str(e))
        hardware.flush()
        error_log("Failed to read any configuration")
