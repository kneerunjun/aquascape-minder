### Cron jobs, interval jobs, dated jobs

My project here needed me to schedule jobs , code functions running at specific times of the day, on all days. [My aquarium and IoT](https://kneerunjun.github.io/aquascape-minder/). Here the aquarium needed specific electrical accessories to be turned ON /OFF depending on the time of the day. This ensures optimum run time for all the accessories and also lets the aquarium owners be hands-off from the sustenance tasks.

For people who dont like any 3rd party software / packages / frameworks written for them , would ofcourse rely on a continuous loops checking for the current time. Some time calculations and formatting in python (which I dont think is too cumbersome) can still get you there.

But here is something that I found handy to schedule cron like jobs. [ApScheduler](https://apscheduler.readthedocs.io/en/latest/userguide.html)

An Excerpt from web , describes the package quite succintly

>Advanced Python Scheduler (APScheduler) is a Python library that lets you schedule your Python code to be executed later, either just once or periodically. You can add new jobs or remove old ones on the fly as you please. If you store your jobs in a database, they will also survive scheduler restarts and maintain their state. When the scheduler is restarted, it will then run all the jobs it should have run while it was offline

### Non blocking background scheduler :

Setting up the scheduler and starting it is quite simple and easy

```python
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler()
sched.start()
# yeah ! and thats all what is required to start a scheduler
```

Above doesn't do too many things - simply cause it hasn't got any jobs scheduled for now. So what can you do to schedule jobs for this scheduler ?

```python
sched = BackgroundScheduler()
@sched.scheduled_job('cron', hour='6-10', minute='0-59', timezone="Asia/Kolkata")
def call_this_on_trigger():
  # dosomething here that you want to between 06:00-10:59
  # this is fired everyminute between that time slot
  pass
sched.start()
```

Using decorators is always better , one for it makes you look cool, and then recollecting the logic at a later date is so very easy.
