from django.apps import AppConfig
from django.db.models.signals import post_init, post_save, post_delete
from .tasks import notify_task_created, notify_task_updated, notify_task_deleted


class ApisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apis'

    # def ready(self):
    #     post_init.connect(notify_task_created)
    #     post_save.connect(notify_task_updated)
    #     post_delete.connect(notify_task_deleted)
