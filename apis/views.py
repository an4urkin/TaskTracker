from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets, filters
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


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ser.ListUserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = User.objects.all()
    serializer_class = ser.ListPerUserSerializer
    permission_classes = [IsAdminUser]


class TaskTrackViewSet(viewsets.ModelViewSet):    

    # Custom filter to show only user-owned tasks
    class _IsStaffFilterBackend(filters.BaseFilterBackend):

        def filter_queryset(self, request, queryset, view):
            if request.user.is_staff == True:
                return queryset
            else:
                return queryset.filter(owner=request.user)

    
    queryset = TaskTrack.objects.all()
    filter_backends = (_IsStaffFilterBackend, filters.OrderingFilter)
    ordering_fields = ['id', 'priority', 'state', 'date']
    permission_classes = [IsAuthenticated]
    serializer_class = ser.ListTaskSerializer


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
        # queryset = TaskTrack.objects.all()
        queryset = self.get_queryset().filter(owner=request.user)
        task = get_object_or_404(queryset, pk=pk)
        serializer = ser.UpdateTaskSerializer(task, data=request.data) # self.serializer_class(task, data=request.data) 

        if request.user.is_staff == False:
            if request.data.get("state") == "complt" or request.data.get("name") or request.data.get("priority"):

                return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                if serializer.is_valid(raise_exception=True):
                    emit_notification('Task Updated!')
        
                self.perform_update(serializer)

                return Response(serializer.data)
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
    