#!/usr/bin/python3
import RPi.GPIO as GPIO
import cloudlink, threading, time
if __name__ == "__main__":
    print("Testing the cloud link module..")
    print("This module test involves setting up threaded tasks on uplinking and downlinking , that run simultenously and also check for the connectivity ")
    killEvent = threading.Event()
    uplinking = cloudlink.UplinkingT(killevent=killEvent,delay=1, url="http://google.co.in")
    uplinking.start()
    time.sleep(5)
    killEvent.set()
    uplinking.join()
