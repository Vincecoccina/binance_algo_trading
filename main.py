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

symbol = "ETHUSDT"
volume = 0.01
no_of_safety_orders = 5
proportion = 1
profit_target = 1

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


def run():
    while True:
        df1 = pd.DataFrame(columns=["price", "qty"])
        df2 = pd.DataFrame(columns=["price", "qty"])
        x = market_order(symbol, volume, "buy")
        df2.loc[0, "price"] = float(x[0]["price"])
        df2.loc[0, "qty"] = float(x[0]["qty"])
        df1 = pd.concat([df1,df2], ignore_index=True)

        curr_no_of_safety_orders = 0
        multiplied_volume = volume * 2
        deviation = -1
        next_price_level = -1

        while True:
            dev = cal_dev_from_initial_price(symbol, df1)
            print(f"deviation {dev}")
            if dev <= next_price_level*proportion:
                if curr_no_of_safety_orders < no_of_safety_orders:
                    try:
                        x = market_order(symbol, multiplied_volume, "buy")
                        df2.loc[0, "price"] = float(x[0]["price"])
                        df2.loc[0, "qty"] = float(x[0]["qty"])
                        df1 = pd.concat([df1,df2], ignore_index=True)
                    except:
                        pass

                    multiplied_volume *= 2
                    deviation *= 2
                    next_price_level += deviation
                    curr_no_of_safety_orders += 1

            pct_profit = cal_pct_profit(symbol, df1)
            print(f"pct_profit {pct_profit}")
            print(df1)

            if pct_profit >= profit_target:
                sell_all(symbol, df1)
                break


run()













