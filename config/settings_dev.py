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
RESOURCE_DIR = r'F:\resource'
