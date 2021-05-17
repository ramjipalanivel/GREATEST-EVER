import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import numpy as np


# fetch historical data of the stock starting 1st Jan 2012 till 31st Dec 2017
stock = web.DataReader('MRF.BO','yahoo', start = "01-01-2012", end="31-12-2017")
stock = stock.dropna(how="any")
#plot the adjusted price against time using the matplotlib library
stock['Adj Close'].plot(grid = True)
#plot the daily returns against time
stock['ret'] = stock['Adj Close'].pct_change()
stock['ret'].plot(grid=True)
#plot the moving average of the adjusted close price
stock['20d'] = stock['Adj Close'].rolling(window=20, center=False).mean()
stock['20d'].plot(grid=True)
#Forecast (t) = a + b X t
#'a' is the intercept that time series makes on Y-axis and 'b' is the slope
#Consider a time series with values D(t) for time period 't'.

#In this equation, 'n' is the sample size. We can validate our model by calculating 
#the forecasted values of D(t) using the above model and comparing the values against actual observed values.
#We can compute mean error which is the mean value of the difference between the forecasted D(t) and the actual D(t).
#In our stock data, D(t) is the adjusted closing price of MRF. 
#We will now compute the values of a, b, forecasted values and their errors using python.


#Populates the time period number in stock under head t
stock['t'] = range (1,len(stock)+1)
#Computes t squared, tXD(t) and n
stock['sqr t']=stock['t']**2
stock['tXD']=stock['t']*stock['Adj Close']
n=len(stock)
#Computes slope and intercept
slope = (n*stock['tXD'].sum() - stock['t'].sum()*stock['Adj Close'].sum())/(n*stock['sqr t'].sum() - (stock['t'].sum())**2)
intercept = (stock['Adj Close'].sum()*stock['sqr t'].sum() - stock['t'].sum()*stock['tXD'].sum())/(n*stock['sqr t'].sum() - (stock['t'].sum())**2)
print ('The slope of the linear trend (b) is: ', slope)
print ('The intercept (a) is: ', intercept)


#check the validity of our model by computing the forecasted values and computing the mean error.
#Computes the forecasted values
stock['forecast'] = intercept + slope*stock['t']
#Computes the error
stock['error'] = stock['Adj Close'] - stock['forecast']
mean_error=stock['error'].mean()
print ('The mean error is: ', mean_error)

#model gave results very close to the actual values. Hence, the data is free from any seasonality.