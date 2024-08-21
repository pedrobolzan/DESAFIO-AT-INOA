'''import time
import os
import csv
import requests
#import re
import zipfile

#import pandas as pd

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.memory import MemoryJobStore

from datetime import datetime
from io import BytesIO

from ..models import Ativo, Cotacao

def baixar_arquivo_csv():
    
    today = datetime.today()
    year = today.strftime('%Y')
    month = today.strftime('%m')
    day = today.strftime('%d')

    url = f'https://arquivos.b3.com.br/apinegocios/tickercsv/{year}-{month}-19'
    
    response = requests.get(url)
    
    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            for filename in z.namelist():
                if filename.endswith('.txt'):
                    with z.open(filename) as csvfile:
                        csv_path = 'cotacoes.csv'
                        with open(csv_path, 'wb') as f:
                            f.write(csvfile.read())
                    print(f"CSV file downloaded and saved as {csv_path}")
                    return csv_path
        print("No CSV file found in the ZIP.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
    return None

def format_time(number):
    hours = number // 10000000
    minutes = (number // 100000) % 100
    seconds = (number // 1000) % 100
    milliseconds = number % 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def processar_csv_e_salvar_bd(caminho_csv):
    with open(caminho_csv, mode='r', encoding='latin-1') as file:
        csv_reader = csv.reader(file, delimiter=';')
        next(csv_reader)  # Pular o cabeçalho

        for index, row in enumerate(csv_reader):
            codigo = row[1].strip()
            preco_negocio = float(row[3].replace(',', '.'))
            data_referencia = datetime.strptime(row[0], '%Y-%m-%d')
            hora_fechamento = format_time(int(row[5].strip()))
            data_hora = datetime.strptime(f'{data_referencia.date()} {hora_fechamento}', '%Y-%m-%d %H:%M:%S,%f')
            quantidade_negociada = int(row[4])
            
            ativo, created = Ativo.objects.get_or_create(codigo=codigo)

            # Create a new Cotacao record
            Cotacao.objects.create(
                ativo=ativo, 
                preco_negocio=preco_negocio, 
                quantidade_negociada=quantidade_negociada, 
                data_hora=data_hora
            )

            if created:
                print(f'Ativo {codigo} foi criado no banco de dados.')

    print("Processamento concluído.")
    return None

def cotacoes_task():
    csv_file = baixar_arquivo_csv()
    if csv_file:
        processar_csv_e_salvar_bd(csv_file)
        os.remove(csv_file)

def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_jobstore(MemoryJobStore(), "default")

    #scheduler.add_job(cotacoes_task, CronTrigger.from_crontab('0 9 * * *'), id='cotacoes_task', replace_existing=True)
    scheduler.add_job(cotacoes_task, CronTrigger.from_crontab('* * * * *'), id='cotacoes_task', replace_existing=True)

    scheduler.start()
    print("Scheduler started...")

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()'''