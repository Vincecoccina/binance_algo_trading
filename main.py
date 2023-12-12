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
    print(df)

def get_curr_value(symbol):
    price = client.get_symbol_ticker(symbol=symbol)
    return price["price"]

def market_order(symbol,volume,direction):
    if direction == "buy":
        order = client.create_order(
            symbol=symbol,
            side=client.SIDE_BUY,
            type=client.ORDER_TYPE_MARKET,
            quantity=volume
        )
        return order["fills"]

    if direction == "sell":
        order = client.create_order(
            symbol=symbol,
            side=client.SIDE_SELL,
            type=client.ORDER_TYPE_MARKET,
            quantity=volume
        )
        return order["fills"]

# df1 = pd.DataFrame(columns=["price", "qty"])
# df2 = pd.DataFrame(columns=["price", "qty"])

# while True:
#     x = market_order("BTCUSDT", 0.002, "buy")
#     df2.loc[0, "price"] = float(x[0]["price"])
#     df2.loc[0, "qty"] = float(x[0]["qty"])
#     df1 = pd.concat([df1,df2], ignore_index=True)
#     print(df1)

def cal_dev_from_initial_price(symbol, df):
    curr_price = float(get_curr_value(symbol))
    init_price = float(df.price[0])
    pct_change = (curr_price - init_price)/init_price*100

    return pct_change

def cal_pct_profit(symbol, df):
    total_profit = 0
    total_value_of_coins = 0
    current_price = float(get_curr_value(symbol))

    for index in df.index:
        initial_value = float(df.loc[index, "price"]) * float(df.loc[index, "qty"])
        current_value = current_price * float(df.loc[index, "qty"])
        profit = current_value - initial_value
        total_profit += profit
        total_value_of_coins += initial_value
    
    return (total_profit/total_value_of_coins)*100

def sell_all(symbol, df):
    volume = float(df["qty"].sum())
    market_order(symbol, volume, "sell")







