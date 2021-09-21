from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import threading
import pika
import os

from taskTracks.models import TaskTrack


class ListTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTrack
        fields = '__all__'


class UpdateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTrack
        fields = ['description', 'state']


"""Obsolete - will be removed later"""
# class CreateTaskSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(required=True)
#     description = serializers.CharField(required=True)
#     # date = serializers.DateTimeField()
#     state = serializers.ChoiceField(choices=models.TaskTrack.States, required=True)
#     priority = serializers.ChoiceField(choices=models.TaskTrack.Priorities, required=True)

#     class Meta:
#         model = models.TaskTrack
#         fields = '__all__'
#         read_only_fields = ['id']

#     def is_valid(self, raise_exception=False):
#         valid = super(CreateTaskSerializer, self).is_valid()
#         if valid:
#             # emit_notification("Task created!")
#             return True
#         else:
#             return False
