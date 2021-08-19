import datetime
from django.http import HttpResponse
from django.utils import timezone
from django.shortcuts import render
from rest_framework import viewsets, filters, generics
from taskTracks import models
from apis import serializers as ser
from .tasks import test_func


def test_view(request):
    test_func.delay()
    return HttpResponse("OK")


class TaskTrackViewSet(viewsets.ModelViewSet):
    queryset = models.TaskTrack.objects.all()
    serializer_class = ser.ListTaskSerializer
    serializer_action_classes = {
        'update': ser.UpdateTaskSerializer,
        'create': ser.CreateTaskSerializer
    }
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'priority', 'state', 'date']

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
