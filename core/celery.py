import os
from datetime import timedelta
from celery._state import _set_current_app
from celery import Celery
from celery.schedules import crontab
from kombu import Queue, Exchange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_shedule = {
'ebay': {
        'task': 'dashboard.tasks.start_point_ebay_scrapers',
        'schedule': crontab(minute='*/2')
    },
'test_task_starter' : {
       'task': 'dashboard.tasks.test',
       'schedule': crontab(minute='*/2'), 
   }
}

app.conf.task_default_queue = 'default'
default_exchange = Exchange('default', type='direct')
app.conf.task_queues = (
    Queue('default', default_exchange, routing_key='default'),)






@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
