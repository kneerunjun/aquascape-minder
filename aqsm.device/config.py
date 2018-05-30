
import threading, json, pdb
from switch import SwitchModes
class TSafeSettings():
    def __init__(self, *args, **kwargs):
        self._lck = threading.Lock()    #settings also has to be tsafe
        self._file ="/home/pi/src/aquascape-minder/aqsm.device/config.json"
    def gpio(self):
        '''This tries to get the gpio pin settings for each of the device
        alternatively this would help us define the pins for all the hardware components here in a single settings file which can be changed remotely too and can be read into anew everytime the program starts
        '''
        try:
            self._lck.acquire()
            with open(self._file) as settfile :
                gpiosettings = json.load(settfile)["gpio"]
            self._lck.release()
            return gpiosettings
        except FileNotFoundError as fe:
            self._lck.release()
            print("failed to get the settings file")
            raise fe
    def schedules(self,id):
        '''This tries to get the gpio pin settings for each of the device
        alternatively this would help us define the pins for all the hardware components here in a single settings file which can be changed remotely too and can be read into anew everytime the program starts
        '''
        try:
            self._lck.acquire()
            with open(self._file) as settfile :
                schedules = json.load(settfile)["schedules"]
                hours = schedules["{0}".format(id)]["hours"]
                minutes = schedules["{0}".format(id)]["minutes"]
            self._lck.release()
            return (hours, minutes)
        except FileNotFoundError as fe:
            self._lck.release()
            print("failed to get the settings file")
            raise fe
    def switches(self, id):
        try:
            self._lck.acquire()
            switch = 0
            with open(self._file) as settfile :
                schedules = json.load(settfile)["schedules"]
                if schedules["{0}".format(id)]["led"]==1:
                    switch  = switch | SwitchModes.LED.value
                if schedules["{0}".format(id)]["air"]==1:
                    switch  = switch | SwitchModes.AIR.value
                if schedules["{0}".format(id)]["flt"]==1:
                    switch  = switch | SwitchModes.FLT.value
                if schedules["{0}".format(id)]["fdr"]==1:
                    switch  = switch | SwitchModes.FDR.value
            self._lck.release()
            return switch
        except FileNotFoundError as fe:
            self._lck.release()
            print("failed to get the settings file")
            raise fe
