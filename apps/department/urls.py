from django.urls import path, include
from rest_framework import routers

from apps.department.views import DepartmentViewSet

router = routers.DefaultRouter()
router.register('department', DepartmentViewSet)

urlpatterns = [
    path('data/', include(router.urls)),
]
