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

BROKER_URL = 'redis://h:pd953bcb2d78af604e9ec029d369e5d2708f4a805f271693b393e34ddf78af2eb@ec2-54-83-245-251.compute-1.amazonaws.com:32119'

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
