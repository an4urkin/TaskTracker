# Generated by Django 3.2.6 on 2021-08-12 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskTracks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasktrack',
            name='deadline',
            field=models.DateField(blank=True, null=True, verbose_name='deadline'),
        ),
        migrations.AddField(
            model_name='tasktrack',
            name='priority',
            field=models.CharField(choices=[('low', 'Low'), ('med', 'Medium'), ('high', 'High'), ('block', 'Blocking')], default='med', max_length=5),
        ),
        migrations.AddField(
            model_name='tasktrack',
            name='state',
            field=models.CharField(choices=[('todo', 'ToDo'), ('ready', 'Ready'), ('in_pr', 'In Progress'), ('compl', 'Completed')], default='todo', max_length=5),
        ),
    ]