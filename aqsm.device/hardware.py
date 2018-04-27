import RPi.GPIO as GPIO

# All the gpio identifications  on the BCM based numbering
# you would want to try out gpio readall - to know more on the BCM based numbering
LEDGPIO=21#physical pin 40
# 39 is GND  - cannot use that for the gpio purpose
AIRGPIO=20#physical pin 38
FLTGPIO=26#physical pin 37
FEEDGPIO=16#physical pin 36

def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    chan_list = [LEDGPIO,AIRGPIO,FLTGPIO,FEEDGPIO]
    GPIO.setup(chan_list, GPIO.OUT, initial=GPIO.LOW)
def flush():
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
