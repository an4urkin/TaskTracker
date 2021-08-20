from datetime import datetime, timedelta
from django.utils import timezone

from celery import shared_task
from celery.utils.log import get_task_logger
# from taskTracks import models


logger = get_task_logger(__name__)


# @shared_task
# def sample_task():
#     logger.info("The sample task just ran.")


# Delete rejected tasks

@shared_task
def delete_rejected_tasks():
    from taskTracks import models
    rejects = models.TaskTrack.objects.all()
    for task in rejects:
        expiration_date = task.date + timedelta(days=2)
        if expiration_date < timezone.now() and task.state == 'to_do':
            task.delete()
    logger.info("Deleted rejected tasks at {}".format(timezone.now()))
