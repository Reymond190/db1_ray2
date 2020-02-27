import os
from celery import Celery
from one.tasks import all2

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'db1.settings')

app = Celery('db1')

app.config_from_object('django.conf:settings', namespace='CELERY')



from one.tasks import all2

app.conf.beat_schedule = {
    "see-you-in-ten-seconds-task": {
        "task": "one.tasks.all2",
        "schedule": 10.0,
    }

}
