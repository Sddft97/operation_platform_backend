from enum import Enum

from django.db import models


class StatusEnum(Enum):
    UNKNOWN = 0
    UPLOADING = 1
    PROCESSING = 2
    FINISHED = 3


# Create your models here.
class Video(models.Model):
    videoId = models.CharField(unique=True, max_length=50)
    videoName = models.CharField(max_length=100)
    videoUrl = models.CharField(unique=True, max_length=255)
    coverImgUrl = models.CharField(blank=True, null=True, max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    lastViewedAt = models.DateTimeField(auto_now=True)
    courseId = models.CharField(max_length=50)
    resolutionVersion = models.CharField(max_length=50, null=True, blank=True)
    status = models.IntegerField(default=StatusEnum.UNKNOWN.value)

    class Meta:
        db_table = 'video'
