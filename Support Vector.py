
####
"Predict with Machine Learning"
"https://www.youtube.com/watch?v=C64BIMx7Slw&t=768s"
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



#############################################
#get the number of rows and columns
DATA.shape

# use (n-1) rows to train the model. Then use model the predict the n-th day.

#save the last datapoint sepreately - dependent
actual_price = DATA.tail(1)
actual_price

#screate new list without last datapoint - independent
DATA2 = DATA.head(len(DATA)-1)
DATA2


#Create empty list to store independent and dependent data
days = list()
prices = list()

#get the data
DATA_days = DATA2.loc[:,'Date']
DATA_price = DATA2.loc[:,'Closing Price (USD)']

DATA_days

#Create the the independent data set
for d in DATA_days:
    days.append([int(d.split('-')[2])])
    #probably a better solution is to store date as number 6794 or something
#create dependent data set
for p in DATA_price:
    prices.append(float(p))
    
days
prices
############
#Create the 3 Support Vector Regression Model

#create and train a SVR model using a linear kernel
lin_SVR = SVR(kernel = 'linear', C=1000.0)
lin_SVR.fit(days, prices)


#create and train a SVR model using a polynomial kernel
poly_SVR = SVR(kernel = 'poly', C=1000.0, degree = 2)
poly_SVR.fit(days, prices)


#create and train a SVR model using a rbf kernel
rbf_SVR = SVR(kernel = 'rbf', C=1000.0, gamma=0.15)
rbf_SVR.fit(days, prices)
##########

# plot the models to see which has the best fit to the orignial data

plt.figure(figsize=(16,8))
plt.scatter(DATA2.index, prices, color = 'red', label ='data')
plt.plot(DATA2.index,lin_SVR.predict(days), color = 'green', label ='RBF model')
plt.plot(DATA2.index,poly_SVR.predict(days), color = 'orange', label ='Polynomial model')
plt.plot(DATA2.index, rbf_SVR.predict(days), color = 'blue', label ='Linear model')
plt.legend()
plt.show()

#
day = [[31]]
rbf_svr.preditct(day)
lin_SVR.predict(days)
poly_SVR.predict(days)
actual_price
