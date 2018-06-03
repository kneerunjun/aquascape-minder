
import RPi.GPIO as GPIO
import time, threading, sys

class WaitingButtonFE(threading.Thread):
    '''A threaded tasks that expects a button or some lowering signal on the chn GPIO to set a threading event. This runs on a separate thread and returns when the button is pressed.
    Its a simple thread that runs a task till a button press, returns when button is pressed
    '''
    def __init__(self,chn,cb,termevnt,*args, **kwargs):
        '''
        evnt        :Threading event which signifies the sought event has occured
        chn         :channel on which the GPIO needs to be set
        '''
        super(WaitingButtonFE, self).__init__()
        self._chn = chn         #GPIO channel to watch on
        self._te  = termevnt    #keep waiting on this event
        GPIO.setup(self._chn,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self._chn, GPIO.FALLING, callback=cb,bouncetime=500)
        # callback is the function to callback when the event is detected
    def run(self):
        while not self._te.wait(1) :
            continue
        GPIO.remove_event_detect(self._chn)
        return
def callbck(chn):
    print("We have the callback on the channel {0}".format(chn))
