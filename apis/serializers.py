from rest_framework import serializers
from taskTracks import models


class ListTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskTrack
        fields = '__all__'


class UpdateTaskSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(choices=models.TaskTrack.States, required=True)
    class Meta:
        model = models.TaskTrack
        fields = ['description', 'state']
        read_only_fields = ['name', 'date', 'priority']


class CreateTaskSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    date = serializers.CharField(required=True)
    state = serializers.ChoiceField(choices=models.TaskTrack.States, required=True)
    priority = serializers.ChoiceField(choices=models.TaskTrack.Priorities, required=True)
    class Meta:
        model = models.TaskTrack
        fields = ['id','name','description','date','state','priority']
