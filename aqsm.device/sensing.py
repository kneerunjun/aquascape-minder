import Adafruit_ADS1x15

class AqsmThermometer():
    def __init__(self,swb,*args, **kwargs):
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.gainfactor=(8, 0.512)
        self.channel =3
        self._swb = swb
    def measure(self):
        volts = (self.gainfactor[1]*self.adc.read_adc(self.channel, gain=self.gainfactor[0]))/32768
        self._swb.put(watertemp=round(volts*100,1))
