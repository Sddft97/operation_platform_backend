# Create your views here.
from django.utils.decorators import method_decorator
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema

tags = ["用户相关接口"],
from rest_framework import viewsets

from apps.user.models import UserEntity
from utils.paginator import AppPageNumberPagination
from utils.queryset_filter import UserFilter
from utils.response import JsonResponse
from utils.serializer import UserSerializer


@method_decorator(
    name='partial_update',
    decorator=swagger_auto_schema(
        tags=["用户相关接口"],
        operation_description="**更新某一个用户信息**"
    )
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserEntity.objects.all().order_by('id')
    serializer_class = UserSerializer
    pagination_class = AppPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter

    @swagger_auto_schema(
        tags=["用户相关接口"],
        operation_description="**查询用户列表**"
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=["用户相关接口"],
        operation_description="**创建一个用户**"
    )
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=["用户相关接口"],
        operation_description="**查询某一个用户**"
    )
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=["用户相关接口"],
        operation_description="更新某一个用户信息"
    )
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @swagger_auto_schema(
        tags=["用户相关接口"],
        operation_description="删除某一个用户"
    )
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return JsonResponse(data=response.data)
