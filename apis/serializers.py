from rest_framework import serializers
from taskTracks import models
from rest_framework.exceptions import ValidationError
import pika


def emit_notification(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    channel.basic_publish(
        exchange='logs',
        routing_key='',
        body=message
    )
    # print(" [x] Sent %r" % message)
    connection.close()


class ListTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskTrack
        fields = '__all__'


class DeleteTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TaskTrack
        fields = '__all__'
        emit_notification("Task deleted!")


class UpdateTaskSerializer(serializers.ModelSerializer):
    state = serializers.ChoiceField(choices=models.TaskTrack.States, required=True)

    class Meta:
        model = models.TaskTrack
        fields = ['description', 'state']

    def is_valid(self, raise_exception=False):
        valid = super(UpdateTaskSerializer, self).is_valid()
        if valid:
            emit_notification("Task updated!")
            return True
        else:
            if self._errors:
                if raise_exception:
                    raise ValidationError(self.errors)
            return False


class CreateTaskSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    date = serializers.DateTimeField(required=True)
    state = serializers.ChoiceField(choices=models.TaskTrack.States, required=True)
    priority = serializers.ChoiceField(choices=models.TaskTrack.Priorities, required=True)

    class Meta:
        model = models.TaskTrack
        fields = '__all__'
        read_only_fields = ['id']

    def is_valid(self, raise_exception=False):
        valid = super(CreateTaskSerializer, self).is_valid()
        if valid:
            emit_notification("Task created!")
            return True
        else:
            return False
