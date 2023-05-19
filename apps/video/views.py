# Create your views here.
import os.path
import uuid

from django.conf import settings
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.request import Request

from apps.video.models import Video, StatusEnum
from apps.video.service import VideoUploadService
from utils.paginator import AppPageNumberPagination
from utils.queryset_filter import VideoFilter
from utils.response import JsonResponse
from utils.serializer import VideoSerializer

MEDIA_ROOT = settings.MEDIA_ROOT


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all().order_by('id')
    serializer_class = VideoSerializer
    pagination_class = AppPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = VideoFilter

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_upload_service = VideoUploadService()

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
        kwargs.update({'partial': True})
        response = super().update(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return JsonResponse(data=response.data)

    @action(methods=['post'], detail=False, url_path='uploadChunk')
    def upload_chunk(self, request: Request, *args, **kwargs):
        chunk = request.FILES.get('chunk')
        file_hash = request.data.get('fileHash')
        file_ext = request.data.get('fileExt')
        chunk_name = request.data.get('chunkName')

        self.video_upload_service.upload_file_chunk(chunk, chunk_name, file_hash, file_ext)

        return JsonResponse()

    @action(methods=['post'], detail=False, url_path='mergeChunk')
    def merge_chunk(self, request: Request, *args, **kwargs):
        file_hash = request.data.get('fileHash')
        file_ext = request.data.get('fileExt')
        file_name = request.data.get('fileName')

        origin_path = self.video_upload_service.merge_file_chunk(file_hash, file_ext)
        target_path = self.video_upload_service.move_to_db_dictionary(origin_path)
        mpd_path = self.video_upload_service.generate_mpd_path(target_path, file_hash)
        poster_path = self.video_upload_service.generate_poster_path(target_path, file_hash)
        video_id = f'vid_{file_hash}_{uuid.uuid4().hex[:8]}'
        video_data = {
            "videoId": video_id,
            "videoName": file_name,
            "videoUrl": os.path.relpath(mpd_path, MEDIA_ROOT),
            "coverImgUrl": os.path.relpath(poster_path, MEDIA_ROOT),
            "status": StatusEnum.PROCESSING.value
        }
        serializer = self.get_serializer(data=video_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 先更新数据库，再视频后处理
        self.video_upload_service.video_process(target_path, mpd_path, poster_path, video_id, self)
        return JsonResponse(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['post'], detail=False, url_path='verifyUpload')
    def verify_upload(self, request: Request, *args, **kwargs):
        file_hash = request.data.get('fileHash')
        file_ext = request.data.get('fileExt')
        res = self.video_upload_service.verify_should_upload(file_hash, file_ext)
        return JsonResponse(data=res)
