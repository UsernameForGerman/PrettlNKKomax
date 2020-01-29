import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'komax_site.settings')
app = Celery('komax_app')
app.config_from_object('django.conf:settings')

app.conf.update(BROKER_URL=os.environ['BROKER_URL'],
                CELERY_RESULT_BACKEND=os.environ['BROKER_URL'])

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)