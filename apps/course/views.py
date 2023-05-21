# Create your views here.
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.course.models import Course, CourseType
from utils.paginator import AppPageNumberPagination
from utils.queryset_filter import CourseFilter, CourseTypeFilter
from utils.response import JsonResponse
from utils.serializer import CourseSerializer, CourseTypeSerializer


@method_decorator(
    name='partial_update',
    decorator=swagger_auto_schema(
        tags=['课程相关接口'],
        operation_description="**更新某一条课程记录**"
    )
)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('id')
    serializer_class = CourseSerializer
    pagination_class = AppPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CourseFilter

    @swagger_auto_schema(
        tags=['课程相关接口'],
        operation_description="**查询课程列表**"
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=['课程相关接口'],
        operation_description="**创建一个课程**"
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=['课程相关接口'],
        operation_description="**查询某一个课程**"
    )
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=['课程相关接口'],
        operation_description="**更新某一条课程记录**"
    )
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=['课程相关接口'],
        operation_description="**删除某一个课程**"
    )
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return JsonResponse(data=response.data)


@method_decorator(
    name='partial_update',
    decorator=swagger_auto_schema(
        tags=['课程类别相关接口'],
        operation_description="**更新某一条课程类别记录**"
    )
)
class CourseTypeViewSet(viewsets.ModelViewSet):
    queryset = CourseType.objects.all().order_by('id')
    serializer_class = CourseTypeSerializer
    pagination_class = AppPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CourseTypeFilter

    @swagger_auto_schema(
        tags=['课程类别相关接口'],
        operation_description="**查询课程类别列表**"
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=['课程类别相关接口'],
        operation_description="**创建一个课程类别**"
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, args, kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=['课程类别相关接口'],
        operation_description="**查询某一个课程类别**"
    )
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, args, kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=['课程类别相关接口'],
        operation_description="**更新某一条课程类别记录**"
    )
    def update(self, request, *args, **kwargs):
        response = super().update(request, args, kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=['课程类别相关接口'],
        operation_description="**删除一个课程类别**"
    )
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, args, kwargs)
        return JsonResponse(data=response.data)
