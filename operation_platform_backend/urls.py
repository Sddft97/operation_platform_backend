"""operation_platform_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from apps.course.urls import urlpatterns as course_urls
from apps.department.urls import urlpatterns as department_urls
from apps.privilege.urls import urlpatterns as privilege_urls
from apps.user.urls import urlpatterns as user_urls
from apps.video.urls import urlpatterns as video_urls
from utils.exception_handler import http404handler, http500handler

API_PREFIX = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_PREFIX, include(video_urls)),
    path(API_PREFIX, include(user_urls)),
    path(API_PREFIX, include(privilege_urls)),
    path(API_PREFIX, include(course_urls)),
    path(API_PREFIX, include(department_urls)),
]

handler404 = http404handler
handler500 = http500handler
