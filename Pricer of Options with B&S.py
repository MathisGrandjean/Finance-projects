"Pricer of Options thanks to the Black-Scholes Formula"

import yfinance as yf
from scipy.stats import norm
import numpy as np 

apple_ticker = yf.Ticker("AAPL")
df = apple_ticker.history(period="1y") 
print(df.head())

class actif:
    
    ''' We develop a class of actif and several methods in order to have the price of a call and a put
        d1 and d2 are variables that are used in the Black-Scholes Formulas
        
        To calcultate the volatily, we used the logaritmic return 
    '''
        
    def __init__(self,price,strike,time,risk_free):
        self.price=price
        self.strike=strike
        self.time=time 
        self.risk_free=risk_free
    
    def info(self):
        print(self.price,self.strike,self.time)
        
    def volatility(self):
        log_returns = np.log(df['High'] / df['High'].shift(1))
        vol = np.std(log_returns)  
        vol_annualized = vol * np.sqrt(252) 
        return vol_annualized
    
    def d1(self):
        vol = self.volatility()
        return (np.log(self.price / self.strike) + (self.risk_free + 0.5 * vol**2) * self.time) / (vol * np.sqrt(self.time))

    def d2(self):
        return self.d1() - self.volatility() * np.sqrt(self.time)
    
    def call(self):
        d1_value = self.d1()
        d2_value = self.d2()
        C = (self.price * norm.cdf(d1_value) - 
             self.strike * np.exp(-self.risk_free * self.time) * norm.cdf(d2_value))
        return C
    
    def put(self):
        d1_value = self.d1()
        d2_value = self.d2()
        P = (self.strike * np.exp(-self.risk_free * self.time) * norm.cdf(-d2_value) - 
             self.price * norm.cdf(-d1_value))
        return P
        
        
apple=actif(df['High'].iloc[1],df['High'].mean(),1,0.01)


apple.volatility()
apple.d1()
apple.d2()
print(apple.call())
print(apple.put())
