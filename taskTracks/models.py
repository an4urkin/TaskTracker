from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class TaskTrack(models.Model):
    class States(models.TextChoices):
        TODO = 'to_do', _('ToDo')
        READY = 'ready', _('Ready')
        INPROGRESS = 'in_pr', _('InProgress')
        COMPLETED = 'complt', _('Completed')

    class Priorities(models.TextChoices):
        LOW = '0_low', _('Low')
        MEDIUM = '1_med', _('Medium')
        HIGH = '2_high', _('High')
        BLOCKING = '3_block', _('Blocking')

    name = models.TextField()
    description = models.TextField()
    date = models.DateTimeField(default=timezone.now, editable=False)
    state = models.TextField(
        choices=States.choices,
        default=States.TODO,
    )
    priority = models.TextField(
        choices=Priorities.choices,
        default=Priorities.MEDIUM,
    )

    def __str__(self):
        return self.name
