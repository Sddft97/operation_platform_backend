# Generated by Django 4.1.7 on 2023-04-14 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0005_alter_video_videoname_alter_video_videourl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='courseId',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='video',
            name='videoId',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
