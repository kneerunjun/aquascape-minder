import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import pdb, datetime, threading, time
import Adafruit_ADS1x15
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
# All the gpio identifications  on the BCM based numbering
# you would want to try out gpio readall - to know more on the BCM based numbering
# LEDGPIO=17          #physical pin 11
# AIRGPIO=27          #physical = 13
# FLTGPIO=22          #physical = 15
# FEEDGPIO=23         #physical = 16
# configuaration for the  6 LCD pins
# LCD_RS = 21         # phsical = 40
# 39 is GND  - cannot use that for the gpio purpose
# LCD_EN = 20         # physical= 38
# LCD_D4 = 26         # physical= 37
# LCD_D5 = 19         # physical= 35
# LCD_D6 = 13         # physical= 33
# LCD_D7 = 6          # physical= 31
# GAINFACTOR = (8, 0.512)# 8 = +/-0.512V : since currently we have temperature not going beyond 50
# TEMPCHN =3           # we have the signal from the LM35 connected to the A3 channel
# lcd = None          # global lcd handle, can be used after the init call
# adc = Adafruit_ADS1x15.ADS1115()    #inititlization of the ADC chipset
# def init_archived():
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)
#     global lcd              #is  a module level variable that we are accessing , so keyword global
#     relaychannels = [LEDGPIO,AIRGPIO,FLTGPIO,FEEDGPIO]
#     GPIO.setup(relaychannels, GPIO.OUT, initial=GPIO.LOW)
#     displaychannels = [LCD_RS,LCD_EN,LCD_D4,LCD_D5,LCD_D6,LCD_D7]
#     GPIO.setup(relaychannels, GPIO.OUT) #remember not to set any values in the initialization
#     # above init is for the lcd and any values set would mean we are getting trash chars on the display
#     lcd = LCD.Adafruit_CharLCD(rs=LCD_RS, en=LCD_EN, d4=LCD_D4, d5=LCD_D5, d6=LCD_D6, d7=LCD_D7, cols=16, lines=2)
#     lcd.clear()
#     return
# def display_archived():
#     global lcd
#     led ="OFF" if led_status()==0 else "ON"
#     flt ="OFF" if filter_status()==0 else "ON"
#     ap ="OFF" if airpump_status()==0 else "ON"
#     top = "L:{0}|F:{1}|A:{2}".format(led,flt,ap)
#     bottom = "{0:%H:%M:%S}".format(datetime.datetime.now())
#     if lcd !=None:
#         lcd.clear()
#         lcd.set_cursor(0,0)
#         lcd.message(top)
#         lcd.set_cursor(0,1)
#         lcd.message(bottom)
def flush():
    GPIO.cleanup()
class SwitchBoard():
    '''One thread safe object that controls all the relays and gives access to all electrical accessories. It is thread safe since we have multiple threads in the single process accessing the SwitchBoard concurrently
    '''
    def __init__(self, *args, **kwargs):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.gpioLED =17    # physical = 11
        self.gpioAIR =27    # physical = 13
        self.gpioFLT =22    # physical = 15
        self.gpioFDR =26    # physical = 16
        GPIO.setup(self.gpioLED, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.gpioAIR, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.gpioFLT, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.gpioFDR, GPIO.OUT, initial=GPIO.LOW)
        self.gpioLck  = threading.Lock()        #this helps us to deal with multiple threads on the single switch board
        self.watertemp=None
    def shutd(self):
        GPIO.output(self.gpioLED, GPIO.LOW)
        GPIO.output(self.gpioAIR, GPIO.LOW)
        GPIO.output(self.gpioFLT, GPIO.LOW)
        GPIO.output(self.gpioFDR, GPIO.LOW)
    def led(self,switch=None):
        status =None
        self.gpioLck.acquire()
        if switch !=None:
            if GPIO.input(self.gpioLED)==0 and switch ==1:
                GPIO.output(self.gpioLED, GPIO.HIGH)
            elif GPIO.input(self.gpioLED)==1 and switch ==0:
                GPIO.output(self.gpioLED, GPIO.LOW)
        else:
            status= GPIO.input(self.gpioLED)
        self.gpioLck.release()
        return status if status!=None else self
    def air(self,switch=None):
        status=None
        self.gpioLck.acquire()
        if switch !=None:
            if GPIO.input(self.gpioAIR)==0 and switch ==1:
                GPIO.output(self.gpioAIR, GPIO.HIGH)
            elif GPIO.input(self.gpioAIR)==1 and switch ==0:
                GPIO.output(self.gpioAIR, GPIO.LOW)
        else:
            status= GPIO.input(self.gpioAIR)
        self.gpioLck.release()
        return status if status!=None else self
    def flt(self,switch=None):
        status=None
        self.gpioLck.acquire()
        if switch !=None:
            if GPIO.input(self.gpioFLT)==0 and switch ==1:
                GPIO.output(self.gpioFLT, GPIO.HIGH)
            elif GPIO.input(self.gpioFLT)==1 and switch ==0:
                GPIO.output(self.gpioFLT, GPIO.LOW)
        else:
            status= GPIO.input(self.gpioFLT)
        self.gpioLck.release()
        return status if status!=None else self
    def fdr(self,switch=None):
        status=None
        self.gpioLck.acquire()
        if switch !=None:
            if GPIO.input(self.gpioFDR)==0 and switch ==1:
                GPIO.output(self.gpioFDR, GPIO.HIGH)
            elif GPIO.input(self.gpioFDR)==1 and switch ==0:
                GPIO.output(self.gpioFDR, GPIO.LOW)
        else:
            status=  GPIO.input(self.gpioFDR)
        self.gpioLck.release()
        return status if status!=None else self
    def htr(self, switch=None):
        self.gpioLck.acquire()
        result = None
        if switch!=None:
            self.watertemp = switch
            self.gpioLck.release()
            result =self
        else:
            result= self.watertemp
            self.gpioLck.release()
        return result
class OLEDDisp():
    def __init__(self, *args, **kwargs):
        self.disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
        self.disp.begin();
        self.disp.clear();
        self.disp.display()
        self.w=self.disp.width
        self.h=self.disp.height
        self.l=0
        self.padding =1
        self.top  = self.padding
        self.bottom = self.h - self.padding
        self.image = Image.new('1', (self.w, self.h))
        self.draw = ImageDraw.Draw(self.image)
        self.fontSz = 9
        self.font  = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', self.fontSz)
    def draw_text(self,text,x,y):
        self.draw.text((x,y),text,font=self.font,fill=255)
        return self
    def draw_thick_rectangle(self,x,y,width,height):
        self.draw.rectangle((x,y,x+width,y+height), outline=255, fill=1)
        return self
    def draw_thin_rectangle(self,x,y,width,height):
        self.draw.rectangle((x,y,x+width,y+height), outline=255, fill=0)
        return self
    def draw_thick_ellipse(self,x,y,width,height):
        self.draw.ellipse((x,y,x+width,y+height), outline=255, fill=1)
        return self
    def draw_thin_ellipse(self,x,y,width,height):
        self.draw.ellipse((x,y,x+width,y+height), outline=255, fill=0)
        return self
    def render(self):
        self.disp.image(self.image)
        self.disp.display()
        return self
    def flush(self):
        self.refresh().disp.display()
    def refresh(self):
        self.draw.rectangle((0,0,self.w,self.h), outline=0, fill=0)
        self.disp.image(self.image)
        return self
class AqsmOLED():
    '''This just enacapsulates the OLEDDisp to have the domain logic of this specific project
    All the layouting information is in here,and all what we now need is some interface by which this connects to the switchboard to get all the information
    '''
    def __init__(self,*args, **kwargs):
        self.colWidth = 24
        self.iconOffset=3
        self.headers =["oC","LED","FLT","AIR","FDR"]
        self.oled  = OLEDDisp()
    def shutd(self):
        self.oled.flush()
    def display_status(self,sb):
        self.oled.refresh()
        self.oled.draw_text(text="{0:%H:%M:%S   %m/%d}".format(datetime.datetime.now()),x=0,y=0).draw_thin_ellipse(100,0,10,10).draw_text("A",115,0)
        for idx, h in enumerate(self.headers):
            self.oled=self.oled.draw_text(h,idx*self.colWidth,16)
        wt = sb.htr()
        if wt!=None:
            self.oled.draw_text(str(wt),0,32)
        for idx, h in enumerate(self.headers):
            if idx!=0 :
                if getattr(sb,h.lower())()==0:
                    self.oled=self.oled.draw_thin_rectangle((idx*self.colWidth)+self.iconOffset,32,10,10)
                elif getattr(sb,h.lower())()==1:
                    self.oled=self.oled.draw_thick_rectangle((idx*self.colWidth)+self.iconOffset,32,10,10)
        self.oled.render()
class AqsmThermometer():
    def __init__(self,*args, **kwargs):
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.gainfactor=(8, 0.512)
        self.channel =3
    def measure(self, sb):
        volts = (self.gainfactor[1]*self.adc.read_adc(self.channel, gain=self.gainfactor[0]))/32768
        sb.htr(switch=round(volts*100,1))
