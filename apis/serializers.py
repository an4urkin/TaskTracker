from rest_framework import serializers
from taskTracks import models


class TaskTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskTrack
        fields = '__all__'
