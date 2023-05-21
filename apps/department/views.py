# Create your views here.
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.department.models import Department
from utils.paginator import AppPageNumberPagination
from utils.queryset_filter import DepartmentFilter
from utils.response import JsonResponse
from utils.serializer import DepartmentSerializer


@method_decorator(
    name='partial_update',
    decorator=swagger_auto_schema(
        tags=['部门相关接口'],
        operation_description="**更新某一条部门记录**"
    )
)
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('id')
    serializer_class = DepartmentSerializer
    pagination_class = AppPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = DepartmentFilter

    @swagger_auto_schema(
        tags=['部门相关接口'],
        operation_description='**查询部门列表**'
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=['部门相关接口'],
        operation_description="**创建一个部门**"
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=['部门相关接口'],
        operation_description="**查询某一个部门**"
    )
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=['部门相关接口'],
        operation_description="**更新某一条部门记录**"
    )
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=['部门相关接口'],
        operation_description="**删除一个部门**"
    )
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return JsonResponse(data=response.data)
