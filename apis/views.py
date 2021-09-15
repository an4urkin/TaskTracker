from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import pika

from apis import serializers as ser
from taskTracks.models import TaskTrack



def emit_notification(message):
    # for local ->'amqp://guest:guest@localhost:5672/%2F' // for docker -> 'amqp://guest:guest@rabbitmq:5672'
    params = pika.URLParameters('amqp://guest:guest@localhost:5672/%2F')
    connection = pika.BlockingConnection(params)  # pika.ConnectionParameters(host='localhost')
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    channel.basic_publish(
        exchange='logs',
        routing_key='',
        body=message
    )
    print(" [x] Sent %r" % message)
    connection.close()


class TaskTrackViewSet(viewsets.ModelViewSet):
    
    def retrieve(self, request, pk):
        queryset = TaskTrack.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        serializer = ser.ListTaskSerializer(task)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = ser.ListTaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            emit_notification("Task Created!")
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        queryset = TaskTrack.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        serializer = ser.UpdateTaskSerializer(task, data=request.data)
        if serializer.is_valid(raise_exception=True):
            emit_notification("Task Updated!")
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        queryset = TaskTrack.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        self.perform_destroy(task)
        emit_notification("Task Deleted!")
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    queryset = TaskTrack.objects.all()
    serializer_class = ser.ListTaskSerializer
    serializer_action_classes = {
        # 'retrieve': ser.ListTaskSerializer,
        'update': ser.UpdateTaskSerializer,
        # 'create': ser.CreateTaskSerializer,
        # 'destroy': ser.DeleteTaskSerializer
    }
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'priority', 'state', 'date']

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
    
