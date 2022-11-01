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

###Trade Rule: 3 Moving Average Crossover (3MAC) - short, medium, long exponential moving average
#Signal: Difference between exponentially moving averages to determine momentum and direction
#short term: 5 period
#middle term: 21 period
#long term: 63 period
    
#buy: MACD line above the signal line
#sell: MACD line below the signal line
#signal line: 9 period
#Macd line: short term exp. moving avg. (ShortEMA)- long term exp. moving avg. (LongMEA)
#short term: typically 12 periods
#long term: typically 26 period


################################################################################################
'Calculate'
################################################################################################

ShortEMA = DATA['Closing Price (USD)'].ewm(span=5, adjust=False).mean()
MiddleEMA = DATA['Closing Price (USD)'].ewm(span=21, adjust=False).mean()
LongEMA = DATA['Closing Price (USD)'].ewm(span=63, adjust=False).mean()

#Visualize the data
plt.figure(figsize=(12.5,4.5))
plt.plot(DATA['Closing Price (USD)'], label = 'closing price', color = 'blue')
plt.plot(ShortEMA, label ='Short', color = 'red')
plt.plot(MiddleEMA,label ='Middle', color = 'orange')
plt.plot(LongEMA,label ='Long', color = 'green')
plt.title('Price over the years')
plt.xlabel('Date', fontsize =18)
plt.ylabel('Price in USD ($)', fontsize =18)
plt.xticks(rotation = 45)
plt.legend(loc='upper left')
plt.show()
plt.draw()


DATA['Short']= ShortEMA
DATA['Middle']= MiddleEMA
DATA['Long']= LongEMA

################################################################################################
'Buy and sell'
################################################################################################

def buy_sell(data):
    Buy = []
    Sell = []
    flag_long = False
    flag_short = False
    
    for i in range(0, len(DATA)):
        if DATA['Middle'][i] < DATA['Long'][i] and DATA['Short'][i] < DATA['Middle'][i] and flag_long == False and flag_short == False :
           Buy.append(DATA['Closing Price (USD)'][i])
           Sell.append(np.nan)
           flag_short = True
           
        elif flag_short ==True and  DATA['Short'][i] > DATA['Middle'][i]:
                Sell.append(DATA['Closing Price (USD)'][i])
                Buy.append(np.nan)
                flag_short = False
                
        if DATA['Middle'][i] > DATA['Long'][i] and DATA['Short'][i] > DATA['Middle'][i] and flag_long == False and flag_short == False :
           Buy.append(DATA['Closing Price (USD)'][i])
           Sell.append(np.nan)
           flag_long = True
           
        elif flag_long == True and  DATA['Short'][i] < DATA['Middle'][i]:
                Sell.append(DATA['Closing Price (USD)'][i])
                Buy.append(np.nan)
                flag_long = False     
                
        else:
            Buy.append(np.nan)
            Sell.append(np.nan)
    
    return(Buy, Sell)

################################################################################################
'Results'
################################################################################################
a =  buy_sell(DATA)
DATA.shape
#here errror: ValueError: Length of values does not match length of index
DATA['Buy_Signal_Price'] = buy_sell(DATA)[0]
DATA['Sell_Signal_Price'] = buy_sell(DATA)[1]

#Visualize the data
plt.figure(figsize=(12.5,4.5))
plt.plot(DATA['Closing Price (USD)'], label = 'closing price', color = 'blue')
plt.plot(ShortEMA, label ='Short', color = 'red')
plt.plot(MiddleEMA,label ='Middle', color = 'orange')
plt.plot(LongEMA,label ='Long', color = 'green')
plt.scatter(DATA.index, DATA['Buy_Signal_Price'], color ='green', label ='Buy', marker ='^', alpha=1)
plt.scatter(DATA.index, DATA['Sell_Signal_Price'], color ='red', label ='Buy', marker ='v', alpha=1)
plt.title('Price over the years')
plt.xlabel('Date', fontsize =18)
plt.ylabel('Price in USD ($)', fontsize =18)
plt.xticks(rotation = 45)
plt.legend(loc='upper left')
plt.show()
plt.draw()