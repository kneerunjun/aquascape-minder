#!/usr/bin/python3
# This module governs the minder service behaviour it has its position as indicated on the next outline
# minder.gov.py > minder.service > minder. upstart.py > minder. py
# incase the entire service needs to be taken down , or has to be restarted
# this would be running atop as a service again that can help us have a direct handle on the services underneath

from signalhandling import GracefulExit, Interruption
from edgebuttons import WaitingButtonFE
import threading, subprocess,time, sys
import RPi.GPIO as GPIO

CMD_IS_ACTIVE ="systemctl is-active minder.service"
CMD_STOP_SRV="sudo systemctl stop minder.service"
CMD_START_SRV="sudo systemctl start minder.service"
CMD_IS_ENABLED="systemctl is-enabled minder.service"
CMD_CPY_SRV="sudo cp ./minder.service /etc/systemd/system/minder.service"
CMD_ENABLE_SRV="sudo systemctl enable minder.service"

def restart_srv(gpiochn):
    '''This is where we go ahead to operate on status of ambientsense.service
    There are about 4 states of the ambientsense.service
    1       : active and running - restart in this case
    2       : inactive , stoppped  - start in this case
    3       : failed , exited - not sure what needs to be done in this case
    4       : disabled - enable it , start it
    '''
    if "active"==subprocess.getoutput(CMD_IS_ACTIVE):
        # this would mean the service is active and can be restarted
        subprocess.run(CMD_STOP_SRV.split())
        time.sleep(3.0)
        # subprocess.run(CMD_START_SRV.split())
    elif "inactive" ==subprocess.getoutput(CMD_IS_ACTIVE):
        # incase if its inactive we need to also find out if the service is disabled
        if "disabled" ==subprocess.getoutput(CMD_IS_ENABLED):
            # enable the service first
            subprocess.run(CMD_CPY_SRV.split())
            time.sleep(1.0)
            subprocess.run(CMD_ENABLE_SRV.split())
        # service has been enabled , all what you need is just start it
        subprocess.run(CMD_START_SRV.split())

if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)  # set board mode to Broadcom
        GPIO.setwarnings(False)
        gexit = GracefulExit()
        kllEvnt = threading.Event()
        edgbtn = WaitingButtonFE(chn=21,cb=restart_srv,termevnt=kllEvnt)
        edgbtn.start()
        edgbtn.join()
        print("Wait button no longer active , all tasks are closed")
        sys.exit(0)
    except Interruption as interr:
        print("ambientsense.restart.py : system signal for exit")
        kllEvnt.set()   # clearing off the button thread
        sys.exit(0)     # no need to  tamper with ambientsense.service
        # here we see that the governor service is just falling apart and that is ok
