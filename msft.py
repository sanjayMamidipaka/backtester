import requests, json
import matplotlib.pyplot as plt
import requests, time
import bs4
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import json, time, math, backtester
from stockstats import StockDataFrame
import alpaca_trade_api as tradeapi

APCA_API_KEY_ID = 'PK27ZUFXYB6Q9T2PR9W6'
APCA_API_SECRET_KEY = 'Y9ur5bxfjlOc4bJhEiYRvNKRSEu5j5nxhw80oWJb'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL, api_version='v2')
account = api.get_account()


def create_order(symbol, qty, side, type, time_in_force):
    api.submit_order(
        symbol= symbol,
        qty=qty,
        side=side,
        type=type,
        time_in_force=time_in_force
)




def scrape(df, stopprofit, stoploss):
    count = 0
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    f = ''
    r = requests.get('https://finance.yahoo.com/quote/MSFT?p=MSFT&.tsrc=fin-srch')
    soup = bs4.BeautifulSoup(r.text, 'lxml')
    f = soup.find('div',{'class': 'My(6px) Pos(r) smartphone_Mt(6px)'}).find('span').text

    g = soup.find_all('td')
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    count += 1
    dict1 = {'Time': dt_string, 'close': float(f)}
    print(dict1)
    total.append(dict1)
    initial = pd.DataFrame(total)

    stock = StockDataFrame.retype(initial)
    initial['bband1'] = stock['boll_lb']
    initial['bband2'] = stock['boll_ub']
                    
    if ((stock['rsi_6'][i] <= 30 and initial['close'][i] - initial['bband1'][i] < 0.1)): #buy
        if b.buy(math.floor(initialInvestment/initial['close'][i]), initial['close'][i], i):
            print(create_order('MSFT', 55, 'buy', 'market', 'gtc'))

    elif ((stock['rsi_6'][i] >= 70 and initial['bband2'][i] - initial['close'][i] < 0.1) or float(f) >= stopprofit or float(f) <= stoploss): #sell
        if b.sell(b.get_current_buys(), initial['close'][i], i):
            print(create_order('MSFT', 55, 'sell', 'market', 'day'))
    else:
        print('no trade executed')

    stopprofit = float(f) + 0.05
    stoploss = float(f) - 0.05

                
            



total = []
initialInvestment = 500.0
stopprofit = 0
stoploss = 0
b = backtester.Backtester(initialInvestment)
df = pd.DataFrame()

for i in range(100000):
    time.sleep(30)
    scrape(df, stopprofit, stoploss)

#try using stochastic with rsi
#use middle bband value
#check if middle bband  value is closer and if it touches