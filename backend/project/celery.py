from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.broker_url = 'redis://redis:6379/0'
app.conf.result_backend = 'redis://redis:6379/0'

app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']
app.conf.enable_utc = True
app.conf.timezone = 'Asia/Baghdad'

app.conf.beat_schedule = {
    'scrape-all-stocks-at-1am-iraq-time': {
        'task': 'marketing.tasks.scrape_all_stocks',
        'schedule': crontab(hour=12, minute=45),
    },
    'scrape-all-commodities-at-am-iraq-time': {
        'task': 'marketing.tasks.scrape_all_commodities',
        'schedule': crontab(hour=12, minute=45),
    },
    'scrape-all-cryptocurrencies-at-0am-iraq-time': {
        'task': 'marketing.tasks.scrape_all_cryptocurrencies',
        'schedule': crontab(hour=12, minute=45),
    },
    'log-time-every-1-minutes': {
        'task': 'marketing.tasks.log_current_time',
        'schedule': crontab(minute='*/15'),
    },
    'check-cache-contents-hourly': {
        'task': 'marketing.tasks.check_cache_contents',
        'schedule': crontab(hour='*', minute=0),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

