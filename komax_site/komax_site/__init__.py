from .celery import app

from komax_site.celery import app as celery_app

__all__ = ('app', 'celery_app')
