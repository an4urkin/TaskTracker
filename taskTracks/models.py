import jwt

from datetime import timedelta
from django.utils import timezone

from django.conf import settings
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _



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


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Указанное имя пользователя должно быть установлено')

        if not email:
            raise ValueError('Данный адрес электронной почты должен быть установлен')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False
        )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = UserManager()
