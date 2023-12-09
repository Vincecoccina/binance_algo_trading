import pandas as pd
import pandas_ta as ta
import numpy as np
import plotly.graph_objects as go
import os
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")

# Initialisation de l'API Binance
client = Client(api_key=api_key, api_secret=secret_key, tld='com')

# Fonction de récupération des données historique du BITCOIN sur 500 jours
def get_historical_data(symbol, interval, limit=500):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'Quote_asset_volume', 'Number_of_trades', 'Taker_buy_base_asset_volume', 'Taker_buy_quote_asset_volume', 'Ignore'])
    df[['Open', 'High', 'Low', 'Close']] = df[['Open', 'High', 'Low', 'Close']].astype(float)
    return df

data = get_historical_data('BTCUSDT', '1d', limit=500)
# Nettoyage des données
data = data.drop(columns=['Quote_asset_volume', 'Close_time', 'Number_of_trades','Taker_buy_base_asset_volume', 'Taker_buy_quote_asset_volume', 'Ignore' ])
data['Open_time'] = pd.to_datetime(data['Open_time'], unit='ms')
data.rename(columns={'Open_time': 'Date'}, inplace=True)
data.set_index('Date', inplace=True)
# Ajout de la colonne SMA
data["SMA_10"] = ta.sma(data["Close"], length=10)




