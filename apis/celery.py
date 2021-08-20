from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('apis')
app.conf.enable_utc = False  # False for non-UTC region
app.conf.update(timezone='Europe/Kiev')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()
