import datetime
from django.utils import timezone
from django.shortcuts import render
from rest_framework import viewsets, filters, generics
from taskTracks import models
from .serializers import ListTaskSerializer, UpdateTaskSerializer, CreateTaskSerializer


class TaskTrackViewSet(viewsets.ModelViewSet):
    queryset = models.TaskTrack.objects.all()
    serializer_class = ListTaskSerializer
    serializer_action_classes = {
        'update': UpdateTaskSerializer,
        'create': CreateTaskSerializer
    }
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id','priority','state','date']


    def get_serializer_class(self):
       try:
           return self.serializer_action_classes[self.action]
       except (KeyError, AttributeError):
           return super().get_serializer_class()
