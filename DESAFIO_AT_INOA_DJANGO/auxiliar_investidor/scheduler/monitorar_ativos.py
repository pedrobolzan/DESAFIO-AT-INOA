import requests

from ..models import Ativo
from django.db import transaction

from apscheduler.schedulers.background import BackgroundScheduler

def monitorar_ativos(parametros):
    pass

def start_monitorar_ativos_scheduler(parametros):
    """Start a scheduler to update stock list periodically."""
    scheduler_update_ativos = BackgroundScheduler()

    scheduler_update_ativos.add_job(monitorar_ativos(parametros), 'interval', hours=24)  # Runs once every 24 hours
    scheduler_update_ativos.start()
    print("Stock list update scheduler started.")