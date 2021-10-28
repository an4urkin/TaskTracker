import factory
import random
from django.utils import timezone
from taskTracks.models import TaskTrack, User

factory.Faker._DEFAULT_LOCALE = 'en_US'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Faker('name')
    email = factory.Faker('free_email')
    password = factory.Faker('bothify', text='????####')
    is_staff =  factory.Faker('pybool')
    is_active = factory.Faker('pybool')


class TaskTrackFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskTrack
    
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    date = factory.LazyFunction(timezone.now)
    state = random.choice(TaskTrack.States.choices)
    priority = random.choice(TaskTrack.Priorities.choices)
    owner = factory.Iterator(User.objects.all())

