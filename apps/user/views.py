# Create your views here.
from django_filters import rest_framework as filters
from rest_framework import viewsets

from apps.user.models import UserEntity
from utils.paginator import AppPageNumberPagination
from utils.queryset_filter import UserFilter
from utils.response import JsonResponse
from utils.serializer import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserEntity.objects.all().order_by('id')
    serializer_class = UserSerializer
    pagination_class = AppPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return JsonResponse(data=response.data)
