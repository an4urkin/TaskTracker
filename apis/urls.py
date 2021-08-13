from django.urls import path
from .import views
from rest_framework.routers import DefaultRouter




router = DefaultRouter()
router.register('', views.TaskTrackViewSet, basename='tasktracks')


urlpatterns = router.urls

# Obsolete
#
# [
    # path('', views.taskList, name="tasks"),
    # path('<int:pk>/', views.taskDetail, name="detail"),
    # path('create', views.taskCreate, name="create"),
    # path('update/<int:pk>/', views.taskUpdate, name="update"),
    # path('delete/<int:pk>/', views.taskDelete, name="delete"),
# ]
