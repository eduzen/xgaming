from django.apps import AppConfig


class IgamingConfig(AppConfig):
    name = 'igaming'

    def ready(self):
        import igaming.signals
