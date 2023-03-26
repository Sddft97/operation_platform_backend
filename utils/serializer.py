from rest_framework import serializers

from apps.course.models import Course, CourseType
from apps.department.models import Department
from apps.privilege.models import Privilege
from apps.user.models import UserEntity
from apps.video.models import Video


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
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
