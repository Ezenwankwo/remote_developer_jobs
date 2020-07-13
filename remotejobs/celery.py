from __future__ import absolute_import, unicode_literals

import os
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'remotejobs.settings')

app = Celery('remotejobs')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

BROKER_URL = 'redis://h:p219083464fdfc06e43fe3e5ee9af1374c342e5497b6f00db10e15209cd04e1d9@ec2-34-236-54-188.compute-1.amazonaws.com:19199'

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
