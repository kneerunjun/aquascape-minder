import threading, pdb, time

class UplinkingT(threading.Thread):
    '''Worker thread that helps send the device recordings to the cloud
    '''
    def __init__(self,ke,cfg):
        super(UplinkingT,self).__init__()
        self.killEvent  = ke
        self.config = cfg
    def run(self):
        while not self.killEvent.wait(1):
            print("Uplinking now..")
            time.sleep(self.config["delays"]["uplinking"])
class DownlinkingT(threading.Thread):
    '''Worker thread that helps the device to be in constant touch with the settings change on the cloud
    '''
    def __init__(self,ke,cfg):
        super(DownlinkingT,self).__init__()
        self.killEvent  = ke
        self.config = cfg
    def run(self):
        while not self.killEvent.wait(1):
            print("Downlinking now..")
            time.sleep(self.config["delays"]["downlinking"])
