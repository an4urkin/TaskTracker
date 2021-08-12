from django.shortcuts import render

from rest_framework import generics, viewsets

from taskTracks import models
from .serializers import TaskTrackSerializer


class TaskTrackViewSet(viewsets.ModelViewSet):
    queryset = models.TaskTrack.objects.all()
    serializer_class = TaskTrackSerializer


# Obsolete: sepearate classes, replaced by viewset
#
#
# class ListTaskTrack(generics.ListCreateAPIView):
    # queryset = models.TaskTrack.objects.all()
    # serializer_class = TaskTrackSerializer


# class DetailTaskTrack(generics.RetrieveUpdateDestroyAPIView):
    # queryset = models.TaskTrack.objects.all()
    # serializer_class = TaskTrackSerializer
