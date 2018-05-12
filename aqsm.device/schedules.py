#   project             :aquascape minder
#   author              :kneerunjun@gmail.com
#   development         :24-APRIL-2018
#   purpose             :This helps setting up the cron jobs for the tank assiting tasks
from apscheduler.schedulers.background import BackgroundScheduler
import json, sys, datetime, pdb, hardware, logging
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
    def __init__(self,sb,*args,**kwargs):
        settings = read_cron_settings()
        self.aps  = BackgroundScheduler()
        self.aps.add_job(self.trg_riseandshine,"cron",hour=settings["riseandshine"]["hours"], minute=settings["riseandshine"]["minutes"],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_middaycalm,"cron",hour=settings["middaycalm"]["hours"], minute=settings["middaycalm"]["minutes"],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_middaycleanup,"cron",hour=settings["middaycleanup"]["hours"], minute=settings["middaycleanup"]["minutes"],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_lateafternoon,"cron",hour=settings["lateafternoon"]["hours"], minute=settings["lateafternoon"]["minutes"],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_twilight,"cron",hour=settings["twilight"]["hours"], minute=settings["twilight"]["minutes"],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_supper,"cron",hour=settings["supper"]["hours"], minute=settings["supper"]["minutes"],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_night,"cron",hour=settings["night"]["hours"], minute=settings["night"]["minutes"],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_midnight,"cron",hour=settings["midnight"]["hours"], minute=settings["midnight"]["minutes"],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_darknight,"cron",hour=settings["darknight"]["hours"], minute=settings["darknight"]["minutes"],timezone="Asia/Kolkata")
        self.aps.add_job(self.trg_dawn,"cron",hour=settings["dawn"]["hours"], minute=settings["dawn"]["minutes"],timezone="Asia/Kolkata")
        self.sb = sb
        self.aps.start()
    def operate_switch_board(self, sett):
        self.sb.led(switch =sett["led"])\
        .air(switch=sett["airpump"])\
        .flt(switch=sett["filter"])\
        .fdr(switch=sett["feeder"])
    def trg_dawn(self):
        self.operate_switch_board(read_cron_settings("dawn"))
    def trg_darknight(self):
        self.operate_switch_board(read_cron_settings("darknight"))
    def trg_midnight(self):
        self.operate_switch_board(read_cron_settings("midnight"))
    def trg_night(self):
        self.operate_switch_board(read_cron_settings("night"))
    def trg_supper(self):
        self.operate_switch_board(read_cron_settings("supper"))
    def trg_twilight(self):
        self.operate_switch_board(read_cron_settings("twilight"))
    def trg_middaycleanup(self):
        self.operate_switch_board(read_cron_settings("middaycleanup"))
    def trg_middaycalm(self):
        self.operate_switch_board(read_cron_settings("middaycalm"))
    def trg_riseandshine(self):
        self.operate_switch_board(read_cron_settings("riseandshine"))
    def trg_lateafternoon(self):
        self.operate_switch_board(read_cron_settings("lateafternoon"))
    def shutd(self):
        self.aps.shutdown()
