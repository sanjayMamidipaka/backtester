import backtester
from stockstats import StockDataFrame
import pandas as pd
import matplotlib.pyplot as plt
import math, numpy as np

final = 0.0
initial = pd.read_json('https://cloud.iexapis.com/stable/stock/amd/intraday-prices?token=pk_03bf40cb7637400faf65d2d30773bf22&exactDate=20200518')

stock = StockDataFrame.retype(initial)
initial['bband1'] = stock['boll_lb']
initial['bband2'] = stock['boll_ub']
initial['rsi'] = stock['rsi_6']
initialInvestment = 500.0
stoploss = float(initial['close'][0]) - 0.1

b = backtester.Backtester(initialInvestment)
for i in range(0,len(initial.index)):

    if (stock['rsi_6'][i] < 45 and float(initial['close'][i] - initial['bband1'][i]) < 0.1 or float(initial['close'][i]) <= float(stoploss)): #buy
        if b.buy(math.floor(initialInvestment/initial['close'][i]), initial['close'][i], i):
            pass

    elif (stock['rsi_6'][i] > 60 and float(initial['bband2'][i] - initial['close'][i]) < 0.1 or float(initial['close'][i]) <= float(stoploss)): #sell
        if b.sell(b.get_current_buys(), initial['close'][i], i):
            pass


i = len(initial.index)-1
if b.sell(b.get_current_buys(), initial['close'][i], i): #sell everything once the day is done
    print('sell')


#plt.plot(stock['timestamp'], initial['close'])

#plt.scatter(sellx, selly,c='red', label='sell')
#plt.scatter(buyx, buyy,c='green', label='buy')
final += float(b.get_returns())
#plt.legend()
print(b.get_returns())
#plt.show()

print(final)
