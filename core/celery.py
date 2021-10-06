
app = Celery('app')
app.conf.beat_shedule = {
'ebay': {
        'task': 'dashboard.tasks.start_point_ebay_scrapers',
        'schedule': crontab(minute='*/20')
    },
}