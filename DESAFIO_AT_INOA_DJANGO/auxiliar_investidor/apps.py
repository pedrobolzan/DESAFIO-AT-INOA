from django.apps import AppConfig

class AuxiliarInvestidorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auxiliar_investidor'

    def ready(self):
            from .scheduler.listar_ativos import start_stock_update_scheduler, debug_stock_update
            from .scheduler.monitorar_ativos import monitorar_todos_os_ativos
            start_stock_update_scheduler()
            monitorar_todos_os_ativos()
            #debug_stock_update()
