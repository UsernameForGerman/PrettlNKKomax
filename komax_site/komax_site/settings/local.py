from .base import *


ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
    }
}

# CORS
# ------------------------------------------------------------------------------
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_REPLACE_HTTPS_REFERER = True

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
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1"]
if os.environ.get("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]

# Celery
# ------------------------------------------------------------------------------
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-eager-propagates
# CELERY_TASK_EAGER_PROPAGATES = True
# CELERY_IGNORE_RESULT = True
# CELERYD_MAX_TASKS_PER_CHILD = 5

# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console']
        },
    },
}

# STATIC
# ------------------------

# STATICFILES_STORAGE = "config.settings.production.StaticRootS3Boto3Storage"
# STATIC_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/"
STATIC_ROOT = '/var/komax_site/static/'
STATIC_URL = '/files/static/'

# MEDIA
# ------------------------------------------------------------------------------
# region http://stackoverflow.com/questions/10390244/
# Full-fledge class: https://stackoverflow.com/a/18046120/104731
# from storages.backends.s3boto3 import S3Boto3Storage  # noqa E402
MEDIA_ROOT = '/var/komax_site/media/'
MEDIA_URL = '/files/media/'

