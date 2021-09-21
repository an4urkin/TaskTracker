import pika
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.response import Response


from apis import serializers as ser
from taskTracks.models import TaskTrack



def emit_notification(message):

    cred = pika.PlainCredentials('guest', 'guest')
    params = pika.ConnectionParameters(
        host='localhost', # for local -> 'localhost' || for docker -> 'rabbitmq'
        port=5672,
        virtual_host='/',
        credentials=cred
    )
    connection = pika.BlockingConnection(params)
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
            try:
                emit_notification("Task Created!")
            except:
                pass
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        queryset = TaskTrack.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        serializer = ser.UpdateTaskSerializer(task, data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                emit_notification("Task Updated!")
            except:
                pass
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        queryset = TaskTrack.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        self.perform_destroy(task)
        try:
            emit_notification("Task Deleted!")
        except:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    queryset = TaskTrack.objects.all()
    serializer_class = ser.ListTaskSerializer
    serializer_action_classes = {
        # 'retrieve': ser.ListTaskSerializer,
        'update': ser.UpdateTaskSerializer,
        # 'create': ser.CreateTaskSerializer
    }
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'priority', 'state', 'date']

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
    
