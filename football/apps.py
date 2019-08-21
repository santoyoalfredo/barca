from django.apps import AppConfig

class FootballConfig(AppConfig):
    name = 'football'

    def ready(self):
        import football.signals
