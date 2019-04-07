#Author: s3634919 Renning Liu
#!/usr/bin/env python3
from crontab import CronTab
    

def set_job():
    cron = CronTab(user='pi')
    cron.remove_all()

    job  = cron.new(command='python3 /home/pi/assignment1/monitorAndNotify.py')
    job.day.every(1)
    job.every_reboot()

    sec_job = cron.new(command='python3 /home/pi/assignment1/bluetooth.py')
    sec_job.every_reboot()
    cron.write()

if __name__ == "__main__":
    set_job()
