#   project             :aquascape minder
#   author              :kneerunjun@gmail.com
#   development         :24-APRIL-2018
#   purpose             :This helps setting up the cron jobs for the tank assiting tasks
from apscheduler.schedulers.background import BackgroundScheduler
import json, sys, datetime, pdb, hardware, logging

sched = BackgroundScheduler()

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
def switch_board(cronsettings):
    '''This is one stop place where all the cron jobs send their settings and the switch board is then operated accordingly
    settings        : variables from the global space denoting crons from settings.json
    settings object is expected to have properties as , led, airpump, filter, feeder
    '''
    ok =0
    if "led" not in cronsettings or (cronsettings["led"]==False and hardware.led_status()==1):
        ok =hardware.turn_off_led()
    elif cronsettings["led"]==True and hardware.led_status()==0:
        print("LED being turned on")
        ok =hardware.turn_on_led()
    if ok!=0:
        logging.warning("aqsm.schedules:rise_and_shine: Error with LED switch_board")
    ok=0
    if "airpump" not in cronsettings or (cronsettings["airpump"]==False and hardware.airpump_status()==1):
        ok =hardware.turn_off_airpump()
    elif cronsettings["airpump"]==True and hardware.airpump_status()==0:
        print("Airpump being turned on")
        ok =hardware.turn_on_airpump()
    if ok!=0:
        logging.warning("aqsm.schedules:rise_and_shine: Error with Airpump switch_board")
    ok=0
    if "filter" not in cronsettings or (cronsettings["filter"]==False and hardware.filter_status()==1):
        print("Filter being turned off")
        ok =hardware.turn_off_filter()
    elif cronsettings["filter"]==True and hardware.filter_status()==0:
        ok =hardware.turn_on_filter()
    if ok!=0:
        logging.warning("aqsm.schedules:rise_and_shine: Error with Filter switch_board")
    ok=0
    if "feeder" not in cronsettings or (cronsettings["feeder"]==False and hardware.feeder_status()==1):
        ok =hardware.turn_off_feeder()
    elif cronsettings["feeder"]==True and hardware.feeder_status()==0:
        ok =hardware.turn_on_feeder()
    if ok!=0:
        logging.warning("aqsm.schedules:rise_and_shine: Error with Feeder switch_board")
cron_settings  = read_cron_settings()
@sched.scheduled_job('cron', hour=cron_settings["riseandshine"]["hours"], minute=cron_settings["riseandshine"]["minutes"], timezone="Asia/Kolkata")
def call_riseandshine():
    switch_board(read_cron_settings("riseandshine"))

@sched.scheduled_job('cron', hour=cron_settings["middaycalm"]["hours"], minute=cron_settings["middaycalm"]["minutes"], timezone="Asia/Kolkata")
def call_middaycalm():
    switch_board(read_cron_settings("middaycalm"))

@sched.scheduled_job('cron', hour=cron_settings["middaycleanup"]["hours"], minute=cron_settings["middaycleanup"]["minutes"], timezone="Asia/Kolkata")
def call_middaycleanup():
    switch_board(read_cron_settings("middaycleanup"))

@sched.scheduled_job('cron', hour=cron_settings["lateafternoon"]["hours"], minute=cron_settings["lateafternoon"]["minutes"], timezone="Asia/Kolkata")
def call_lateafternoon():
    switch_board(read_cron_settings("lateafternoon"))

@sched.scheduled_job('cron', hour=cron_settings["twilight"]["hours"], minute=cron_settings["twilight"]["minutes"], timezone="Asia/Kolkata")
def call_twilight():
    switch_board(read_cron_settings("twilight"))

@sched.scheduled_job('cron', hour=cron_settings["supper"]["hours"], minute=cron_settings["supper"]["minutes"], timezone="Asia/Kolkata")
def call_supper():
    switch_board(read_cron_settings("supper"))

@sched.scheduled_job('cron', hour=cron_settings["night"]["hours"], minute=cron_settings["night"]["minutes"], timezone="Asia/Kolkata")
def call_night():
    switch_board(read_cron_settings("night"))

@sched.scheduled_job('cron', hour=cron_settings["midnight"]["hours"], minute=cron_settings["midnight"]["minutes"], timezone="Asia/Kolkata")
def call_midnight():
    switch_board(read_cron_settings("midnight"))

@sched.scheduled_job('cron', hour=cron_settings["darknight"]["hours"], minute=cron_settings["darknight"]["minutes"], timezone="Asia/Kolkata")
def call_darknight():
    switch_board(read_cron_settings("darknight"))

@sched.scheduled_job('cron', hour=cron_settings["dawn"]["hours"], minute=cron_settings["dawn"]["minutes"], timezone="Asia/Kolkata")
def dawn():
    switch_board(read_cron_settings("dawn"))
