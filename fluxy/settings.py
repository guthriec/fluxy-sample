"""
Django settings for fluxy project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = TEMPLATE_DEBUG = False

ADMINS = (
    ('Ayush Sood', 'ayushsood@gmail.com'),
    ('Chris Guthrie', 'guthriec93@gmail.com'),
    ('Rahul Gupta-Iwasaki', 'deepthinkingfool@gmail.com'),
    ('Arushi Raghuvanshi', 'arushi.raghu@gmail.com'),
    ('Amrit Saxena', 'amrit.saxena1@gmail.com'),
)
MANAGERS = ADMINS

SERVER_EMAIL = 'Fluxy Support <support@fluxyapp.com>'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ALLOWED_HOSTS = []

# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# All media is migrated to S3 buckets
MEDIA_ROOT = ''
MEDIA_URL = ''

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Imported from local_settings
AWS_S3_ACCESS_KEY_ID = ''
AWS_S3_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''

# If one enables Access to private, the links will no longer be public
# and the cache will break
# AWS_DEFAULT_ACL = 'private'
AWS_QUERYSTRING_AUTH = False
AWS_HEADERS = {
  'Cache-Control': 'max-age=86400', #(1 day)
}

# Static files - includes JS, CSS and Images
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
  # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
  'compressor.finders.CompressorFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
  'django.template.loaders.filesystem.Loader',
  'django.template.loaders.app_directories.Loader',
  # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

SECRET_KEY = '36b2glm^*w=wz8+y&fn^s6^huvgibiaz$7++!rayba8fi)%0pd'

INSTALLED_APPS = (
    'fluxy',
    'deals',
    'dashboard',
    'landing_page',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Look to the default backend first, if authentication fails on that
# fall back to the Facebook backend.
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'fluxy.facebook_backend.FacebookBackend',
)

# Replacing django user model
AUTH_USER_MODEL = 'fluxy.FluxyUser'

# Safer version for the signed cookie session backend
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Login URL
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

ROOT_URLCONF = 'fluxy.urls'
WSGI_APPLICATION = 'fluxy.wsgi.application'

# Caching
# https://docs.djangoproject.com/en/dev/topics/cache/
# using python-memcached
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
          '127.0.0.1:11211'
        ]
    }
}

try:
  # Local dev settings - use local_settings_template.py as a template and move
  # it to local_settings.py
  from local_settings import *
except ImportError:
  pass
