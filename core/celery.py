import os
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
from kombu import Queue, Exchange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
'ebay': {
        'task': 'dashboard.tasks.start_point_ebay_scrapers',
        'schedule': 10.0,
    },
'test_task_starter' : {
       'task': 'dashboard.tasks.test',
       'schedule': 10.0, 
   }
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
