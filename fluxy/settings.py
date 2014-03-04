"""
Django settings for fluxy project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '36b2glm^*w=wz8+y&fn^s6^huvgibiaz$7++!rayba8fi)%0pd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    'fluxyapp.com',
    'www.fluxyapp.com',
    'http://fluxyapp.com',
    'http://www.fluxyapp.com'
]

ADMINS = (
    ('Ayush Sood', 'ayushsood@gmail.com'),
    ('Chris Guthrie', 'guthriec93@gmail.com'),
    ('Rahul Gupta-Iwasaki', 'deepthinkingfool@gmail.com'),
    ('Arushi Raghuvanshi', 'arushi.raghu@gmail.com'),
    ('Amrit Saxena', 'amrit.saxena1@gmail.com'),
)

# Application definition

INSTALLED_APPS = (
    'deals',
    'fluxy',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'fluxy.urls'

WSGI_APPLICATION = 'fluxy.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Replacing django user model
AUTH_USER_MODEL = 'fluxy.FluxyUser'

# Template files

TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'templates'),
]

try:
  # Local dev settings - use local_settings_template.py as a template and move
  # it to local_settings.py
  from local_settings import *
except ImportError:
  pass
