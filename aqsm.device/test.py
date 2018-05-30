#!/usr/bin/python3
from switch import SwitchBoard,SwitchModes
from config import TSafeSettings
from logger import TermLogger
import RPi.GPIO as GPIO
import threading, time, datetime
from schedules import Scheduler
from display import AqsmOLED
from signalhandling import GracefulExit , Interruption
from sensing import AqsmThermometer
def testswitchboard(l,swb):
    l.log("Switch baord test ..")
    swb.switch(SwitchModes.LED.value)
    time.sleep(3)
    swb.switch(SwitchModes.LED.value|SwitchModes.FLT.value)
    time.sleep(3)
    swb.switch(SwitchModes.AIR.value)
    time.sleep(10)
    swb.switch(SwitchModes.LED.value|SwitchModes.FLT.value|SwitchModes.AIR.value|SwitchModes.FDR.value|SwitchModes.HTR.value)
    time.sleep(10)
    swb.switch(0) # this ideally should shut down all the things
    l.log("Closing the switch board test ..")
def probe(l, swb):
    while True :
        print("led :{0} air :{1} flt :{2} fdr: {3} htr :{4}".format(swb.led(), swb.air(), swb.flt(), swb.fdr(), swb.htr()))
        print("{0:%H:%M:%S   %m/%d}".format(datetime.datetime.now()))
        time.sleep(2)
def blocker():
    while True :
        print("{0:%H:%M:%S   %m/%d}".format(datetime.datetime.now()))
        time.sleep(60.0)
def display(swb, ke):
    oled  = AqsmOLED(swb=swb)
    while not ke.wait(1.0):
        oled.display_status()
    oled.shutd()
    print("We are now exiting the display loop")
def temp(swb, ke):
    thermo = AqsmThermometer(swb=swb)
    while not ke.wait(5.0):
        thermo.measure()
    print("We are now exiting the temp loop")
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
    except Interruption as ie:
        ke.set()
        time.sleep(2.0)
        sched.shutd()
        swb.shutd()
        GPIO.cleanup()
        time.sleep(2.0)
