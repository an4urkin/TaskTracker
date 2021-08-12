from rest_framework import serializers
from taskTracks import models


class TaskTrackSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'description',
            'date',
            'state',
            'priority',
        )
        model = models.TaskTrack