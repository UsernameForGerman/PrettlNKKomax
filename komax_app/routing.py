# test_one/routing.py
from django.urls import re_path, path
from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url("setup/", consumers.KomaxAppTaskConsumer),
    url("harnesses/", consumers.HarnessConsumer),
    url("komax_manager/", consumers.KomaxConsumer),
    url('komaxes/', consumers.KomaxWebConsumer),
    url('account/', consumers.WorkerConsumer),
    # path("komax_app/komaxes/", consumers.KomaxConsumer)
]