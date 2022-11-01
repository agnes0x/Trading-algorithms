"using dual moving average crossover to determiine when to buy and sell"
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Load the data

DATA =pd.read_csv("BTC.csv")
DATA

#Visualize the data
plt.figure(figsize=(12.5,4.5))
plt.plot(DATA['Closing Price (USD)'], label = 'closing price')
plt.title('Price over the years')
plt.xlabel('2013 - 2021 ')
plt.ylabel('Price')
plt.legend(loc='upper left')
plt.show()
plt.draw()

#Momentum
###Trade Rule: Dual Moving Average Crossover
#Signal: Whenever the short term average crosses the longterm average
#buy: after crossing, shorterm exceeds longterm
#sell: after crossing, shortterm falls below longterm

#Create the short term average
#SMA30
#Create a simple moving average (SMA) with a 30 day window
SMA30 = pd.DataFrame()
SMA30['Closing Price (USD)']=DATA['Closing Price (USD)'].rolling(window=30).mean()


#Create Long term average
#SMA100
#Create a simple moving average (SMA) with a 100 day window
SMA100 = pd.DataFrame()
SMA100['Closing Price (USD)']=DATA['Closing Price (USD)'].rolling(window=100).mean()

#Visualize the data



plt.figure(figsize=(12.5,4.5))
plt.plot(DATA['Date'], DATA['Closing Price (USD)'], label = 'Closing Price')
plt.plot(DATA['Date'], SMA30['Closing Price (USD)'], label = 'SMA30)')
plt.plot(DATA['Date'], SMA100['Closing Price (USD)'], label = 'SMA100' )
plt.title('Price over the years')
plt.xlabel('2013 - 2021 ')
plt.ylabel('Closing Price USD ($)')
plt.legend(loc='upper left')
plt.show()

#Create a new data frame to store 
data2 = pd.DataFrame()
data2['CryptoCurrency'] = DATA['Closing Price (USD)']
data2['SMA30'] = SMA30['Closing Price (USD)']
data2['SMA100'] = SMA100['Closing Price (USD)']

#Create a function to signal when to buy and sell asset/stock
def buy_sell(data):
    signalPriceToBuy = []
    signalPriceToSell = []
    flag = -1
    
    for i in range(len(data2)):
        if data2['SMA30'][i]> data2['SMA100'][i]:
            if flag !=1:
                signalPriceToBuy.append(data2['CryptoCurrency'][i])
                signalPriceToSell.append(np.nan)
                flag=1
            else: 
                signalPriceToBuy.append(np.nan)
                signalPriceToSell.append(np.nan)
        
        elif data2['SMA30'][i] < data2['SMA100'][i]:
            if flag !=0:
                signalPriceToBuy.append(np.nan)
                signalPriceToSell.append(data2['CryptoCurrency'][i])
                flag=0
            else: 
                signalPriceToBuy.append(np.nan)
                signalPriceToSell.append(np.nan)
        else:
             signalPriceToBuy.append(np.nan)
             signalPriceToSell.append(np.nan)
             
    return(signalPriceToBuy, signalPriceToSell)

#Store the buy and sell data into a variable
buy_sell = buy_sell(DATA)
data2['Buy_Signal_Price'] = buy_sell[0]
data2['Sell_Signal_Price'] = buy_sell[1]

#Show the data
data2

#Visualize the data and the strategy to buy and sell
plt.figure(figsize=(12.6,4.6))
plt.plot(data2['CryptoCurrency'], label = 'CC', alpha =0.35)
plt.plot(data2['SMA30'], label = 'SMA30', alpha =0.35)
plt.plot(data2['SMA100'], label = 'SMA100', alpha =0.35)
plt.scatter(data2.index, data2['Buy_Signal_Price'], label = 'Buy', marker ='^', color='green' )
plt.scatter(data2.index, data2['Sell_Signal_Price'], label = 'Sell', marker ='^', color='red' )
plt.title("Cryptocurrency Price History, Buy, and Sell Signals")
plt.xlabel("2011 - 2021")
plt.ylabel('Close Price USD ($)')
plt.legend(loc='upper left')
plt.show()


