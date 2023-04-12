from urllib.parse import urljoin

from django.conf import settings
from rest_framework import serializers

from apps.course.models import Course, CourseType
from apps.department.models import Department
from apps.privilege.models import Privilege
from apps.user.models import UserEntity
from apps.video.models import Video


class FileUrlField(serializers.CharField):
    """
    drf原生FileField的url序列化不满足要求
    重写对于url的序列化，使其支持根据设置的STATIC_SERVER和MEDIA_ROOT变化
    """

    def to_representation(self, value):
        if not value:
            return None

        static_server = settings.STATIC_SERVER
        media_root = settings.MEDIA_ROOT
        return urljoin(static_server, urljoin(media_root, value))


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    videoUrl = FileUrlField(label='videoUrl')

    class Meta:
        model = Video
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEntity
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class CourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseType
        fields = '__all__'


class PrivilegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Privilege
        fields = '__all__'
