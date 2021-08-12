from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from taskTracks import models
from .serializers import TaskTrackSerializer

# Replaced by separate views, may be changed later
#
# class TaskTrackViewSet(viewsets.ModelViewSet):
    # queryset = models.TaskTrack.objects.all()
    # serializer_class = TaskTrackSerializer


@api_view(['GET'])
def taskList(request):
    tasks = models.TaskTrack.objects.all()
    serializer = TaskTrackSerializer(tasks, many=True)
    return Response(serializer.data)
    
    
@api_view(['GET'])
def taskDetail(request, pk):
    tasks = models.TaskTrack.objects.filter(id=pk)
    serializer = TaskTrackSerializer(tasks, many=True)
    return Response(serializer.data)
    
    
@api_view(['POST'])
def taskCreate(request):
    serializer = TaskTrackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
    
    
@api_view(['POST'])
def taskUpdate(request, pk):
    task = models.TaskTrack.objects.filter(id=pk)
    serializer = TaskTrackSerializer(instace=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
    
    
@api_view(['DELETE'])
def taskDelete(request, pk):
    task = TaskTrack.objects.filter(id=pk)
    task.delete()
    return Response('Deleted')
