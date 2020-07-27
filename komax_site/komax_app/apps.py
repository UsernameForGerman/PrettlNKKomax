from django.apps import AppConfig


class KomaxAppConfig(AppConfig):
    name = 'komax_app'

    def ready(self):
        import komax_app.signals
