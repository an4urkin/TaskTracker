# Generated by Django 3.2.6 on 2021-10-11 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taskTracks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasktrack',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
