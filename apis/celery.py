from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('apis')
app.conf.enable_utc = False  # False for non-UTC region
app.conf.update(timezone='Europe/Kiev')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat settings - will add later

app.autodiscover_tasks()


@app.task(bind=True)
def test_task(self):
    print(f'Request: {self.Request!r}')
