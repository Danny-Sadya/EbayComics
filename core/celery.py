import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab
from kombu import Queue, Exchange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.autodiscover_tasks()
app.conf.beat_shedule = {
'ebay': {
        'task': 'dashboard.tasks.start_point_ebay_scrapers',
        'schedule': crontab(minute='*/20')
    },
}


app.conf.timezone = 'UTC'


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
