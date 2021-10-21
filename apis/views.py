from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView


from apis import serializers as ser
from taskTracks.models import TaskTrack, User
from apis.emit_notification import emit_notification


# Custom filter to show only user-owned tasks
class IsStaffFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if request.user.is_staff == True:
            return queryset
        else:
            return queryset.filter(owner=request.user)


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ser.RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'token': serializer.data.get('token', None),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ser.LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# class UserView(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = ser.ListPerUserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ser.ListUserSerializer


class TaskTrackViewSet(viewsets.ModelViewSet):
    queryset = TaskTrack.objects.all()
    filter_backends = (IsStaffFilterBackend, filters.OrderingFilter)
    ordering_fields = ['id', 'priority', 'state', 'date']
    permission_classes = [IsAuthenticated]
    serializer_class = ser.ListTaskSerializer
    # serializer_action_classes = {
    #     'update': ser.UpdateTaskSerializer,
    # }

    # def get_serializer_class(self):
    #     try:
    #         return self.serializer_action_classes[self.action]
        
    #     except (KeyError, AttributeError):
    #         return super().get_serializer_class()

    # def retrieve(self, request, pk):
    #     queryset = TaskTrack.objects.all()
    #     task = get_object_or_404(queryset, pk=pk)
    #     serializer = ser.ListTaskSerializer(task)
    #     username = request.user.username
    #     print(' [x] Author - user: %r' % username)
        
    #     return Response(serializer.data)
    
    def create(self, request):
        if request.user.is_staff == True:
            serializer = self.serializer_class(data=request.data) # ser.ListTaskSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                emit_notification('Task Created!')
        
            self.perform_create(serializer)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, pk):
        queryset = TaskTrack.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(task, data=request.data) # ser.ListTaskSerializer(task, data=request.data)

        if request.user.is_staff == False and request.data.get("state") == "complt":
            return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        else:
            if serializer.is_valid(raise_exception=True):
                emit_notification('Task Updated!')
        
            self.perform_update(serializer)

            return Response(serializer.data)
    
    def destroy(self, request, pk):
        if request.user.is_staff == True:            
            queryset = TaskTrack.objects.all()
            task = get_object_or_404(queryset, pk=pk)
            self.perform_destroy(task)
            emit_notification('Task Deleted!')
        
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:  
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    