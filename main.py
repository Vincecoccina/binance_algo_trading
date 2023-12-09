import pandas as pd
import pandas_ta as ta
import numpy as np
import plotly.graph_objects as go
import os
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY_TEST")
secret_key = os.getenv("SECRET_KEY_TEST")

# Initialisation de l'API Binance
client = Client(api_key=api_key, api_secret=secret_key, tld='com',testnet=True)

def get_balance():
    x = client.get_account()
    df = pd.DataFrame(x["balances"])

def get_curr_value(symbol):
    price = client.get_symbol_ticker(symbol=symbol)
    return price["price"]





