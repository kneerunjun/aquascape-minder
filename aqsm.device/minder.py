#!/usr/bin/python3
# This is the main program that would be started when the service starts
# This would call out the concocction of all the objects and kick start the processes
# This also handles the cleanup of all the obejcts isafely when the program is about to terminate
# developer     : kneerunjun@gmail
# redesigned    : 30 MAY 2018 , India
# This is the successor to the program that was written , but found with some performance issues

from switch import SwitchBoard,SwitchModes
from config import TSafeSettings
from logger import TermLogger
import RPi.GPIO as GPIO
import threading, time, datetime, sys
from schedules import Scheduler
from display import AqsmOLED
from signalhandling import GracefulExit , Interruption
from sensing import AqsmThermometer

GPIO_RESPONSE_DELAY=2.0

def display(swb, ke):
    oled  = AqsmOLED(swb=swb)
    while not ke.wait(1.0):
        oled.display_status()
    oled.shutd()
def temp(swb, ke):
    thermo = AqsmThermometer(swb=swb)
    while not ke.wait(5.0):
        thermo.measure()
if __name__ == "__main__":
    if __name__ == "__main__":
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        try:
            gExit = GracefulExit()
            l = TermLogger()
            ke = threading.Event()
            config = TSafeSettings()
            swb = SwitchBoard(confg =config)
            sched  = Scheduler(swb=swb,confg =config)
            threads = []
            t = threading.Thread(target =display, args=(swb,ke))
            threads.append(t)
            t = threading.Thread(target =temp, args=(swb,ke))
            threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            GPIO.cleanup()
            time.sleep(GPIO_RESPONSE_DELAY)
            sys.exit(0)
        except Interruption as ie:
            ke.set()
            time.sleep(GPIO_RESPONSE_DELAY)
            sched.shutd()
            swb.shutd()
            GPIO.cleanup()
            sys.exit(0)
