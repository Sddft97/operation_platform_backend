# Create your views here.
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.privilege.models import Privilege
from utils.paginator import AppPageNumberPagination
from utils.queryset_filter import PrivilegeFilter
from utils.response import JsonResponse
from utils.serializer import PrivilegeSerializer


@method_decorator(
    name='partial_update',
    decorator=swagger_auto_schema(
        tags=['权限相关接口'],
        operation_description="**更新某一条权限记录**"
    )
)
class PrivilegeViewSet(viewsets.ModelViewSet):
    queryset = Privilege.objects.all().order_by('id')
    serializer_class = PrivilegeSerializer
    pagination_class = AppPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PrivilegeFilter

    @swagger_auto_schema(
        tags=['权限相关接口'],
        operation_description="**查询权限列表**"
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=['权限相关接口'],
        operation_description="**创建一条新的权限**"
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=['权限相关接口'],
        operation_description="**查询某一条权限记录**"
    )
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=['权限相关接口'],
        operation_description="**更新某一条权限记录**"
    )
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=['权限相关接口'],
        operation_description="**删除某一条权限记录**"
    )
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, args, kwargs)
        return JsonResponse(data=response.data)
