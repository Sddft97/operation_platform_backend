from django.db import models


# Create your models here.
class Department(models.Model):
    deptCode = models.CharField(unique=True, max_length=50)
    deptName = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = 'department'
