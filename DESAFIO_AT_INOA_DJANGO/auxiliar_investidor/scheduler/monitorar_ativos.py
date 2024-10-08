import requests
import os

from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from apscheduler.schedulers.background import BackgroundScheduler
from ..models import Ativo, Cotacao, TunelParametro

scheduler = BackgroundScheduler()
scheduler.start()

def verificar_preco(ativo_id, parametros):

    ativo = Ativo.objects.get(id=ativo_id)

    token = os.environ.get('BRAPI_TOKEN')

    url = f'https://brapi.dev/api/quote/{ativo.codigo}?token={token}'
    response = requests.get(url)

    if response.status_code == 200:
        try:
            cotacao_atual = response.json()['results'][0]['regularMarketPrice']
            print(f"Stock price for code {ativo.codigo} is {cotacao_atual}.")
        except (KeyError, IndexError):
            print(f"Failed to fetch stock name for code {cotacao_atual}.")
    else:
        print("Failed to fetch stock data from BRAPI")

    if cotacao_atual is None:
        print(f"Não foi possível obter a cotação para {ativo.codigo}")
        return
    
    Cotacao.objects.create(ativo=ativo, preco_negocio=cotacao_atual, data_hora=timezone.now())

    if cotacao_atual <= parametros.limite_inferior:
        print(f"Atenção: O preço da ação {ativo.codigo} atingiu o limite inferior definido de {parametros.limite_inferior}!")
        subject = f"Alerta de Ação: {ativo.codigo} atingiu o limite inferior de preço"
        html_message = render_to_string('email_inferior.html', {
            'codigo_acao': ativo.codigo,
            'nome_acao': ativo.nome,
            'preco_atual': cotacao_atual,
            'limite_inferior': parametros.limite_inferior
        })
        plain_message = strip_tags(html_message)
        from_email = "pedrobolzan@poli.ufrj.br"
        to = parametros.email

        send_mail(subject, plain_message, from_email, [to], html_message=html_message)

    if cotacao_atual >= parametros.limite_superior:
        print(f"Atenção: O preço da ação {ativo.codigo} atingiu o limite superior definido de {parametros.limite_superior}!")
        subject = f"Alerta de Ação: {ativo.codigo} atingiu o limite superior de preço"
        html_message = render_to_string('email_superior.html', {
            'codigo_acao': ativo.codigo,
            'nome_acao': ativo.nome,
            'preco_atual': cotacao_atual,
            'limite_superior': parametros.limite_superior
        })
        plain_message = strip_tags(html_message)
        from_email = "pedrobolzan@poli.ufrj.br"
        to = parametros.email

        send_mail(subject, plain_message, from_email, [to], html_message=html_message)

def create_monitorar_ativos_scheduler(ativo_id, parametros):

    #scheduler = BackgroundScheduler()
    
    intervalo = parametros.periodicidade  # Em minutos

    #schedule_existente = TunelParametro.objects.get(ativo_id=ativo_id)

    job_id = f'verificar_preco_{ativo_id}'

    print(job_id)

    if scheduler.get_job(job_id):
        print(f"Monitoramento do ativo {ativo_id} já existe. Verificando se é necessário alterar o intervalo.")
        scheduler.reschedule_job(
                job_id,
                trigger='interval',
                minutes=intervalo,
            )
    else:
        scheduler.add_job(
            verificar_preco,
            'interval',
            minutes=intervalo,
            args=[ativo_id, parametros],
            id=job_id,
            replace_existing=True,
        )
        print(f"Monitoramento do ativo {ativo_id} criado com sucesso com intervalo de {intervalo} minutos."),
        
    #scheduler.start()

def monitorar_todos_os_ativos():
    
    #scheduler = BackgroundScheduler()

    ativos_monitorados = Ativo.objects.filter(tunelparametro__isnull=False)
    for ativo in ativos_monitorados:
        try:
            parametros = TunelParametro.objects.get(ativo=ativo)
            intervalo = parametros.periodicidade 

            scheduler.add_job(
                verificar_preco,
                'interval',
                minutes=intervalo,
                args=[ativo.id, parametros],
                id=f'verificar_preco_{ativo.id}',
                replace_existing=True,
            )
            print(f"Monitoramento do ativo {ativo.codigo} iniciado com intervalo de {intervalo} minutos com job id = verificar_preco_{ativo.id}.")
        except TunelParametro.DoesNotExist:
            print(f"Parâmetros não encontrados para o ativo {ativo.codigo}. Monitoramento não iniciado.")
    print("--------------------------------------------------------------------------------")
    print("Monitoramento de todos os ativos iniciado.")
    #scheduler.start()

def remove_monitoramento(ativo_id):
    scheduler.remove_job(f'verificar_preco_{ativo_id}')
    print(f"Monitoramento do ativo {ativo_id} removido com sucesso.")