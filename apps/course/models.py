from django.db import models


# Create your models here.
class Course(models.Model):
    courseId = models.CharField(unique=True, max_length=50)
    courseName = models.CharField(unique=True, max_length=50)
    courseDescription = models.CharField(null=True, blank=True, max_length=500)
    courseCoverUrl = models.CharField(null=True, blank=True, max_length=255)

    courseTypeId = models.IntegerField()
    deptCode = models.CharField(max_length=50)

    class Meta:
        db_table = 'course'


class CourseType(models.Model):
    name = models.CharField(unique=True, max_length=50)
    label = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'course_type'
