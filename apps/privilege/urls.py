from django.urls import path, include
from rest_framework import routers

from apps.privilege.views import PrivilegeViewSet

router = routers.DefaultRouter()
router.register('privilege', PrivilegeViewSet)

urlpatterns = [
    path('data/', include(router.urls)),
]
