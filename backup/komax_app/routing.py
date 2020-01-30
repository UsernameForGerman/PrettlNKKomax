# test_one/routing.py
from django.urls import re_path, path
from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url("komax_app/setup/", consumers.KomaxAppTaskConsumer),
    url("komax_app/harnesses/", consumers.HarnessConsumer),
    # path("komax_app/komaxes/", consumers.KomaxConsumer)
]