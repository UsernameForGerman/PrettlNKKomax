web: daphne komax_site.asgi:application --port $PORT --bind 0.0.0.0
worker: python manage.py celery worker --loglevel=info
beat: python manage.py celery beat --loglevel=info