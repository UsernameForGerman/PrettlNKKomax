"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "komax_site.settings")
django.setup()
os.environ['ASGI_THREADS'] = "4"
application = get_default_application()


