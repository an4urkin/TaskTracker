from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


# Set default Django settings os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('apis')

# Celery will apply all configuration keys with defined namespace  app.config_from_object('django.conf:settings', namespace='CELERY')
# Load tasks from all registered apps
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)