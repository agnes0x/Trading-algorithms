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
"4 - Bollinger Bands"
################################################################################################

###Trade Rule: Bollinger bands
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
period = 20
#Simple Moving Average
DATA['SMA'] = DATA['Closing Price (USD)'].rolling(window=period).mean()
#Standard deviation
DATA['STD'] = DATA['Closing Price (USD)'].rolling(window=period).std()
#Upper Band
DATA['Upper'] = DATA['SMA'] + (2 * DATA['STD'] )
#Lower Band
DATA['Lower'] = DATA['SMA'] - (2 * DATA['STD'] )


column_list = ['Closing Price (USD)', 'SMA', 'Upper', 'Lower']
DATA[column_list].plot(figsize=(12.2, 6.4))
plt.title('Bollinger Bands')
plt.xlabel('Date', fontsize =18)
plt.ylabel('Price in USD ($)', fontsize =18)
plt.show(args, kw)
#Plot and shade the area between two Bollinger Bands
 
fig = plt.figure(figsize=(12.2, 6.4))
ax = fig.add_subplot(1,1,1)
# Get the index values of the data frame
x_axis = DATA.index
#plot and shade between upper band and lower
ax.fill_between(x_axis, DATA['Upper'], DATA['Lower'], color = 'grey')
#Plot the price and the moving average
ax.plot(x_axis, DATA['Closing Price (USD)'], color = 'gold', label = 'Price')
ax.plot(x_axis, DATA['SMA'], color = 'blue', label = 'SMA')
ax.title('Bollinger Bands')
ax.set_xlabel('Date')
ax.set_ylabel('Price')
plt.xticks(rotation = 45)
ax.legend()
plt.show()


#Create a new dataframe
new_DATA = DATA[period-1:]



################################################################################################
'Buy and sell'
################################################################################################

def buy_sell(data):
    Buy = []
    Sell = []

    
    for i in range(0, len(DATA['Closing Price (USD)'])):
        if DATA['Close'][i] > DATA['Upper'][i]:
           Sell.append(DATA['Closing Price (USD)'][i])
           Buy.append(np.nan)
         
        elif DATA['Close'][i] > DATA['Lower'][i]:
                Buy.append(DATA['Closing Price (USD)'][i])
                Sell.append(np.nan)        
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