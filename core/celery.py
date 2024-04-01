import os

from celery import Celery
from datetime import timedelta
from bot_api import models


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

minute = models.AboutBot.objects.first().comment_request_time

app.conf.beat_schedule = {
    f'send_push-every-{minute}-minute': {
        'task': 'celery_tasks.tasks.check_push',
        'schedule': timedelta(minutes=minute),
    },
    'create_backup_hourly': {
        'task': 'celery_tasks.tasks.create_backup',
        'schedule': timedelta(hours=1),
    },
}
