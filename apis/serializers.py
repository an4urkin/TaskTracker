from rest_framework import serializers
from taskTracks import models


class ListTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskTrack
        fields = '__all__'


class UpdateTaskSerializer(serializers.ModelSerializer):
    state = serializers.CharField(required=True)
    class Meta:
        model = models.TaskTrack
        fields = ['description', 'state']

    def get_validation_exclusions(self):
        exclusions = super(UpdateTaskSerializer, self).get_validation_exclusions()
        return exclusions + ['state']


class CreateTaskSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    date = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    priority = serializers.CharField(required=True)
    class Meta:
        model = models.TaskTrack
        fields = ['id','name','description','date','state','priority']

    def get_validation_exclusions(self):
        exclusions = super(CreateTaskSerializer, self).get_validation_exclusions()
        return exclusions + ['name','description','date','state','priority']
