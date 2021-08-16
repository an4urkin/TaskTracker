from rest_framework import serializers
from taskTracks import models


class TaskTrackSerializer(serializers.ModelSerializer):
    date = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    priority = serializers.CharField(required=True)
    class Meta:
        model = models.TaskTrack
        fields = '__all__'

    def get_validation_exclusions(self):
        exclusions = super(TaskTrackSerializer, self).get_validation_exclusions()
        return exclusions + ['date','state','priority']


class UpdateTaskSerializer(serializers.ModelSerializer):
    state = serializers.CharField(required=True)
    class Meta:
        model = models.TaskTrack
        fields = ['description', 'state']

    def get_validation_exclusions(self):
        exclusions = super(UpdateTaskSerializer, self).get_validation_exclusions()
        return exclusions + ['state']

