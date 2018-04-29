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
lateafternoon = settings["crons"]["lateafternoon"]
twilight = settings["crons"]["twilight"]
supper = settings["crons"]["supper"]
night = settings["crons"]["night"]
midnight = settings["crons"]["midnight"]
darknight = settings["crons"]["darknight"]


@sched.scheduled_job('cron', hour=riseandshine["hours"], minute=riseandshine["minutes"], timezone="Asia/Kolkata")
def rise_and_shine():
    '''This gets triggered in the morning time , till midday
    LED     :   ON
    AIRPUMP :   ON
    FILTER  :   OFF
    FEEDER  :   OFF
    life at the tank is encouraged to get in active state, woken up from the slumber
    '''
    if  hardware.led_status()==0:
        ok =hardware.turn_on_led()
        if ok ==0:
            logging.info("aqsm.schedules: The LED was turned ON")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the LED ON")
    if  hardware.airpump_status()==0:
        ok =hardware.turn_on_airpump()
        if ok ==0:
            logging.info("aqsm.schedules: The Airpump was turned ON")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the Airpump ON")
    if  hardware.filter_status()==1:
        ok =hardware.turn_off_filter()
        if ok ==0:
            logging.info("aqsm.schedules: The filter was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the filter OFF")
    if  hardware.feeder_status()==1:
        ok =hardware.turn_off_feeder()
        if ok ==0:
            logging.info("aqsm.schedules: The feeder was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the feeder OFF")

@sched.scheduled_job('cron', hour=middaycalm["hours"], minute=middaycalm["minutes"], timezone="Asia/Kolkata")
def mid_day_calm():
    '''This gets triggered after the morning rush hour, we need to give the creatures some de-stress time
    LED     :   OFF
    AIRPUMP :   OFF
    FILTER  :   OFF
    FEEDER  :   OFF - this can be thought out if we need to trigger and leave it to feed the requisite amount
    '''
    if  hardware.led_status()==1:
        ok =hardware.turn_off_led()
        if ok ==0:
            logging.info("aqsm.schedules: The LED was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the LED OFF")
    if  hardware.airpump_status()==1:
        ok =hardware.turn_off_airpump()
        if ok ==0:
            logging.info("aqsm.schedules: The Airpump was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the Airpump OFF")
    if  hardware.filter_status()==1:
        ok =hardware.turn_off_filter()
        if ok ==0:
            logging.info("aqsm.schedules: The filter was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the filter OFF")
    if  hardware.feeder_status()==1:
        ok =hardware.turn_off_feeder()
        if ok ==0:
            logging.info("aqsm.schedules: The feeder was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the feeder OFF")

@sched.scheduled_job('cron', hour=lateafternoon["hours"], minute=lateafternoon["minutes"], timezone="Asia/Kolkata")
def late_after_noon():
    '''After some de-stressing we can resume the airpump , and let the led be off
    LED     :   OFF
    AIRPUMP :   OFF
    FILTER  :   OFF
    FEEDER  :   OFF - this can be thought out if we need to trigger and leave it to feed the requisite amount
    '''
    if  hardware.led_status()==0:
        ok =hardware.turn_on_led()
        if ok ==0:
            logging.info("aqsm.schedules: The LED was turned ON")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the LED ON")
    if  hardware.airpump_status()==0:
        ok =hardware.turn_on_airpump()
        if ok ==0:
            logging.info("aqsm.schedules: The Airpump was turned ON")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the Airpump ON")
    if  hardware.filter_status()==0:
        ok =hardware.turn_off_filter()
        if ok ==0:
            logging.info("aqsm.schedules: The filter was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the filter OFF")
    if  hardware.feeder_status()==1:
        ok =hardware.turn_off_feeder()
        if ok ==0:
            logging.info("aqsm.schedules: The feeder was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the feeder OFF")

@sched.scheduled_job('cron', hour=twilight["hours"], minute=twilight["minutes"], timezone="Asia/Kolkata")
def twilight():
    '''We continue to have the pump on , and here we go ahead to turn on the LED as well.
    LED     :   ON
    AIRPUMP :   ON
    FILTER  :   OFF
    FEEDER  :   OFF
    '''
    if  hardware.led_status()==0:
        ok =hardware.turn_on_led()
        if ok ==0:
            logging.info("aqsm.schedules: The LED was turned ON")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the LED ON")
    if  hardware.airpump_status()==0:
        ok =hardware.turn_on_airpump()
        if ok ==0:
            logging.info("aqsm.schedules: The Airpump was turned ON")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the Airpump ON")
    if  hardware.filter_status()==1:
        ok =hardware.turn_off_filter()
        if ok ==0:
            logging.info("aqsm.schedules: The filter was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the filter OFF")
    if  hardware.feeder_status()==1:
        ok =hardware.turn_off_feeder()
        if ok ==0:
            logging.info("aqsm.schedules: The feeder was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the feeder OFF")

@sched.scheduled_job('cron', hour=supper["hours"], minute=supper["minutes"], timezone="Asia/Kolkata")
def supper():
    '''We continue to have the pump on , and here we go ahead to turn on the LED as well.
    LED         :   ON
    AIRPUMP     :   OFF
    FILTER      :   OFF
    FEEDER      :   ON
    '''
    if  hardware.led_status()==0:
        ok =hardware.turn_on_led()
        if ok ==0:
            logging.info("aqsm.schedules: The LED was turned ON")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the LED ON")
    if  hardware.airpump_status()==1:
        ok =hardware.turn_off_airpump()
        if ok ==0:
            logging.info("aqsm.schedules: The Airpump was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the Airpump OFF")
    if  hardware.filter_status()==1:
        ok =hardware.turn_off_filter()
        if ok ==0:
            logging.info("aqsm.schedules: The filter was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the filter OFF")
    if  hardware.feeder_status()==0:
        ok =hardware.turn_on_feeder()
        if ok ==0:
            logging.info("aqsm.schedules: The feeder was turned ON")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the feeder ON")

@sched.scheduled_job('cron', hour=night["hours"], minute=night["minutes"], timezone="Asia/Kolkata")
def night():
    '''We continue to have the pump on , and here we go ahead to turn on the LED as well.
    LED         :   ON
    AIRPUMP     :   ON
    FILTER      :   OFF
    FEEDER      :   OFF
    '''
    if  hardware.led_status()==0:
        ok =hardware.turn_on_led()
        if ok ==0:
            logging.info("aqsm.schedules: The LED was turned ON")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the LED ON")
    if  hardware.airpump_status()==0:
        ok =hardware.turn_on_airpump()
        if ok ==0:
            logging.info("aqsm.schedules: The Airpump was turned ON")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the Airpump ON")
    if  hardware.filter_status()==1:
        ok =hardware.turn_off_filter()
        if ok ==0:
            logging.info("aqsm.schedules: The filter was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the filter OFF")
    if  hardware.feeder_status()==1:
        ok =hardware.turn_off_feeder()
        if ok ==0:
            logging.info("aqsm.schedules: The feeder was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the feeder OFF")

@sched.scheduled_job('cron', hour=midnight["hours"], minute=midnight["minutes"], timezone="Asia/Kolkata")
def midnight():
    '''This de-stressing time for the marine life, with minimum amount of aeration
    LED         :   OFF
    AIRPUMP     :   OFF
    FILTER      :   ON
    FEEDER      :   OFF
    '''
    if  hardware.led_status()==1:
        ok =hardware.turn_off_led()
        if ok ==0:
            logging.info("aqsm.schedules: The LED was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the LED OFF")
    if  hardware.airpump_status()==1:
        ok =hardware.turn_off_airpump()
        if ok ==0:
            logging.info("aqsm.schedules: The Airpump was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the Airpump OFF")
    if  hardware.filter_status()==0:
        ok =hardware.turn_on_filter()
        if ok ==0:
            logging.info("aqsm.schedules: The filter was turned ON")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the filter ON")
    if  hardware.feeder_status()==1:
        ok =hardware.turn_off_feeder()
        if ok ==0:
            logging.info("aqsm.schedules: The feeder was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the feeder OFF")

@sched.scheduled_job('cron', hour=darknight["hours"], minute=darknight["minutes"], timezone="Asia/Kolkata")
def darknight():
    '''Still water body , with only the filter on till the next high energy wake up
    LED         :   OFF
    AIRPUMP     :   OFF
    FILTER      :   ON
    FEEDER      :   OFF
    '''
    if  hardware.led_status()==1:
        ok =hardware.turn_off_led()
        if ok ==0:
            logging.info("aqsm.schedules: The LED was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the LED OFF")
    if  hardware.airpump_status()==1:
        ok =hardware.turn_off_airpump()
        if ok ==0:
            logging.info("aqsm.schedules: The Airpump was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the Airpump OFF")
    if  hardware.filter_status()==0:
        ok =hardware.turn_on_filter()
        if ok ==0:
            logging.info("aqsm.schedules: The filter was turned ON")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the filter ON")
    if  hardware.feeder_status()==1:
        ok =hardware.turn_off_feeder()
        if ok ==0:
            logging.info("aqsm.schedules: The feeder was turned OFF")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the feeder OFF")
