from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicproject.settings')

# django.setup()

app = Celery('musicproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# Periodic task schedule
app.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'users.tasks.send_daily_email',
        'schedule': crontab(minute= 55, hour= 10),
    },
}
