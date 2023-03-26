from django.urls import path, include
from rest_framework import routers

from apps.video.views import VideoViewSet

router = routers.DefaultRouter()
router.register('video', VideoViewSet)

urlpatterns = [
    path('data/', include(router.urls)),
]
