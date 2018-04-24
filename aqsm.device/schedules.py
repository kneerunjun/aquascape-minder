#   project             :aquascape minder
#   author              :kneerunjun@gmail.com
#   development         :24-APRIL-2018
#   purpose             :This helps setting up the cron jobs for the tank assiting tasks
from apscheduler.schedulers.background import BackgroundScheduler
import json, sys, datetime, pdb
# initially we would want to pick from settings the cron job timing
try:
    with open('./settings.json') as data_file:
        settings = json.load(data_file)
        settings = settings["settings"]
except FileNotFoundError as fe:
    print("schedules.py : failed to open the settings.json file ,check if the file is present and valid")
    sys.exit(1)

# now once we have the settings , we need to go ahead and set initial state of the devices according to the time we have now. Else lets say we start the program at 18:01 , the jobs devices that should have been turned ON at 18:00 would not have started anyway
# NOTE: Setting the initial state for each of the devices at the start of the program
# everything here is based on finding the settings.json file
if settings!=None:
    sched = BackgroundScheduler()

# def compress_list_tostring(lst):
#     '''This helps to convert the incoming list from the json to a comma separated string
#     Comma separated string is used to setup the cron job on specific hours
#     '''
#     return ','.join(map(str, lst))
# def device_schedule(devicename, on_off=1):
#     '''This digs into the settins dictionary and gets the ON, OFF schedule as required
#     returns a tuple (hours , minutes) that signify the hours & minutes at which the triggers are fired. It spits out an list , so you may have to compress_list_tostring before setting up cron jobs
#     on_off      : schedule for on time ==1 and schedule for off time ==0
#     '''
#     if settings!=None:
#         device =settings["crons"]["{0}".format(devicename)]
#         hrs =device["off"]["hours"] if on_off==0 else device["on"]["hours"]
#         mins =device["off"]["minutes"] if on_off==0 else device["on"]["minutes"]
#         return (hrs, mins)

# NOTE: Refer to the settings, we now have range of values for hours and minutes and hence the cron job is to fire  every minute - but we now block the action depending on if only there is a state change
led_on_schedule = settings["crons"]["led"]["on"]
led_off_schedule = settings["crons"]["led"]["off"]
@sched.scheduled_job('cron', hour=led_on_schedule["hours"], minute=led_on_schedule["minutes"], timezone="Asia/Kolkata")
def turn_on_led():
	print("LED is now being turned on")
@sched.scheduled_job('cron', hour=led_off_schedule["hours"], minute=led_off_schedule["minutes"], timezone="Asia/Kolkata")
def turn_off_led():
	print("LED is now being turned off")

# now working this for the airpump
air_on_schedule = settings["crons"]["airpump"]["on"]
air_off_schedule = settings["crons"]["airpump"]["off"]
@sched.scheduled_job('cron', hour=air_on_schedule["hours"], minute=air_off_schedule["minutes"], timezone="Asia/Kolkata")
def turn_on_air():
	print("Airpump is now being turned on")
@sched.scheduled_job('cron', hour=air_off_schedule["hours"], minute=air_off_schedule["minutes"], timezone="Asia/Kolkata")
def turn_off_air():
	print("Airpump is now being turned off")

# now working this for the filter
filter_on_schedule = settings["crons"]["filter"]["on"]
filter_off_schedule = settings["crons"]["filter"]["off"]

@sched.scheduled_job('cron', hour=filter_on_schedule["hours"], minute=filter_on_schedule["minutes"], timezone="Asia/Kolkata")
def turn_on_filter():
	print("Filter is now being turned on")

@sched.scheduled_job('cron', hour=filter_off_schedule["hours"], minute=filter_off_schedule["minutes"], timezone="Asia/Kolkata")
def turn_off_filter():
	print("Filter is now being turned off")

# now working this for the feeder
feeder_on_schedule = settings["crons"]["feeder"]["on"]
feeder_off_schedule = settings["crons"]["feeder"]["off"]

@sched.scheduled_job('cron', hour=feeder_on_schedule["hours"], minute=feeder_on_schedule["minutes"], timezone="Asia/Kolkata")
def turn_on_feeder():
	print("Feeder is now being turned on")

@sched.scheduled_job('cron', hour=feeder_off_schedule["hours"], minute=feeder_off_schedule["minutes"], timezone="Asia/Kolkata")
def turn_off_feeder():
	print("Feeder is now being turned off")
