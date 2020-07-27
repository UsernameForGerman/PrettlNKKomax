FROM python:3.6.11-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update -y \
  # psycopg2 dependencies
  && apt-get install gcc -y \
  && apt-get install libpq-dev -y
  # for Django translations
  # && apt-get install gettext -y

RUN addgroup --system django \
    && adduser --system --group django --shell /bin/sh

WORKDIR /home/django/

RUN mkdir -p  /home/django/app/
RUN mkdir -p  /home/django/app/static
RUN mkdir -p  /home/django/app/media
RUN mkdir -p  /var/komax_site/static/
RUN mkdir -p  /var/komax_site/media/

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
RUN chown django /start
COPY ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker
RUN chown django /start-celeryworker

#COPY ./compose/production/django/celery/beat/start /start-celerybeat
#RUN sed -i 's/\r//' /start-celerybeat
#RUN chmod +x /start-celerybeat
#RUN chown django /start-celerybeat
#
#COPY ./compose/production/django/celery/flower/start /start-flower
#RUN sed -i 's/\r//' /start-flower
#RUN chmod +x /start-flower
COPY ./komax_site /app

RUN chown -R django /app
# RUN chown -R django:django /home/django/
RUN chown -R django:django /var/komax_site

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
