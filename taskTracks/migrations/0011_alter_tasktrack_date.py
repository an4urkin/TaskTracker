# Generated by Django 3.2.6 on 2021-08-26 14:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskTracks', '0010_alter_tasktrack_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktrack',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 26, 14, 14, 43, 273646)),
        ),
    ]