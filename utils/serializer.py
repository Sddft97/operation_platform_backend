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
        extra_kwargs = {
            'id': {
                'label': '数据库主键id',
                'help_text': '数据库主键id，为满足数据库约束而存在，具有唯一性'
            },
            'courseId': {
                'label': '课程id',
                'help_text': '代表一个课程，具有唯一性'
            },
            'courseName': {
                'label': '课程名',
                'help_text': '课程名称，人类可读'
            },
            'courseDescription': {
                'label': '课程介绍',
                'help_text': '对本课程的介绍信息'
            },
            'courseCoverUrl': {
                'label': '课程封面地址',
                'help_text': '展示课程时使用的封面'
            },
            'courseTypeId': {
                'label': '课程类别id',
                'help_text': '标识课程属于哪个类别，与CourseType表有关'
            },
            'deptCode': {
                'label': '部门id',
                'help_text': '标识课程属于哪个部门，与Department表有关'
            }
        }


class VideoSerializer(serializers.ModelSerializer):
    videoUrl = FileUrlField(label='视频地址', help_text='不能直接使用，需要配合nginx之类进行反向代理')
    coverImgUrl = FileUrlField(label='视频封面图片的地址', help_text='不能直接使用，需要配合nginx之类进行反向代理')
    resolutionVersion = StringListField(label='视频支持的分辨率', required=False, allow_null=True, allow_blank=True,
                                        help_text='列表格式')

    class Meta:
        model = Video
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'label': '数据库主键id',
                'help_text': '数据库主键id，为满足数据库约束而存在，具有唯一性'
            },
            'videoId': {
                'label': '视频id',
                'help_text': '视频id，具有唯一性，业务上更常用，也更具有解释性'
            },
            'videoName': {
                'label': '视频名称',
                'help_text': '视频名称'
            },
            'createdAt': {
                'label': '视频创建时间',
                'help_text': '视频创建时间，添加记录时自动创建'
            },
            'lastModifiedAt': {
                'label': '视频最近修改时间',
                'help_text': '视频最近修改时间，修改记录时自动更新'
            },
            'courseId': {
                'label': '课程id',
                'help_text': '视频所属的课程id'
            },
            'status': {
                'label': '视频所处状态',
                'help_text': """
                    视频目前的状态，有以下几种可选值：
                    - 0: 未知状态
                    - 1: 正在上传中
                    - 2: 正在转码处理中
                    - 3: 准备就绪
                """
            }
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEntity
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'label': '数据库主键id',
                'help_text': '数据库主键id，为满足数据库约束而存在，具有唯一性'
            },
            'uid': {
                'label': '用户id',
                'help_text': '视频id，具有唯一性，业务上更常用'
            },
            'avatar': {
                'label': '用户头像图片地址',
                'help_text': '用户头像图片地址'
            },
            'email': {
                'label': '用户电子邮箱地址',
                'help_text': '用户电子邮箱地址'
            },
            'username': {
                'label': '用户名',
                'help_text': '用户名'
            },
            'sex': {
                'label': '用户性别',
                'help_text': '用户性别'
            },
            'privCode': {
                'label': '用户权限id',
                'help_text': '描述用户所具有的权限，与Privilege表相关'
            },
            'deptCode': {
                'label': '用户所属部门id',
                'help_text': '描述用户所属部门信息，与Department表相关'
            },
            'phoneNumber': {
                'label': '用户电话号码',
                'help_text': '用户电话号码'
            }
        }


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'label': '数据库主键id',
                'help_text': '数据库主键id，为满足数据库约束而存在，具有唯一性'
            },
            'deptCode': {
                'label': '部门编号',
                'help_text': '代表一个部门，具有唯一性'
            },
            'deptName': {
                'label': '部门名称',
                'help_text': '具有唯一性，用于展示，是人类可读的名称'
            }
        }


class CourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseType
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'label': '数据库主键id',
                'help_text': '数据库主键id，为满足数据库约束而存在，具有唯一性'
            },
            'name': {
                'label': '课程类别名',
                'help_text': '代表一个课程，具有唯一性，人类可读'
            },
            'label': {
                'label': '课程类别标签',
                'help_text': '用于展示课程类别，人类可读。一般情况下与name保持一致即可'
            }
        }


class PrivilegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Privilege
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'label': '数据库主键id',
                'help_text': '数据库主键id，为满足数据库约束而存在，具有唯一性'
            },
            'privilegeCode': {
                'label': '权限码',
                'help_text': '具有唯一性，代表一种权限'
            },
            'privilegeName': {
                'label': '权限名',
                'help_text': '具有唯一性，用于展示，是人类可读的名称'
            }
        }
