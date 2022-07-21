from django.apps import AppConfig


class BibleappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bibleapp'

    def ready(self):
        import bibleapp.signals

    
        
