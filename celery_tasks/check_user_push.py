from __future__ import absolute_import, unicode_literals
from celery import shared_task
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] | %(levelname)s: %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)


@shared_task()
def check_push():
    return "Task completed successfully"
