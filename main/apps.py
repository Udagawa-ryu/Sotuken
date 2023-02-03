from django.apps import AppConfig
from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import datetime


class MainConfig(AppConfig):
    name = 'main'
    def ready(self):
        start()

def backup_run():
    date = datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
    res = subprocess.run("python manage.py dbbackup -o "+date+".dump", stdout=subprocess.PIPE, shell=True, encoding="shift-jis")
    print(res.stdout)

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(backup_run, 'cron', hour=23, minute=59,misfire_grace_time=60*60)# 毎日23時59分に実行
    scheduler.start()
