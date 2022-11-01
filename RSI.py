################################################################################################
"Libraries"
################################################################################################
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

# Replace the default row index of the panda dataframe with Date from csv.

DATA = DATA.set_index(pd.DatetimeIndex(DATA['Date'].values))
DATA

#Visualize the data
plt.figure(figsize=(12.5,4.5))
plt.plot(DATA['Closing Price (USD)'], label = 'closing price')
plt.title('Price over the years')
plt.xlabel('2013 - 2021 ', fontsize =18)
plt.ylabel('Price in USD ($)', fontsize =18)
plt.legend(loc='upper left')
plt.show()
plt.draw()

################################################################################################
"2 - RSI"
################################################################################################
###Trade Rule: Relative Strength Index (RSI)
##determine whether an asset is over sold or over bought
#common 14 days

#Get the difference in price. Today vs previous day -> diff is one.
delta = DATA['Closing Price (USD)'].diff(1)
delta

#Get rid of nan values. (diff cannot be calculated for the first day)
delta = delta.dropna()
delta

#Get a list for positive and negative gains
#duplicate original
up = delta.copy()
down = delta.copy()
#replace values that dont belong with a 0
up[up<0] = 0
#up now only contains positive values
down[down>0] =0
#down only contains negative values

#Get the time period
period = 14
#Calculate average gain and average loss
AVG_Gain =up.rolling(window=period).mean()
AVG_Loss =abs(down.rolling(window=period).mean())

#Calculate the Relative Strength (RS)
RS = AVG_Gain  / AVG_Loss

# Calculate the relative strength index (RSI)
RSI = 100.0 - (100.0/(1.0+RS))


#Visualize Results
plt.figure(figsize=(12.5,4.5))
RSI.plot()
plt.show()


#Analyse
#Create a new dataframe
new_df = pd.DataFrame()
new_df['Closing Price (USD)'] = DATA['Closing Price (USD)']
new_df['RSI'] = RSI

#Visualize price
plt.figure(figsize=(12.5,4.5))
plt.plot(new_df.index, new_df['Closing Price (USD)'])
plt.title('Price over the years')
plt.legend(new_df.columns.values,loc='upper left')
plt.show()

#Visualize RSI
plt.figure(figsize=(12.5,4.5))
plt.plot(new_df.index, new_df['RSI'])
plt.title('RSI over the years')
#significant level indicators for RFSI graph
plt.axhline(0, linestyle = "--", alpha = 0.5, color = 'gray')
plt.axhline(10, linestyle = "--", alpha = 0.5, color = 'orange')
plt.axhline(20, linestyle = "--", alpha = 0.5, color = 'green')
plt.axhline(30, linestyle = "--", alpha = 0.5, color = 'red')
plt.axhline(70, linestyle = "--", alpha = 0.5, color = 'red')
plt.axhline(80, linestyle = "--", alpha = 0.5, color = 'green')
plt.axhline(90, linestyle = "--", alpha = 0.5, color = 'orange')
plt.axhline(100, linestyle = "--", alpha = 0.5, color = 'gray')
plt.show()

