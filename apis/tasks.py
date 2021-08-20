from datetime import timedelta
from django.utils import timezone

from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


# Delete rejected tasks from database

@shared_task
def delete_rejected_tasks():
    from taskTracks import models
    rejects = models.TaskTrack.objects.all()
    for task in rejects:
        expiration_date = task.date + timedelta(days=1)
        if expiration_date < timezone.now() and task.state == 'to_do':
            task.delete()
    logger.info("Deleted rejected tasks at {}".format(timezone.now()))
