import factory
import random
from django.utils import timezone

from taskTracks.models import TaskTrack


factory.Faker._DEFAULT_LOCALE = 'en_US'

class TaskTrackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskTrack
    
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    date = factory.LazyFunction(timezone.now)
    state = random.choice(TaskTrack.States.choices)
    priority = random.choice(TaskTrack.Priorities.choices)
