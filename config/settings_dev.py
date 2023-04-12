# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'operation_platform',
        'USER': 'root',
        'PASSWORD': '010508ssw',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}

# resource root path for videos, images, etc
MEDIA_ROOT = r'F:\resource'

# temp dictionary to save file chunks when uploading big files by chunk
TMP_UPLOAD_ROOT = r'F:\resource\tmp'

STATIC_SERVER = r'http://localhost:3557/'
