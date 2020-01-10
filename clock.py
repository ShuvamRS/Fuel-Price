from apscheduler.schedulers.blocking import BlockingScheduler
from subprocess import call
from datetime import date, timedelta
import calendar
import holidays


sched = BlockingScheduler()

'''
Web Scraping done at 5:30 pm as fuel prices get posted
around 5:00 pm on Mondays except on government holidays
in which case data are posted the following day.
'''
@sched.scheduled_job('cron', day_of_week='mon-tue', hour=17, minute=30)
def scheduled_job():
	US_holidays = holidays.UnitedStates()
	today = date.today()

	# If current day is Monday and it is not a holiday
	if today.weekday() == 0 and today not in US_holidays:
		call(["python", "scraper.py"])

	# If current day is Tuesday and preceding Monday was a holiday
	elif today.weekday() == 1 and (today - timedelta(days = 1)) in US_holidays:
		call(["python", "scraper.py"])


sched.start()
