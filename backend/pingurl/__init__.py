import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

app = Flask(__name__)
scheduler = BackgroundScheduler(daemon=True)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
