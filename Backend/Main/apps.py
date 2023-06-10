from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Main'

    #? Initialize the signals
    def ready(self):
        import Main.signals
