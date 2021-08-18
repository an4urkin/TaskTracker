from celery.schedules import crontab
from celery import shared_task
from django.utils import timezone
from taskTracks import models


@shared_task(bind=True)
def test_func():
    for item in range(10):
        print(item)
    return "OK"

# Doesn't work - needs fix, celery.task - deprecated

# @periodic_task(run_every=crontab(minute='*/5'))
# def delete_rejected_tasks():
#     query = models.TaskTrack.objects.all()
#     for task in query:
#         expiration_date = task.date + datetime.timedelta(days=2)
#         if expiration_date < timezone.now():
#             task.delete()
#     return "Deleted rejected tasks at {}".format(timezone.now())
