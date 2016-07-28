from __future__ import absolute_import

import os
from datetime import timedelta

import django

from celery import Celery
from celery.schedules import crontab
from django.conf import settings


CELERY_TIMEZONE = 'UTC'
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'linker.settings')
django.setup()
app = Celery('linker',
             broker='amqp://',
             backend='amqp://',
             )


app.config_from_object('django.conf:settings')
app.conf.update(
    CELERYBEAT_SCHEDULE={
        'update-query': {
            'task': 'distributors.tasks.update_queries',
            'schedule': timedelta(hours=24)
        },
    }
)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
