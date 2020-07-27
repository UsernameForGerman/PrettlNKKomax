from .base import *


# GENERAL
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = ['.prettl.ru', 'django:9000', 'react:8080']

# CORS
# ------------------------------------------------------------------------------
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Gunicorn
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["gunicorn"]

# STATIC
# ------------------------------------------------------------------------------

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

# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'django.log',
            'maxBytes': 5*1024*1024,
            'backupCount': 1,
            'formatter': 'file',
        },
        # 'mail_admins': {
        #     'level': 'WARNING',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'email_backend': 'django.core.mail.backends.smtp.EmailBackend',
        #     'include_html': True,
        # }
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            # 'handlers': ['file', 'mail_admins']
            'handlers': ['file']
        },
    },
}

