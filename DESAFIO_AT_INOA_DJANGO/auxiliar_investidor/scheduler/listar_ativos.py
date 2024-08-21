import requests

from ..models import Ativo
from django.db import transaction

from apscheduler.schedulers.background import BackgroundScheduler

def fetch_available_stocks():
    """Fetch the list of available stocks from BRAPI API."""
    url = "https://brapi.dev/api/available"
    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    print(data)
    print(f"Received {len(data['stocks'])} stock symbols from the API.")

    stocks = data['stocks']

    return stocks

def fetch_stock_name(stock_code):
    """Fetch the full name of a stock based on its code from BRAPI."""
    url = f'https://brapi.dev/api/quote/{stock_code}?token=cfAWDpKFkPa6ZeN6B3Cxyo'
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            nome = response.json()['results'][0]['longName']
            print(f"Stock name for code {stock_code} is {nome}.")
            return nome
        except (KeyError, IndexError):
            print(f"Failed to fetch stock name for code {stock_code}.")
            nome = f"Átivo de código {stock_code}"
    else:
        print("Failed to fetch stock data from BRAPI")
    
    return None

def insert_stocks_into_db(stocks):
    """Fetch the full name of each stock and insert or update it in the Ativo model."""
    existing_stocks = Ativo.objects.values_list('codigo', flat=True)
    print(existing_stocks)
    print("============================================================================================")

    for stock in stocks:

        if stock not in existing_stocks:
            # Fetch the full name of the stock from BRAPI
            nome = fetch_stock_name(stock)
                
            if nome:
                # Use update_or_create to either update an existing record or create a new one
                Ativo.objects.update_or_create(
                    codigo=stock,
                    nome=nome
                )
                print(f"Stock code {stock} has been added to the database with name {nome}.")
            else:
                print(f"Stock name for code {stock} could not be found.")
        else:
            pass
            #print(f"Stock code {stock} already exists in the database.")

def update_stock_list():
    print("fetching stock list...")
    stocks = fetch_available_stocks()
    print("inserting stocks into db...")
    insert_stocks_into_db(stocks)

def start_stock_update_scheduler():
    """Start a scheduler to update stock list periodically."""
    scheduler_update_ativos = BackgroundScheduler()

    scheduler_update_ativos.add_job(update_stock_list, 'interval', hours=24)  # Runs once every 24 hours
    scheduler_update_ativos.start()
    print("Stock list update scheduler started.")

def debug_stock_update():
    update_stock_list()
    print("Stock list update manual query started.")
