from django.apps import AppConfig


class AppTranscriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_transcription'

    def ready(self):
        import app_transcription.signals
