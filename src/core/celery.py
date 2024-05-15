import os
from django.conf import settings
import django

from celery import Celery
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

django.setup()
from bot_api.models import AboutBot
try:
    minute = AboutBot.objects.first().comment_request_time
except:
    minute = 1

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
