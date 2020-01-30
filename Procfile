web: daphne komax_site.asgi:application --port $PORT --bind 0.0.0.0
worker: celery worker -A komax_app -B --loglevel=info
python manage.py celery -v 2 -B -s celery -E -l INFO