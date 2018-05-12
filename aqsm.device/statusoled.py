#!/usr/bin/python3
#   Author          : kneerunjun@gmail.com
#   Version         : 0.0.0
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Syntactic wrapper for SD1306 Adafruit https://github.com/adafruit/Adafruit_Python_SSD1306.git
# clone the repository
# python3 setup.py install
# use chaining on the functions to display on the OLED over I2C
# default I2C slave address that the SSD1306 gets configured = 0x3c
# we are currently making this for 64 dots height - since it gives us the best results
# DejaVuSerif = is the default font , need to change this for it to load default font

import datetime, time
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
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
        self.disp.clear()
        self.disp.display()
    def refresh(self):
        self.draw.rectangle((0,0,self.w,self.h), outline=0, fill=0)
        self.disp.image(self.image)
        self.disp.display()
        return self
class AqsmOLED():
    '''This just enacapsulates the OLEDDisp to have the domain logic of this specific project
    All the layouting information is in here,and all what we now need is some interface by which this connects to the switchboard to get all the information
    '''
    def __init__(self,*args, **kwargs):
        self.colWidth = 24
        self.iconOffset=3
        headers =["oC","LED","FLT","AIR","FDR"]
        self.oled  = OLEDDisp().draw_text(text="{0:%H:%M:%S   %m/%d}".format(datetime.datetime.now()),x=0,y=0).draw_thin_ellipse(100,0,10,10).draw_text("A",115,0)
        for idx, h in enumerate(headers):
            self.oled=self.oled.draw_text(h,idx*self.colWidth,16)
        for idx, h in enumerate(headers):
            if idx!=0 :
                self.oled=self.oled.draw_thin_rectangle((idx*self.colWidth)+self.iconOffset,32,10,10)
        self.oled.render()
if __name__ == "__main__":
    oled  = AqsmOLED()
    time.sleep(60)
