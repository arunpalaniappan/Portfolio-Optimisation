import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import fix_yahoo_finance as yf
import datetime as dt

#list of stocks in portfolio
stocks = ['AAPL','AMZN','MSFT','GM']

#download daily price data for each of the stocks in the portfolio
##start = dt.datetime(2012,5,31)
##stock_prices = {}
##
##for i in stocks:
##    try:
##        stock_prices[i] = yf.download(i,start = start)['Adj Close']
##    except ValueError:
##        print ('The stock data is currently not available')

data = pd.read_csv('data.csv')
data.sort_index(inplace=True)

del data['Date']

##convert daily stock prices into daily returns
returns = data.pct_change()

##calculate mean daily return and covariance of daily returns
mean_daily_returns = returns.mean()
cov_matrix = returns.cov()

##set number of runs of random portfolio weights
num_portfolios = 25000

results = np.zeros((4+len(stocks)-1,num_portfolios))

for i in range(num_portfolios):
    #select random weights for portfolio holdings
    weights = np.array(np.random.random(4))
    #rebalance weights to sum to 1
    weights /= np.sum(weights)
    
    #calculate portfolio return and volatility
    portfolio_return = np.sum(mean_daily_returns * weights) * 252
    portfolio_std_dev = np.sqrt(np.dot(weights.T,np.dot(cov_matrix, weights))) * np.sqrt(252)
    
    #store results in results array
    results[0,i] = portfolio_return
    results[1,i] = portfolio_std_dev
    #Sharpe Ratio (return / volatility)
    results[2,i] = results[0,i] / results[1,i]
    for j in range(len(weights)):
        results[j+3,i] = weights[j]

#convert results array to Pandas DataFrame
results_frame = pd.DataFrame(results.T,columns=['ret','stdev','sharpe',stocks[0],stocks[1],stocks[2],stocks[3]])

#locate position of portfolio with highest Sharpe Ratio
max_sharpe_point = results_frame.iloc[results_frame['sharpe'].idxmax()]
#locate positon of portfolio with minimum standard deviation
min_vol_point = results_frame.iloc[results_frame['stdev'].idxmin()]

#create scatter plot coloured by Sharpe Ratio
plt.scatter(results_frame.stdev,results_frame.ret,c=results_frame.sharpe,cmap='RdYlBu')
plt.xlabel('Volatility')
plt.ylabel('Returns')
plt.colorbar()

#plot red star to highlight position of portfolio with highest Sharpe Ratio
plt.scatter(max_sharpe_point[1],max_sharpe_point[0],marker=(5,1,0),color='r',s=1000)
#plot green star to highlight position of minimum variance portfolio
plt.scatter(min_vol_point[1],min_vol_point[0],marker=(5,1,0),color='g',s=1000)
plt.show()
