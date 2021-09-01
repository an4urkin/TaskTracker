from rest_framework import viewsets, filters
from rest_framework.decorators import action
from taskTracks import models
from apis import serializers as ser


class TaskTrackViewSet(viewsets.ModelViewSet):
    queryset = models.TaskTrack.objects.all()
    serializer_class = ser.ListTaskSerializer
    serializer_action_classes = {
        'update': ser.UpdateTaskSerializer,
        'create': ser.CreateTaskSerializer,
        'destroy': ser.DeleteTaskSerializer
    }
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'priority', 'state', 'date']

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
