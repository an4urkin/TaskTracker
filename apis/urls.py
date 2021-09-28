# from django.urls import path
from rest_framework.routers import DefaultRouter

from .import views

app_name = 'apis'
router = DefaultRouter()
router.register('', views.TaskTrackViewSet, basename='tasktracks')

urlpatterns = router.urls
