import os
import django
django.setup()

from celery import Celery
from datetime import timedelta
from bot_api.models import AboutBot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

minute = AboutBot.objects.first().comment_request_time
# minute = 1

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
