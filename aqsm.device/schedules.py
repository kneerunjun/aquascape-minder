from apscheduler.schedulers.background import BackgroundScheduler
import json, sys, datetime
def read_cron_settings(strCronName=None):
    '''Gets you the setting for the specific cron name
    We know all the crons are addressed by their names we can pick a specific setting
    if you do not provide the strCronName, it would return all the crons
    '''
    try:
        with open('/home/pi/src/aquascape-minder/aqsm.device/settings.json') as data_file:
            settings = json.load(data_file)["settings"]
            crons = settings["crons"]
            if strCronName !=None:
                if strCronName in crons:
                    return crons[strCronName]
                else :
                    raise Exception("Bad name for the cron setting, no such setting found - {0}".format(strCronName))
            else:
                return crons
    except FileNotFoundError as fe:
        print("schedules.py : failed to open the settings.json file ,check if the file is present and valid")
        raise fe

class Scheduler():
    def __init__(self,swb,confg,*args,**kwargs):
        self._config  = confg
        self.aps  = BackgroundScheduler()
        self._swb = swb
        rs =confg.schedules("riseandshine")
        self.aps.add_job(self.trg_riseandshine,"cron",hour=rs[0], minute=rs[1],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_middaycalm,"cron",hour=confg.schedules("middaycalm")[0], minute=confg.schedules("middaycalm")[1],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_middaycleanup,"cron",hour=confg.schedules("middaycleanup")[0], minute=confg.schedules("middaycleanup")[1],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_lateafternoon,"cron",hour=confg.schedules("lateafternoon")[0], minute=confg.schedules("lateafternoon")[1],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_twilight,"cron",hour=confg.schedules("twilight")[0], minute=confg.schedules("twilight")[1],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_supper,"cron",hour=confg.schedules("supper")[0], minute=confg.schedules("supper")[1],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_night,"cron",hour=confg.schedules("night")[0], minute=confg.schedules("night")[1],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_midnight,"cron",hour=confg.schedules("midnight")[0], minute=confg.schedules("midnight")[1],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_darknight,"cron",hour=confg.schedules("darknight")[0], minute=confg.schedules("darknight")[1],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_dawn,"cron",hour=confg.schedules("dawn")[0], minute=confg.schedules("dawn")[1],timezone="Asia/Kolkata")
        self.aps.start()
    def trg_dawn(self):
        self._swb.switch(self._config.switches("dawn"))
    def trg_darknight(self):
        self._swb.switch(self._config.switches("darknight"))
    def trg_midnight(self):
        self._swb.switch(self._config.switches("midnight"))
    def trg_night(self):
        self._swb.switch(self._config.switches("night"))
    def trg_supper(self):
        self._swb.switch(self._config.switches("supper"))
    def trg_twilight(self):
        self._swb.switch(self._config.switches("twilight"))
    def trg_middaycleanup(self):
        self._swb.switch(self._config.switches("middaycleanup"))
    def trg_middaycalm(self):
        self._swb.switch(self._config.switches("middaycalm"))
    def trg_riseandshine(self):
        self._swb.switch(self._config.switches("riseandshine"))
    def trg_lateafternoon(self):
        self._swb.switch(self._config.switches("lateafternoon"))
    def shutd(self):
        self.aps.shutdown()
