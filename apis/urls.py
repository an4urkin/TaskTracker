from django.urls import path
from .import views
from rest_framework.routers import DefaultRouter


# Replaced by separate URLs, may be changed later
#
# router = DefaultRouter()
# router.register('', TaskTrackViewSet, basename='tasktracks')


urlpatterns = [
    path('', views.taskList, name="tasks"),
    path('detail/<int:pk>/', views.taskDetail, name="detail"),
    path('create', views.taskCreate, name="create"),
    path('update/<int:pk>/', views.taskUpdate, name="update"),
    path('delete/<int:pk>/', views.taskDelete, name="delete"),
]
# router.urls      Replaced by separate URLs, may be changed later
