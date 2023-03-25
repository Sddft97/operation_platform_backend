from django.db import models


class UserEntity(models.Model):
    class Meta:
        db_table = 'user'

    class Sex(models.TextChoices):
        MALE = '男'
        FEMAIL = '女'
        UNKNOWN = ''

    uid = models.CharField(unique=True, max_length=100)
    avatar = models.CharField(null=True, blank=True, max_length=255)
    email = models.CharField(null=True, blank=True, max_length=50)
    username = models.CharField(max_length=20)
    sex = models.CharField(choices=Sex.choices, null=True, blank=True, max_length=5)
    privCode = models.CharField(max_length=10)
    deptCode = models.CharField(max_length=10)
    phoneNumber = models.CharField(max_length=20)
