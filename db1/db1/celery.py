import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'db1.settings')

app = Celery('db1')

app.config_from_object('django.conf:settings', namespace='CELERY')




app.conf.beat_schedule = {
    "see-you-in-ten-seconds-task": {
        "task": "one.tasks.all2",
        "schedule": 10.0,
    },
    "clean_and_store":{
        "task":"one.task.clean_store",
        "schedule":crontab(),
    }

}
