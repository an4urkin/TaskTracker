from django.urls import path

from .views import TaskTrackViewSet #ListTaskTrack, DetailTaskTrack     Obsolete: replaced by viewset
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', TaskTrackViewSet, basename='tasktracks')
urlpatterns = router.urls

#Obsolete: replaced by viewset
#
# [
    # path('', ListTaskTrack.as_view()),
    # path('<int:pk>/', DetailTaskTrack.as_view()),
# ]