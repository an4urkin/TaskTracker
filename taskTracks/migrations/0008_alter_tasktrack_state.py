# Generated by Django 3.2.6 on 2021-08-18 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskTracks', '0007_alter_tasktrack_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktrack',
            name='state',
            field=models.CharField(choices=[('to_do', 'ToDo'), ('ready', 'Ready'), ('in_pr', 'In Progress'), ('complt', 'Completed')], default='to_do', max_length=10),
        ),
    ]