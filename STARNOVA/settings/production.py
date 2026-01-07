from .base import *
import os

DEBUG = False

ALLOWED_HOSTS = [
    'starnova.itpoint.us',
    'www.starnova.itpoint.us',
    "127.0.0.1",
    "localhost",
    "31.97.233.191",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/STARNOVA/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/STARNOVA/media'

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
