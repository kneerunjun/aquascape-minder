# this module represents the actual switch board accessed from various threads
# this enables to also turn the gpio on / off for requisite conditions
import RPi.GPIO as GPIO
from enum import Enum
from logger import TermLogger
import threading, time, json
import pdb
class SwitchModes(Enum):
    LED=1
    AIR=2
    FLT=4
    FDR=8
    HTR=16
class  SwitchBoard():
    '''This is the TSafe object where we get all the current status information
    '''
    def __init__(self,confg,*args, **kwargs):
        self._lck = threading.Lock()
        self._ledgpio  = confg.gpio()["led"]
        self._airgpio  = confg.gpio()["air"]
        self._fltgpio  = confg.gpio()["flt"]
        self._fdrgpio  = confg.gpio()["fdr"]
        self._htrgpio  = confg.gpio()["htr"]
        GPIO.setup([self._ledgpio,self._airgpio,self._fltgpio,self._fdrgpio,self._htrgpio], GPIO.OUT, initial=GPIO.LOW)
        self._temp = None
    def put(self,watertemp,*args,**kwargs):
        self._lck.acquire()
        self._temp  = watertemp
        self._lck.release()
    def temp(self):
        result  = None
        self._lck.acquire()
        result  = self._temp
        self._lck.release()
        return result
    def led(self):
        self._lck.acquire()
        result= GPIO.input(self._ledgpio)
        self._lck.release()
        return result
    def air(self):
        self._lck.acquire()
        result= GPIO.input(self._airgpio)
        self._lck.release()
        return result
    def flt(self):
        self._lck.acquire()
        result= GPIO.input(self._fltgpio)
        self._lck.release()
        return result
    def fdr(self):
        self._lck.acquire()
        result= GPIO.input(self._fdrgpio)
        self._lck.release()
        return result
    def htr(self):
        self._lck.acquire()
        result= GPIO.input(self._htrgpio)
        self._lck.release()
        return result
    def switch(self,switchmode):
        '''This basically would switches multiple devices with one value
        switch mode is ORed values of the switch modes sent from the client
        '''
        self._lck.acquire()
        if (switchmode & SwitchModes.LED.value) ==  SwitchModes.LED.value:
            if GPIO.input(self._ledgpio) ==0:
                GPIO.output(self._ledgpio, GPIO.HIGH)
        else:
            if GPIO.input(self._ledgpio) ==1:
                GPIO.output(self._ledgpio, GPIO.LOW)
        if (switchmode & SwitchModes.AIR.value) ==  SwitchModes.AIR.value:
            if GPIO.input(self._airgpio) ==0:
                GPIO.output(self._airgpio, GPIO.HIGH)
        else:
            if GPIO.input(self._airgpio) ==1:
                GPIO.output(self._airgpio, GPIO.LOW)
        if (switchmode & SwitchModes.FLT.value) ==  SwitchModes.FLT.value:
            if GPIO.input(self._fltgpio) ==0:
                GPIO.output(self._fltgpio, GPIO.HIGH)
        else:
            if GPIO.input(self._fltgpio) ==1:
                GPIO.output(self._fltgpio, GPIO.LOW)
        if (switchmode & SwitchModes.FDR.value) ==  SwitchModes.FDR.value:
            if GPIO.input(self._fdrgpio) ==0:
                GPIO.output(self._fdrgpio, GPIO.HIGH)
        else:
            if GPIO.input(self._fdrgpio) ==1:
                GPIO.output(self._fdrgpio, GPIO.LOW)
        if (switchmode & SwitchModes.HTR.value) ==  SwitchModes.HTR.value:
            if GPIO.input(self._htrgpio) ==0:
                GPIO.output(self._htrgpio, GPIO.HIGH)
        else:
            if GPIO.input(self._htrgpio) ==1:
                GPIO.output(self._htrgpio, GPIO.LOW)
        self._lck.release()
    def shutd(self):
        GPIO.output([self._ledgpio,self._airgpio,self._fltgpio,self._fdrgpio,self._htrgpio], GPIO.LOW)
