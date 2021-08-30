from rest_framework import serializers
from taskTracks import models


class ListTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskTrack
        fields = '__all__'


class UpdateTaskSerializer(serializers.Serializer):
    description = serializers.CharField(required=True)
    state = serializers.ChoiceField(choices=models.TaskTrack.States, required=True)


class CreateTaskSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    date = serializers.DateTimeField(required=True)
    state = serializers.ChoiceField(choices=models.TaskTrack.States, required=True)
    priority = serializers.ChoiceField(choices=models.TaskTrack.Priorities, required=True)
