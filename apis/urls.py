from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .import views

app_name = 'apis'
router = DefaultRouter()
router.register(r'', views.TaskTrackViewSet, basename='tasklist')

urlpatterns = [
    re_path(r'^register/?$', views.RegistrationView.as_view(), name='user_registration'),
    re_path(r'^login/?$', views.LoginView.as_view(), name='user_login'),
    re_path(r'^users/?$', views.UserListView.as_view(), name='user_list'),
    re_path(r'^users/(?P<id>[^/]+)/$', views.UserDetailView.as_view(), name='user_detail'),
]
urlpatterns += router.urls
