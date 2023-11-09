from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
scheduler = BackgroundScheduler(daemon=True)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

from pingurl import watched_urls