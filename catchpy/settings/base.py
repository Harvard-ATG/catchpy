"""
Django settings for catch project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import re

from corsheaders.defaults import default_headers
from dj_secure_settings.loader import load_secure_settings

SECURE_SETTINGS = load_secure_settings()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_NAME = 'catchpy'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECURE_SETTINGS.get('catchpy_django_secret_key', 'CHANGE_ME')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['localhost',  '127.0.0.1']
# allowed_hosts_other = os.environ.get('CATCHPY_ALLOWED_HOSTS', '')
allowed_hosts_other = SECURE_SETTINGS.get('catchpy_allowed_hosts', '')
if allowed_hosts_other:
    ALLOWED_HOSTS.extend(allowed_hosts_other.split())



# Application definition

INSTALLED_APPS = [
    'anno.apps.AnnoConfig',
    'consumer.apps.ConsumerConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'corsheaders',
]

MIDDLEWARE = [
    'log_request_id.middleware.RequestIDMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    #'django.middleware.common.CommonMiddleware',
    'catchpy.middleware.HxCommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'consumer.jwt_middleware.jwt_middleware',
]

ROOT_URLCONF = PROJECT_NAME + '.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = PROJECT_NAME + '.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': SECURE_SETTINGS.get('catchpy_db_name', 'catchpy'),
        'USER': SECURE_SETTINGS.get('catchpy_db_user', 'catchpy'),
        'PASSWORD': SECURE_SETTINGS.get('catchpy_db_password', 'catchpy'),
        'HOST': SECURE_SETTINGS.get('catchpy_db_hosts', 'localhost'),
        'PORT': SECURE_SETTINGS.get('catchpy_db_port', '5432'),
        'ATOMIC_REQUESTS': False,
        'CONN_MAX_AGE': 500,  # permanent connections
    },
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
"""
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
"""

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
_STATIC_DIRNAME = os.environ.get('CATCHPY_STATIC_DIRNAME', 'static')
STATIC_ROOT = os.environ.get('CATCHPY_STATIC_ROOT', os.path.join(BASE_DIR, _STATIC_DIRNAME + '/'))


# Logging config
_DEFAULT_LOG_LEVEL = os.environ.get('CATCHPY_LOG_LEVEL', 'DEBUG')
_LOG_ROOT = os.environ.get('CATCHPY_LOG_ROOT', BASE_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter',
        },
    },
    'formatters': {
        'simple': {
            'format': ('%(asctime)s|%(levelname)s [%(filename)s:%(funcName)s]'
                       ' [%(request_id)s] %(message)s')
        },
        'verbose': {
            'format': '%(levelname)s\t%(asctime)s.%(msecs)03dZ\t%(name)s:%(lineno)s\t%(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S'
        },
        'syslog': {
            'format': ('%(levelname)s [%(filename)s:%(funcName)s:%(lineno)s]'
                       ' [%(request_id)s] %(message)s')
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'syslog',
            'stream': 'ext://sys.stdout',
            'filters': ['request_id'],
        },
        'errorfile_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'filename': os.path.join(_LOG_ROOT, 'django-catchpy_errors.log'),
            'maxBytes': 10485760,  # 10MB
            'backupCount': 7,
            'encoding': 'utf8',
            'filters': ['request_id'],
        },
        'default': {
            'class': 'logging.handlers.WatchedFileHandler',
            'level': _DEFAULT_LOG_LEVEL,
            'formatter': 'verbose',
            'filename': os.path.join(_LOG_ROOT, 'django-catchpy.log'),
        },
    },
    'loggers': {
        'anno': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': True
        },
        'consumer': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True
        },
        'catchpy': {
            'level': 'INFO',
            'handlers': ['console'],
            'propagate': True
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'default'],
        },
    }
}



#
# definitions for catch webapp
#

# jsonld context
CATCH_JSONLD_CONTEXT_IRI = os.environ.get(
    'CATCH_JSONLD_CONTEXT_IRI',
    'http://catchpy.harvardx.harvard.edu.s3.amazonaws.com/jsonld/catch_context_jsonld.json')

# max number of rows to be returned in a search request
CATCH_RESPONSE_LIMIT = int(os.environ.get('CATCH_RESPONSE_LIMIT', 200))

# default platform for annotatorjs annotations
CATCH_DEFAULT_PLATFORM_NAME = os.environ.get(
    'CATCH_DEFAULT_PLATFORM_NAME', 'hxat-edx_v1.0')

# admin id overrides all permissions, when requesting_user
CATCH_ADMIN_GROUP_ID = os.environ.get('CATCH_ADMIN_GROUP_ID', '__admin__')

# log request time
CATCH_LOG_REQUEST_TIME = os.environ.get(
    'CATCH_LOG_REQUEST_TIME', 'false').lower() == 'true'
CATCH_LOG_SEARCH_TIME = os.environ.get(
    'CATCH_LOG_SEARCH_TIME', 'false').lower() == 'true'

# log jwt and jwt error message
CATCH_LOG_JWT = os.environ.get(
    'CATCH_LOG_JWT', 'false').lower() == 'true'
CATCH_LOG_JWT_ERROR = os.environ.get(
    'CATCH_LOG_JWT_ERROR', 'false').lower() == 'true'

# annotation body regexp for sanity checks
CATCH_ANNO_SANITIZE_REGEXPS = [
    re.compile(r) for r in ['<\s*script', ]
]

#
# settings for django-cors-headers
#
CORS_ORIGIN_ALLOW_ALL = True   # accept requests from anyone
CORS_ALLOW_HEADERS = default_headers + (
    'x-annotator-auth-token',  # for back-compat
)




