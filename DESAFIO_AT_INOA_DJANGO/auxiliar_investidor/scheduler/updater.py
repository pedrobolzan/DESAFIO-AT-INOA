import time
import os
#import csv
import requests
#import re
import zipfile

import pandas as pd

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

    df = pd.read_csv(caminho_csv, delimiter=';', encoding='latin-1')
    
    df['PrecoNegocio'] = df['PrecoNegocio'].replace(',', '.', regex=True).astype(float)
    df['HoraFechamento'] = df['HoraFechamento'].apply(format_time)

    df['DataReferencia'] = pd.to_datetime(df['DataReferencia'])
    df['datetime'] = df['DataReferencia'].astype(str) + ' ' + df['HoraFechamento']
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S,%f')

    for index, row in df.iterrows():
        codigo = row['CodigoInstrumento'] 
        preco_negocio = row['PrecoNegocio']
        data_hora = row['datetime']
        quantidade_negociada = row['QuantidadeNegociada']

        try:
            ativo = Ativo.objects.get(codigo=codigo)
            Cotacao.objects.create(ativo=ativo, preco_negocio=preco_negocio, quantidade_negociada=quantidade_negociada, data_hora=data_hora)
        except Ativo.DoesNotExist:
            print(f'Ativo {codigo} não encontrado no banco de dados.')
        except Exception as e:
            print(f'Erro ao processar a linha {index}: {e}')

    print("Processamento concluído.")

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
        scheduler.shutdown()