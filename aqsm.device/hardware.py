import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import pdb, datetime
# All the gpio identifications  on the BCM based numbering
# you would want to try out gpio readall - to know more on the BCM based numbering
LEDGPIO=17          #physical pin 11
AIRGPIO=27          #physical = 13
FLTGPIO=22          #physical = 15
FEEDGPIO=23         #physical = 16
# configuaration for the  6 LCD pins
LCD_RS = 21         # phsical = 40
# 39 is GND  - cannot use that for the gpio purpose
LCD_EN = 20         # physical= 38
LCD_D4 = 26         # physical= 37
LCD_D5 = 19         # physical= 35
LCD_D6 = 13         # physical= 33
LCD_D7 = 6          # physical= 31
lcd = None          # global lcd handle, can be used after the init call
def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    global lcd              #is  a module level variable that we are accessing , so keyword global
    relaychannels = [LEDGPIO,AIRGPIO,FLTGPIO,FEEDGPIO]
    GPIO.setup(relaychannels, GPIO.OUT, initial=GPIO.LOW)
    displaychannels = [LCD_RS,LCD_EN,LCD_D4,LCD_D5,LCD_D6,LCD_D7]
    GPIO.setup(relaychannels, GPIO.OUT) #remember not to set any values in the initialization
    # above init is for the lcd and any values set would mean we are getting trash chars on the display
    lcd = LCD.Adafruit_CharLCD(rs=LCD_RS, en=LCD_EN, d4=LCD_D4, d5=LCD_D5, d6=LCD_D6, d7=LCD_D7, cols=16, lines=2)
    lcd.clear()
    return
def display():
    global lcd
    led ="OFF" if led_status()==0 else "ON"
    flt ="OFF" if filter_status()==0 else "ON"
    ap ="OFF" if airpump_status()==0 else "ON"
    top = "L:{0}|F:{1}|A:{2}".format(led,flt,ap)
    bottom = "{0:%H:%M:%S}".format(datetime.datetime.now())
    if lcd !=None:
        lcd.clear()
        lcd.set_cursor(0,0)
        lcd.message(top)
        lcd.set_cursor(0,1)
        lcd.message(bottom)
def flush():
    global lcd
    lcd.clear()
    GPIO.cleanup()
def led_status():
    return GPIO.input(LEDGPIO)
def turn_on_led():
    GPIO.output(LEDGPIO, GPIO.HIGH)
    return 0
def turn_off_led():
    GPIO.output(LEDGPIO, GPIO.LOW)
    return 0
def airpump_status():
    return GPIO.input(AIRGPIO)
def turn_on_airpump():
    GPIO.output(AIRGPIO, GPIO.HIGH)
    return 0
def turn_off_airpump():
    GPIO.output(AIRGPIO, GPIO.LOW)
    return 0
def filter_status():
    return GPIO.input(FLTGPIO)
def turn_off_filter():
    GPIO.output(FLTGPIO, GPIO.LOW)
    return 0
def turn_on_filter():
    GPIO.output(FLTGPIO, GPIO.HIGH)
    return 0
def feeder_status():
    return GPIO.input(FEEDGPIO)
def turn_off_feeder():
    GPIO.output(FEEDGPIO, GPIO.LOW)
    return 0
def turn_on_feeder():
    GPIO.output(FEEDGPIO, GPIO.HIGH)
    return 0
