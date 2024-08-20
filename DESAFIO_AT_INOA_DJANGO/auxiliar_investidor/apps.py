from django.apps import AppConfig

class AuxiliarInvestidorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auxiliar_investidor'

    def ready(self):
            from .scheduler.updater import start_scheduler
            start_scheduler()