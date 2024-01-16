from optionprice import Option as Op
import numpy as np
from collections import deque
from numpy import array_equal
from functools import lru_cache
# ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO']

@lru_cache(maxsize=1000)
def calculate_volatility(points) -> float:
    """Calculate the volatility of a stock, points must be a tuple"""

    if len(points) < 2:
        return .1
    
    # Calculate daily returns
    returns = np.diff(points) / points[:-1]

    # Calculate standard deviation of daily returns
    daily_volatility = np.std(returns)

    # Annualize volatility
    annualized_volatility = np.sqrt(252) * daily_volatility

    return annualized_volatility
    

class StockOption:
    def __init__(self,stockobj,strike_price,expiration_date,option_type,ogprice=None) -> None:
        """Option is controls 100 shares of a stock, so quantity is controlling 100*quantity shares"""
        self.stockobj = stockobj
        self.strike_price = strike_price
        self.expiration_date = int(expiration_date)
        self.option_type = str(option_type)
        self.color = (0,0,0)
        self.name = f'{self.stockobj.name} {self.option_type}'

        self.option = Op(european=True,kind=self.option_type,s0=float(self.stockobj.price)*100,k=self.strike_price*100,t=self.expiration_date,sigma=calculate_volatility(tuple(self.stockobj.graphrangelists['1Y'])),r=0.05)
        if ogprice:
            self.ogvalue = ogprice
        else:
            self.ogvalue = self.option.getPrice(method="MC",iteration=200)

        self.lastvalue = [self.stockobj.price*100,self.get_value(True)]# [stock price, option value] Used to increase performance by not recalculating the option value every time
    
    def __eq__(self,other):
        return [self.stockobj,self.strike_price,self.option_type,self.expiration_date] == [other.stockobj,other.strike_price,other.option_type,other.expiration_date]
    
    def __iadd__(self,other):
        if self == other:
            
            return self
        raise ValueError('The options must be the same')
    
    def self_volatility(self):
        """returns the volatility of the option"""
        return calculate_volatility(tuple(self.stockobj.graphrangelists['1Y']))
        
    def percent_change(self):
        """returns the percent change of the option"""
        return ((self.get_value() - (self.ogvalue)) / (self.ogvalue)) * 100
    def get_inputs(self):
        return (self.option_type,self.stockobj.price,self.strike_price,self.expiration_date,calculate_volatility(tuple(self.stockobj.graphrangelists['1Y'])),0.05,)
    
    # create a method to return an exact copy of the object
    def get_copy(self) -> 'StockOption':        
            return StockOption(self.stockobj,self.strike_price,self.expiration_date,self.option_type,self.get_value(True))
    def resetOgValue(self):
        self.ogvalue = self.get_value(True)
    def advance_time(self):
        self.expiration_date -= 1
        self.option.t = self.expiration_date

    def get_value(self,bypass=False):
        """""Bypass is used to force a recalculation of the option value"""
        if bypass:
            self.option.s0 = float(self.stockobj.price)*100
            self.option.k = self.strike_price*100
            self.option.sigma = calculate_volatility(tuple(self.stockobj.graphrangelists['1Y']))
            
            self.lastvalue = [self.stockobj.price*100,self.option.getPrice(method="BSM",iteration=1)]
            return self.lastvalue[1]
        if ((self.stockobj.price*100)/self.lastvalue[0]) > 1.005 or ((self.stockobj.price*100)/self.lastvalue[0]) < 0.995:# if the stock price has changed by more than 2%
            # print('recalculating option value',bypass)
            self.option.s0 = float(self.stockobj.price)*100
            self.option.k = self.strike_price*100
            self.option.sigma = calculate_volatility(tuple(self.stockobj.graphrangelists['1Y']))
            
            self.lastvalue = [self.stockobj.price*100,self.option.getPrice(method="MC",iteration=200)]
            return self.lastvalue[1]
        return self.lastvalue[1]
    

# Option prices are impacted by 4 major elements i.e. delta, gamma, theta, vega.

# Theta is time decay works in reducing the premium as per the time to expiry.

# Vega is volatility, very difficult to explain, let’s just say option prices increase with the increase in volatility.

# Delta is the ratio of option price change as a percentage of underlying change.
    
# Gamma is the rate of change of delta with respect to the change in the underlying price.
# The massive price change is due to something called Gamma acceleration. Let’s just say that as the option moves nearer to the stock price, it increases faster. Not linearly but exponentially.