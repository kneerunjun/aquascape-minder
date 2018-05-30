import Adafruit_ADS1x15
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import datetime
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
    def __init__(self,swb,*args, **kwargs):
        self.colWidth = 24
        self.iconOffset=3
        self.headers =["oC","LED","FLT","AIR","FDR"]
        self.oled  = OLEDDisp()
        self._swb = swb
    def shutd(self):
        self.oled.refresh()
        self.oled.flush()
    def display_status(self):
        self.oled.refresh()
        self.oled.draw_text(text="{0:%H:%M:%S   %m/%d}".format(datetime.datetime.now()),x=0,y=0).draw_thin_ellipse(100,0,10,10).draw_text("A",115,0)
        for idx, h in enumerate(self.headers):
            self.oled=self.oled.draw_text(h,idx*self.colWidth,16)
        wt = self._swb.temp()
        if wt!=None:
            self.oled.draw_text(str(wt),0,32)
        for idx, h in enumerate(self.headers):
            if idx!=0 :
                if getattr(self._swb,h.lower())()==0:
                    self.oled=self.oled.draw_thin_rectangle((idx*self.colWidth)+self.iconOffset,32,10,10)
                elif getattr(self._swb,h.lower())()==1:
                    self.oled=self.oled.draw_thick_rectangle((idx*self.colWidth)+self.iconOffset,32,10,10)
        self.oled.render()
