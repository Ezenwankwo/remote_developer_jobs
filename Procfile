web: gunicorn remotejobs.wsgi
worker: celery -A remotejobs worker -l info -P gevent
