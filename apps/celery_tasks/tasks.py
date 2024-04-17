from __future__ import absolute_import, unicode_literals
from celery import shared_task
import logging
from .models import NotifyTasks, ServiceStuff, ProductDetail
from .utils import send_message_to_user
from subprocess import run


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] | %(levelname)s: %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)


@shared_task()
def check_push():
    users = NotifyTasks.objects.all()
    for user in users:
        if user.type == 'service':
            data = ServiceStuff.objects.get(id=user.receiver)
        else:
            data = ProductDetail.objects.get(id=user.receiver)
        send_message_to_user(user=user, lang=user.user.language, receiver=data, datatype=user.type)
    return "Task completed successfully"


@shared_task
def create_backup():
    run(['python', 'manage.py', 'dumpdata', '>', 'backup.json'])
    return "Backup created successfully"