import os
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
    重写对于url的序列化，使其支持根据设置的STATIC_SERVER变化
    """

    def to_representation(self, value):
        if not value:
            return None

        value_ = value.replace(os.sep, "/")  # 将url中的路径分隔符统一替换

        static_server = settings.STATIC_SERVER
        return urljoin(static_server, value_)


class StringListField(serializers.CharField):
    """
    将数据库中形如 'param1,param2,param3' 的字符串转为List
    """

    def to_representation(self, value):
        return [token.strip() for token in value.split(",")]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    videoUrl = FileUrlField(label='videoUrl')
    coverImgUrl = FileUrlField(label='coverImgUrl')
    resolutionVersion = StringListField(label='resolutionVersion', required=False, allow_null=True, allow_blank=True)

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
