#!/usr/bin/python3
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import time, hardware
lcd_rs        = 21
lcd_en        = 20
lcd_d4        = 26
lcd_d5        = 19
lcd_d6        = 13
lcd_d7        = 6
lcd_backlight = None
if __name__ == "__main__":
    print ("Testing the hardware module with changes")
    hardware.init()
    while True:
        hardware.display()
        hardware.turn_on_airpump()
        time.sleep(2)
        hardware.turn_off_airpump()
    # print("We are testing the character lcd here")
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setwarnings(False)
    # GPIO.setup([lcd_rs,lcd_en,lcd_d4,lcd_d5,lcd_d6,lcd_d7], GPIO.OUT)
    # lcd = LCD.Adafruit_CharLCD(rs=lcd_rs, en=lcd_en, d4=lcd_d4, d5=lcd_d5, d6=lcd_d6, d7=lcd_d7, cols=16, lines=2)
    # while True:
    #     lcd.clear()
    #     lcd.home()
    #     lcl=time.localtime()
    #     lcd.message("{0}:{1}:{2}".format(lcl.tm_hour, lcl.tm_min, lcl.tm_sec))
    #     time.sleep(1)
    # GPIO.cleanup()
