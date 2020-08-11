import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'komax_site.settings')
app = Celery('komax_site')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update()

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)