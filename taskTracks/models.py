from django.db import models
from django.utils.translation import ugettext_lazy as _


class TaskTrack(models.Model):
    
    class States(models.TextChoices):
        TODO = 'todo', _('ToDo')
        READY = 'ready', _('Ready')
        INPROGRESS = 'in_pr', _('In Progress')
        COMPLETED = 'compl', _('Completed')
    
    
    class Priorities(models.TextChoices):
        LOW = 'low', _('Low')
        MEDIUM = 'med', _('Medium')
        HIGH = 'high', _('High')
        BLOCKING = 'block', _('Blocking')
    
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField(null=True, blank=True)
    state = models.CharField(
        max_length=5,
        choices=States.choices,
        default=States.TODO,
    )
    priority = models.CharField(
        max_length=5,
        choices=Priorities.choices,
        default=Priorities.MEDIUM,
    )
    
    
    def __str__(self):
        return self.name
