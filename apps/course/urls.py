from django.urls import path, include
from rest_framework import routers

from apps.course.views import CourseViewSet, CourseTypeViewSet

router = routers.DefaultRouter()
router.register('course', CourseViewSet)
router.register('courseType', CourseTypeViewSet)

urlpatterns = [
    path('data/', include(router.urls)),
]
