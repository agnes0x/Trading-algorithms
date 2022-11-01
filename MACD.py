
################################################################################################
"Libraries"
################################################################################################
from sklearn.svm import SVR
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


################################################################################################
"Data"
################################################################################################
#Load the data
DATA =pd.read_csv("BTC.csv")
DATA

DATA = DATA.set_index(pd.DatetimeIndex(DATA['Date'].values))
DATA

#Visualize the data
plt.figure(figsize=(12.5,4.5))
plt.plot(DATA['Closing Price (USD)'], label = 'closing price')
plt.title('Price over the years')
plt.xlabel('Date', fontsize =18)
plt.ylabel('Price in USD ($)', fontsize =18)
plt.xticks(rotation = 45)
plt.legend(loc='upper left')
plt.show()
plt.draw()

################################################################################################
"3 - MACD crossover"
################################################################################################

###Trade Rule: Moving Average Convergence Divergence Crossover (MACD)
#Signal: Difference between exponentially moving averages to determine momentum and direction
#short term: typically
#buy: MACD line above the signal line
#sell: MACD line below the signal line
#signal line: 9 period
#Macd line: short term exp. moving avg. (ShortEMA)- long term exp. moving avg. (LongMEA)
#short term: typically 12 periods
#long term: typically 26 period


################################################################################################
'Calculate'
################################################################################################

ShortEMA = DATA['Closing Price (USD)'].ewm(span=12, adjust=False).mean()
LongEMA = DATA['Closing Price (USD)'].ewm(span=26, adjust=False).mean()
MACD = ShortEMA - LongEMA
Signal = MACD.ewm(span=9, adjust = False).mean()

################################################################################################
'Visualize'
################################################################################################

plt.figure(figsize=(12.2, 4.5))
plt.plot(DATA.index, MACD, label = 'MACD', color = 'red')
plt.plot(DATA.index, Signal, label = 'Signal', color = 'blue')
plt.legend(loc='upper left')
plt.xticks(rotation = 45)
plt.show()

################################################################################################
'Buy and sell'
################################################################################################
DATA['MACD']= MACD
DATA['Signal']= Signal

def buy_sell(data):
    Buy = []
    Sell = []
    flag = -1
    
    for i in range(0, len(Signal)):
        if DATA['MACD'][i]> DATA['Signal'][i]:
            Sell.append(np.nan)
            if flag !=1:
                Buy.append(DATA['Closing Price (USD)'][i])
                flag=1
            else: 
                Buy.append(np.nan)
        
        elif DATA['MACD'][i] < DATA['Signal'][i]:
            Buy.append(np.nan)
            if flag !=0:
                Sell.append(DATA['Closing Price (USD)'][i])
                flag=0
            else:
                Sell.append(np.nan)
        else:
             Buy.append(np.nan)
             Sell.append(np.nan)    
    return(Buy, Sell)

################################################################################################
'Run rule'
################################################################################################
a = buy_sell(DATA)
DATA['Buy_Signal_Price'] = a[0]
DATA['Sell_Signal_Price'] = a[1]

plt.figure(figsize=(12.2, 4.6))
plt.scatter(DATA.index, DATA['Buy_Signal_Price'], color ='green', label ='Buy', marker ='^', alpha=1)
plt.scatter(DATA.index, DATA['Sell_Signal_Price'], color ='red', label ='Buy', marker ='v', alpha=1)
plt.plot(DATA['Closing Price (USD)'], label = 'Price', alpha = 0.35)
plt.title('Buy and sell signals versus Price')
plt.xlabel('Date')
plt.ylabel('Close Price USD ($)')
plt.legend(loc='upper left')
plt.xticks(rotation = 45)
plt.show()

