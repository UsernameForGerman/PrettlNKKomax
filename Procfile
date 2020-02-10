release: python manage.py makemigrations && python manage.py migrate --noinput
web: daphne komax_site.asgi:application --port $PORT --bind 0.0.0.0
worker: REMAP_SIGTERM=SIGQUIT celery worker --app komax_site.celery.app --loglevel info