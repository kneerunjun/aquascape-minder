#!/usr/bin/python3
import RPi.GPIO as GPIO
import cloudlink, threading, time, hardware, schedules
def task_2(sb):
    disp = hardware.AqsmOLED()
    while True :
        disp.display_status(sb)
        time.sleep(1)
if __name__ == "__main__":
    sb = hardware.SwitchBoard()
    sched = schedules.Scheduler(sb)
    t2  = threading.Thread(target=task_2, args=(sb,))
    t2.start()
    t2.join()
