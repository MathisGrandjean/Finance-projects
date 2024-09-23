"pricer option vanille"

import yfinance as yf
import pandas as pd
from scipy.stats import norm
import numpy as np 

apple_ticker = yf.Ticker("AAPL")

df = apple_ticker.history(period="1y") 
print(df.head())

class actif:
    def __init__(self,price,strike,time,risk_free):
        self.price=price
        self.strike=strike
        self.time=time 
        self.risk_free=risk_free
    
    def info(self):
        print(self.price,self.strike,self.time)
        
    def volatility(self):
        log_return_year=np.zeros(len(df['High'])-1)
        for i in range(1,len(df['High'])):
            log_return =np.log( df['High'].iloc[i]/df['High'].iloc[i-1])
            log_return_year[i-1]=log_return
            diff_return=0
        for i in range(len(log_return_year)):
            diff_return=diff_return+(log_return_year[i]-log_return_year.mean())**2
        vol=np.sqrt(1/(len(df['High'])-1)*diff_return)
        vol_annualized=vol*np.sqrt(252)
        return vol_annualized
    
    def d1(self):
        num=np.log(self.price/self.strike)+(self.risk_free+((self.volatility()**2)/2)*self.time)
        den=np.sqrt(self.volatility())*self.time
        return num/den

    def d2(self):
        return self.d1()-self.volatility()*np.sqrt(self.time)
    
    def call(self):
        d1_normal= norm.cdf(self.d1(),0,1)
        d2_normal= norm.cdf(self.d2(),0,1)
        C=self.price*d1_normal- self.strike*np.exp(-self.risk_free*self.time)*d2_normal
        return C
        
apple=actif(df['High'].iloc[1],df['High'].mean(),1,0.01)


apple.volatility()
apple.d1()
apple.d2()
print(apple.call())
