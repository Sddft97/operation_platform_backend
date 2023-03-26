from django_filters import rest_framework as filters

from apps.course.models import Course, CourseType
from apps.department.models import Department
from apps.privilege.models import Privilege
from apps.user.models import UserEntity
from apps.video.models import Video


class VideoFilter(filters.FilterSet):
    videoName_like = filters.CharFilter(field_name='videoName', lookup_expr='contains')
    createdAt_lte = filters.DateTimeFilter(field_name='createdAt', lookup_expr='lte')
    createdAt_gte = filters.DateTimeFilter(field_name='createdAt', lookup_expr='gte')
    lastViewedAt_lte = filters.DateTimeFilter(field_name='lastViewedAt', lookup_expr='lte')
    lastViewedAt_gte = filters.DateTimeFilter(field_name='lastViewedAt', lookup_expr='gte')

    class Meta:
        model = Video
        fields = [
            'id',
            'videoId',
            'courseId',
        ]


class CourseFilter(filters.FilterSet):
    courseName_like = filters.CharFilter(field_name='courseName', lookup_expr='contains')

    class Meta:
        model = Course
        fields = [
            'id',
            'courseId',
            'courseTypeId',
            'deptCode'
        ]


class CourseTypeFilter(filters.FilterSet):
    name_like = filters.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = CourseType
        fields = [
            'id'
        ]


class DepartmentFilter(filters.FilterSet):
    deptName_like = filters.CharFilter(field_name='deptName', lookup_expr='contains')

    class Meta:
        model = Department
        fields = [
            'id',
            'deptCode'
        ]


class PrivilegeFilter(filters.FilterSet):
    class Meta:
        model = Privilege
        fields = [
            'id',
            'privilegeCode'
        ]


class UserFilter(filters.FilterSet):
    username_like = filters.CharFilter(field_name='username', lookup_expr='contains')

    class Meta:
        model = UserEntity
        fields = [
            'id',
            'uid',
            'email',
            'sex',
            'privCode',
            'deptCode',
            'phoneNumber'
        ]
