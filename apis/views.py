from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView


from apis import serializers as ser
from taskTracks.models import TaskTrack, User
from apis.emit_notification import emit_notification


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


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ser.ListPerUserSerializer

    def get(self, request):
        user = User.objects.all()
        serializer = self.serializer_class(user, many=True)
        
        return Response(serializer.data)
    
    def put(self, request, pk):
        queryset = TaskTrack.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        serializer = ser.UpdateTaskSerializer(task, data=request.data)

        if serializer.is_valid(raise_exception=True):
            emit_notification('Task Updated!')
        
        self.perform_update(serializer)
        username = request.user.username
        print(' [x] Author - user: %r' % username)


class TaskTrackViewSet(viewsets.ModelViewSet):
    queryset = TaskTrack.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ser.ListTaskSerializer
    serializer_action_classes = {
        'update': ser.UpdateTaskSerializer,
        # 'retrieve': ser.ListTaskSerializer,
        # 'create': ser.CreateTaskSerializer
    }
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'priority', 'state', 'date']

    def retrieve(self, request, pk):
        queryset = TaskTrack.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        serializer = ser.ListTaskSerializer(task)
        username = request.user.username
        print(' [x] Author - user: %r' % username)
        
        return Response(serializer.data)
    
    def create(self, request):
        serializer = ser.ListTaskSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            emit_notification('Task Created!')
        
        self.perform_create(serializer)
        username = request.user.username
        print(' [x] Author - user: %r' % username)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        queryset = TaskTrack.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        serializer = ser.UpdateTaskSerializer(task, data=request.data)

        if serializer.is_valid(raise_exception=True):
            emit_notification('Task Updated!')
        
        self.perform_update(serializer)
        username = request.user.username
        print(' [x] Author - user: %r' % username)
        
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        queryset = TaskTrack.objects.all()
        task = get_object_or_404(queryset, pk=pk)
        self.perform_destroy(task)
        emit_notification('Task Deleted!')
        username = request.user.username
        print(' [x] Author - user: %r' % username)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        
        except (KeyError, AttributeError):
            return super().get_serializer_class()
    