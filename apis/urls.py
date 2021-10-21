from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .import views

app_name = 'apis'
router = DefaultRouter()
router.register('', views.TaskTrackViewSet, basename='tasklist')
router.register(r'users', views.UserViewSet, basename='userlist')

urlpatterns = [
    re_path(r'^register/?$', views.RegistrationView.as_view(), name='user_registration'),
    re_path(r'^login/?$', views.LoginView.as_view(), name='user_login'),
    # re_path(r'^users/?$', views.UserView.as_view(), name='user_tasklist'),
    path('', include(router.urls)),
]
# urlpatterns = router.urls
