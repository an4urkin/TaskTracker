from django.shortcuts import render
from rest_framework import viewsets, filters
from taskTracks import models
from .serializers import TaskTrackSerializer


class TaskTrackViewSet(viewsets.ModelViewSet):
    queryset = models.TaskTrack.objects.all()
    serializer_class = TaskTrackSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id','priority','state','date']
    