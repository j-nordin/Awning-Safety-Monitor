import os
from crontab import CronTab

filepath = os.path.join(os.path.dirname(__file__), 'main.py')

def set_check_interval_to_15_min(command: str):
    cron = CronTab(user=True)
    cron.remove_all(comment='awning')
    job = cron.new(command=command, comment="awning")
    # TODO: Change to 15 min
    job.minute.every(1)
    cron.write()


def set_check_interval_to_3_h(command: str):
    cron = CronTab(user=True)
    cron.remove_all(comment='awning')
    job = cron.new(command=command, comment="awning")
    job.hour.every(3)
    cron.write()


if __name__ == '__main__':
    set_check_interval_to_15_min(f"python {filepath}")
