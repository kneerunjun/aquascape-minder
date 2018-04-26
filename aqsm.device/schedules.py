#   project             :aquascape minder
#   author              :kneerunjun@gmail.com
#   development         :24-APRIL-2018
#   purpose             :This helps setting up the cron jobs for the tank assiting tasks
from apscheduler.schedulers.background import BackgroundScheduler
import json, sys, datetime, pdb,

try:
    with open('./settings.json') as data_file:
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


hardware.init()         # we are expecting the hardware GPIO to get initialized here
@sched.scheduled_job('cron', hour=riseandshine["hours"], minute=riseandshine["minutes"], timezone="Asia/Kolkata")
def rise_and_shine():
    '''This gets triggered in the morning time , till midday
    LED     :   ON
    AIRPUMP :   ON
    FILTER  :   OFF
    FEEDER  :   OFF
    life at the tank is encouraged to get in active state, woken up from the slumber
    '''
    # confirm shall return 0/-1 to confirm if the action was success
    if  hardware.led_status()==0:
        ok =hardware.turn_on_led()
        if ok ==0:
            logging.info("aqsm.schedules: The LED was turned ON")
        else:
            logging.warning("aqsm.schedules:rise_and_shine: Error turning the LED ON")

    confirm =hardware.turn_on_airpump()if hardware.airpump_status()==0 else None
    if confirm !=None:
        logging.info("aqsm.schedules: The airpump was turned ON")
    else:
        logging.debug("aqsm.schedules:The airpump was already ON")
    confirm=hardware.turn_off_filter() if hardware.filter_status()==1 else None
    if confirm !=None:
        logging.info("aqsm.schedules: The filter was turned OFF")
    else:
        logging.debug("aqsm.schedules:The filter was already OFF")
    confirm =hardware.turn_off_feeder() if hardware.feeder_status()==1 else None
    if confirm !=None:
        logging.info("aqsm.schedules: The feeder was turned OFF")
    else:
        logging.debug("aqsm.schedules:The feeder was already OFF")
