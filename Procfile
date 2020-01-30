web: daphne komax_site.asgi:application --port $PORT --bind 0.0.0.0
worker: celery worker -A komax_app --loglevel=info