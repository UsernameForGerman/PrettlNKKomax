FROM python:3.6.11-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y \
  # psycopg2 dependencies
  && apt-get install gcc -y \
  && apt-get install libpq-dev -y \
  # for Django translations
  && apt-get install gettext -y

WORKDIR /home/django/

RUN mkdir -p  /home/django/app/
RUN mkdir -p  /home/django/app/static
RUN mkdir -p  /home/django/app/media
RUN mkdir -p  /var/komax_site/static/
RUN mkdir -p  /var/komax_site/media/

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/local/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker

#COPY ./compose/local/django/celery/beat/start /start-celerybeat
#RUN sed -i 's/\r//' /start-celerybeat
#RUN chmod +x /start-celerybeat

COPY ./compose/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r//' /start-flower
RUN chmod +x /start-flower

COPY ./komax_site /app

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
