"""
Django settings for komax_site project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import dj_database_url
# import dotenv
# import django_heroku
import redis
from corsheaders.defaults import default_headers
from django.utils.translation import gettext_lazy as _
import urllib.parse

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# To set sqlite3 locally and postresql on server:
# dotenv_file = os.path.join(BASE_DIR, ".env")
# if os.path.isfile(dotenv_file):
#     dotenv.load_dotenv(dotenv_file)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "l2gugz_=3y)eq5jz2&+qu*f%5t_i=kgx0dcn=1v&8^1*2%mkw5"
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = os.environ.get('DEBUG', True)
# INPROD = os.environ.get('INPROD', False)
INPROD = os.environ.get('INPROD', False)
DEBUG = os.environ.get('DEBUG', True)

ALLOWED_HOSTS = ['localhost', 'komax.prettl.ru']

CORS_ALLOW_HEADERS = (
    'Access-Control-Allow-Headers',
    'Access-Control-Allow-Credentials',
    'Cache-Control',
    'If-Modified-Since',
    'Accept',
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)


SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'



# Application definition
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'description.apps.DescriptionConfig',
    'main_app.apps.MainAppConfig',
    'komax_app.apps.KomaxAppConfig',
    'api_komax_app.apps.ApiKomaxAppConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
]

MIDDLEWARE = [
    # 'corsheaders.middleware.CorsMiddleware',
    'api_komax_app.middleware.cors.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsPostCsrfMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    # 'DEFAULT_RENDERER_CLASSES': (
    #     'rest_framework.renderers.JSONRenderer',
    #     'rest_framework_xml.renderers.XMLRenderer',
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
}


CORS_ORIGIN_WHITELIST = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1:9000"
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

ROOT_URLCONF = 'komax_site.urls'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'main_app/templates'),
            os.path.join(BASE_DIR, 'description/templates'),
            os.path.join(BASE_DIR, 'komax_app/templates')
        ]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'komax_site.wsgi.application'

# Channels
ASGI_APPLICATION = 'komax_site.routing.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

if not INPROD:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'komaxdb',
            'USER': 'server',
            'PASSWORD': "zMv-a5QZ7+Jm5!*@",
            'HOST': "127.0.0.1",
            'PORT': 5432,
        }
    }

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # 'komax_app.backends.WorkerAuthBackend'
]

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
    os.path.join(BASE_DIR, 'description/locale'),
    os.path.join(BASE_DIR, 'komax_app/locale'),
    os.path.join(BASE_DIR, 'main_app/locale'),
)

LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Russian'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'main_app/static/'),
    os.path.join(BASE_DIR, 'komax_app/static/'),
    # os.path.join(BASE_DIR, 'static/'),
    # os.path.join(BASE_DIR, 'description/static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media')

MEDIA_URL = '/media/'


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', '6379')],
        },
    },
}

# IS_CI = os.environ.get('IS_CI', False)
# if not IS_CI:
#     django_heroku.settings(locals())

# Email send
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'info-komax@yandex.ru '
EMAIL_HOST_PASSWORD = 'komax_prettl-nk'
EMAIL_USE_SSL = True
SITE_URL = 'komaxsite.herokuapp.com'



# Localhost related seetings to REDIS and CELERY
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/account/'
LOGOUT_REDIRECT_URL = '/'



