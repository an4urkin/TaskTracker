from celery.schedules import crontab
# from celery.task import periodic_task
from django.utils import timezone
from taskTracks import models

# Doesn't work - needs fix, celery.task - deprecated

# @periodic_task(run_every=crontab(minute='*/5'))
def delete_rejected_tasks():
    query = models.TaskTrack.objects.all()
    for task in query:
        expiration_date = task.date + datetime.timedelta(days=2)
        if expiration_date < timezone.now():
            task.delete()
    return "Deleted rejected tasks at {}".format(timezone.now())