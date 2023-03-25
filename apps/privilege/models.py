from django.db import models


# Create your models here.
class Privilege(models.Model):
    privilegeCode = models.CharField(unique=True, null=False, blank=False, max_length=20)
    privilegeName = models.CharField(unique=True, null=False, blank=False, max_length=30)

    class Meta:
        db_table = 'privilege'
