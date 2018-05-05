#!/usr/bin/python3
import RPi.GPIO as GPIO
import time, threading, sys

def upon_edge_detect(channel):
    print("We have an edge case detection on channel :{0}".format(channel))
class WaitOnFallingEdgeT(threading.Thread):
    '''A threaded tasks that expects a button or some lowering signal on the chn GPIO to set a threading event. This runs on a separate thread and returns when the button is pressed.
    Its a simple thread that runs a task till a button press, returns when button is pressed
    '''
    def __init__(self,chn,cb,termevnt,*args, **kwargs):
        '''
        evnt        :Threading event which signifies the sought event has occured
        chn         :channel on which the GPIO needs to be set
        '''
        super(WaitOnFallingEdgeT, self).__init__()
        self.chn = chn
        self.terminateEvent  = termevnt
        GPIO.setup(chn,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(chn, GPIO.FALLING, callback=cb)
    def run(self):
        while not self.terminateEvent.wait(1) :
            time.sleep(1) # this thread does hardly anything, just sleeps waiting for edge to lower
    def upon_falling(self, channel):
        print("WaitOnFallingEdgeT: Edge detected on port {0}".format(self.chn))
class WaitOnRisingEdgeT(threading.Thread):
    '''A threaded tasks that expects a button or some up signal on the chn GPIO to set a threading event. This runs on a separate thread and returns when the button is pressed.
    '''
    def __init__(self,chn,cb,termevnt,*args, **kwargs):
        '''
        evnt        :Threading event which signifies the sought event has occured
        chn         :channel on which the GPIO needs to be set
        '''
        super(WaitOnRisingEdgeT, self).__init__()
        self.chn = chn
        self.terminateEvent  = termevnt
        GPIO.setup(chn,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(chn, GPIO.RISING, callback=cb)
    def run(self):
        while not self.terminateEvent.wait(1) :
            time.sleep(1) # this thread does hardly anything, just sleeps waiting for edge to higher
    def upon_rising(self, channel):
        print("WaitOnRisingEdgeT: Edge detected on port {0}".format(self.chn))

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    edgeFallen = threading.Event()
    # waitforedge  =WaitOnFallingEdgeT(chn=12, evnt=edgeFallen)
    # waitforedge.start()
    # waitforedge.join()
    waitforedge  =WaitOnRisingEdgeT(chn=12, evnt=edgeFallen)
    waitforedge.start()
    waitforedge.join()
    sys.exit(0)
