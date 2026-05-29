from django.apps import AppConfig


class PuzzleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'puzzle'

    def ready(self):
        import os
        is_dev = os.environ.get('DEBUG', 'True').lower() == 'true'
        run_main = os.environ.get('RUN_MAIN') == 'true'
        
        if not is_dev or run_main:
            try:
                from .warmer import start_self_ping
                start_self_ping()
            except ImportError:
                pass
