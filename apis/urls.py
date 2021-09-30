# from django.urls import path
import rest_framework
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .import views

app_name = 'apis'
router = DefaultRouter()
router.register('', views.TaskTrackViewSet, basename='tasktracks')

urlpatterns = [
    re_path(r'^registration/?$', views.RegistrationView.as_view(), name='user_registration'),
    re_path(r'^login/?$', views.LoginView.as_view(), name='user_login'),
    path('', include(router.urls)),
]
# urlpatterns = router.urls
