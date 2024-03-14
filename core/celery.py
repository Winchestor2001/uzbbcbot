import os

from celery import Celery
from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

minute = 1

app.conf.beat_schedule = {
    f'send_push-every-{minute}-minute': {
        'task': 'celery_tasks.tasks.check_push',
        'schedule': timedelta(minutes=minute),
    }
}
