#   This was developed to keep the cloud database updated with the data on the ground
#   Has threaded tasks that can be fired to send data up to the cloud else get data from the cloud
#   author      : kneerunjun@gmail.combak
#   dated       : April 2018

import threading, pdb, time, requests
class KillableT(threading.Thread):
    '''This just signifies the a threaded task having a kill event in it'''
    def __init__(self,*args, **kwargs):
        super(KillableT,self).__init__()
        self.killEvent = kwargs["killevent"]
class CloudLink(KillableT):
    def __init__(self,*args, **kwargs):
        super(CloudLink,self).__init__(*args, **kwargs)
        self.url = kwargs["url"]
    def check_link(self):
        if self.url!=None :
            return True if(requests.get(self.url).status_code==200) else False
        else:
            return False
class UplinkingT(CloudLink):
    '''Worker thread that helps send the device recordings to the cloud
    '''
    def __init__(self,*args, **kwargs):
        super(UplinkingT,self).__init__(*args, **kwargs)
        self.delay = kwargs["delay"]
    def run(self):
        while not self.killEvent.wait(1):
            if self.check_link()==True:
                print("uplinking now..")
                # this is where we go ahead to upload to the api
                # uplink is now established
            else:
                time.sleep(30)
                # a long 30 second wait before you can try for another time
                # so when the cloud is not up , the thread just sleeps for 30 seconds in between
            time.sleep(self.delay)
class DownlinkingT(CloudLink):
    '''Worker thread that helps the device to be in constant touch with the settings change on the cloud. This would check for connectivity
    '''
    def __init__(self,*args, **kwargs):
        super(DownlinkingT,self).__init__(*args, **kwargs)
        self.delay = kwargs["delay"]
    def run(self):
        while not self.killEvent.wait(1):
            if self.check_link()==True:
                print("downlinking now..")
            else:
                time.sleep(30)
                # a long 30 second wait before you can try for another time
                # so when the cloud is not up , the thread just sleeps for 30 seconds in between
            time.sleep(self.delay)
