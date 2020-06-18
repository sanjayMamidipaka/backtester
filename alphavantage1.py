import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import pandas_ta as ta
import backtester, math

initial = pd.read_csv('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=15min&symbol=msft&apikey=OUMVBY0VK0HS8I9E&datatype=csv&outputsize=full')
initial = initial[::-1]
initial = initial.reset_index(drop=True)

bbands = ta.bbands(initial['close'], length=200, std=2) #calculating indicators
ema_50 = ta.ema(initial['close'], length=50)
ema_200 = ta.ema(initial['close'], length=200)
rsi = ta.rsi(initial['close'], length=26)
vwap = ta.vwap(initial['high'], initial['low'], initial['close'], initial['volume'])
initial = pd.concat([initial, bbands, ema_50, ema_200, rsi, vwap], axis=1)
initial.columns =['timestamp', 'open', 'high', 'low', 'close', 'volume', 'bband1', 'useless', 'bband2', 'ema1', 'ema2', 'rsi', 'vwap']

initialInvestment = 1000
numTrades = 0
buyx = []
buyy = []
sellx = []
selly = []
b = backtester.Backtester(initialInvestment)
for i in range(200,len(initial.index)):
    one = int(initial['ema1'][i] >= initial['ema2'][i]) #ema
    two = int(initial['rsi'][i] <= 30) # rsi
    three = int(initial['bband1'][i] - initial['open'][i] <= 0.01 or initial['open'][i] <= initial['bband1'][i]) #bollinger bands
    four = int(initial['open'][i] <= initial['vwap'][i]) #vwap
    total = one + two + three + four

    newOne = int(initial['ema1'][i] <= initial['ema2'][i])
    newTwo = int(initial['rsi'][i] >= 70)
    newThree = int(initial['open'][i] - initial['bband2'][i] <= 0.01 or initial['open'][i] >= initial['bband2'][i])
    newFour = int(initial['open'][i] >= initial['vwap'][i]) #vwap
    newTotal = newOne + newTwo + newThree + newFour

    

    if (total >= 3): #buy
        if b.buy(math.floor(float(initialInvestment)/float(initial['open'][i])), float(initial['open'][i]), i):
            numTrades += 1
            buyx.append(i)
            buyy.append(initial['open'][i])

    elif (newTotal >= 3): #sell
        if b.sell(b.get_current_buys(), initial['open'][i], i):
            sellx.append(i)
            selly.append(initial['open'][i])


i = len(initial.index)-1
if b.sell(b.get_current_buys(), initial['open'][i], i): #sell everything once the day is done
    sellx.append(i)
    selly.append(initial['open'][i])

initial['open'].plot()
plt.scatter(sellx, selly,c='red', label='sell')
plt.scatter(buyx, buyy,c='green', label='buy')
plt.legend()
print(b.get_returns())
print('Number of buy-sell pairs:', numTrades)
plt.show()