from django.apps import AppConfig

class AntiTimelineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'medialogue'

    def ready(self):
        import medialogue.signals
