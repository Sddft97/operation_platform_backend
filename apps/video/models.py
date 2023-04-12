from django.db import models


# Create your models here.
class Video(models.Model):
    videoId = models.CharField(unique=True, max_length=50, default="vid#########")
    videoName = models.CharField(max_length=100)
    videoUrl = models.CharField(unique=True, max_length=255)
    coverImgUrl = models.CharField(blank=True, null=True, max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    lastViewedAt = models.DateTimeField(auto_now=True)
    courseId = models.CharField(max_length=50, default="cid########")

    class Meta:
        db_table = 'video'
