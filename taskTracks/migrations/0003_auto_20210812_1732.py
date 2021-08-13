# Generated by Django 3.2.6 on 2021-08-12 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskTracks', '0002_auto_20210812_1707'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tasktrack',
            old_name='title',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='tasktrack',
            name='deadline',
        ),
        migrations.AddField(
            model_name='tasktrack',
            name='date',
            field=models.DateField(blank=True, editable=False, null=True, verbose_name='date'),
        ),
    ]