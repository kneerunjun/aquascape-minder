#   project             :aquascape minder
#   author              :kneerunjun@gmail.com
#   development         :24-APRIL-2018
#   purpose             :This helps setting up the cron jobs for the tank assiting tasks
from apscheduler.schedulers.background import BackgroundScheduler
import json, sys, datetime, pdb, hardware, logging

try:
    with open('/home/pi/src/aquascape-minder/aqsm.device/settings.json') as data_file:
        settings = json.load(data_file)
        settings = settings["settings"]
except FileNotFoundError as fe:
    print("schedules.py : failed to open the settings.json file ,check if the file is present and valid")
    sys.exit(1)
if settings!=None:
    sched = BackgroundScheduler()
# all these are slots in the schedules of an entire day
# these are basically the slots where all you can go ahead and change the relay states
riseandshine = settings["crons"]["riseandshine"]
middaycalm = settings["crons"]["middaycalm"]
middaycleanup=settings["crons"]["middaycleanup"]
lateafternoon = settings["crons"]["lateafternoon"]
twilight = settings["crons"]["twilight"]
supper = settings["crons"]["supper"]
night = settings["crons"]["night"]
midnight = settings["crons"]["midnight"]
darknight = settings["crons"]["darknight"]
dawn= settings["crons"]["dawn"]

def switch_board(settings):
    '''This is one stop place where all the cron jobs send their settings and the switch board is then operated accordingly
    settings        : variables from the global space denoting crons from settings.json
    settings object is expected to have properties as , led, airpump, filter, feeder
    '''
    ok =0
    if "led" not in settings or (settings["led"]==False and hardware.led_status()==1):
        ok =hardware.turn_off_led()
    elif settings["led"]==True and hardware.led_status()==0:
        ok =hardware.turn_on_led()
    if ok!=0:
        logging.warning("aqsm.schedules:rise_and_shine: Error with LED switch_board")
    ok=0
    if "airpump" not in settings or (settings["airpump"]==False and hardware.airpump_status()==1):
        ok =hardware.turn_off_airpump()
    elif settings["airpump"]==True and hardware.airpump_status()==0:
        ok =hardware.turn_on_airpump()
    if ok!=0:
        logging.warning("aqsm.schedules:rise_and_shine: Error with Airpump switch_board")
    ok=0
    if "filter" not in settings or (settings["filter"]==False and hardware.filter_status()==1):
        ok =hardware.turn_off_filter()
    elif settings["filter"]==True and hardware.filter_status()==0:
        ok =hardware.turn_on_filter()
    if ok!=0:
        logging.warning("aqsm.schedules:rise_and_shine: Error with Filter switch_board")
    ok=0
    if "feeder" not in settings or (settings["feeder"]==False and hardware.feeder_status()==1):
        ok =hardware.turn_off_feeder()
    elif settings["feeder"]==True and hardware.feeder_status()==0:
        ok =hardware.turn_on_feeder()
    if ok!=0:
        logging.warning("aqsm.schedules:rise_and_shine: Error with Feeder switch_board")

@sched.scheduled_job('cron', hour=riseandshine["hours"], minute=riseandshine["minutes"], timezone="Asia/Kolkata")
def rise_and_shine():
    global riseandshine
    switch_board(riseandshine)

@sched.scheduled_job('cron', hour=middaycalm["hours"], minute=middaycalm["minutes"], timezone="Asia/Kolkata")
def mid_day_calm():
    global middaycalm
    switch_board(middaycalm)

@sched.scheduled_job('cron', hour=middaycleanup["hours"], minute=middaycleanup["minutes"], timezone="Asia/Kolkata")
def mid_day_cleanup():
    global middaycleanup
    switch_board(middaycleanup)

@sched.scheduled_job('cron', hour=lateafternoon["hours"], minute=lateafternoon["minutes"], timezone="Asia/Kolkata")
def late_after_noon():
    global lateafternoon
    switch_board(lateafternoon)

@sched.scheduled_job('cron', hour=twilight["hours"], minute=twilight["minutes"], timezone="Asia/Kolkata")
def twilight():
    global twilight
    switch_board(twilight)

@sched.scheduled_job('cron', hour=supper["hours"], minute=supper["minutes"], timezone="Asia/Kolkata")
def supper():
    global supper
    switch_board(supper)

@sched.scheduled_job('cron', hour=night["hours"], minute=night["minutes"], timezone="Asia/Kolkata")
def night():
    global night
    switch_board(night)

@sched.scheduled_job('cron', hour=midnight["hours"], minute=midnight["minutes"], timezone="Asia/Kolkata")
def midnight():
    global midnight
    switch_board(midnight)

@sched.scheduled_job('cron', hour=darknight["hours"], minute=darknight["minutes"], timezone="Asia/Kolkata")
def darknight():
    global darknight
    switch_board(darknight)

@sched.scheduled_job('cron', hour=dawn["hours"], minute=dawn["minutes"], timezone="Asia/Kolkata")
def dawn():
    global dawn
    switch_board(dawn)
