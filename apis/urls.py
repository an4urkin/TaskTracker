from django.urls import path
from .import views
from rest_framework.routers import DefaultRouter

app_name = 'apis'
router = DefaultRouter()
router.register('', views.TaskTrackViewSet, basename='tasktracks')

urlpatterns = router.urls
