from optionprice import Option as Op
import numpy as np
from collections import deque
from numpy import array_equal
# ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO']
recentcalculations = {}# key is value of volatility: value is the list of points

def calculate_volatility(points) -> float:
    """Calculate the volatility of a stock based on the last 100 points"""
    global recentcalculations
    if len(points) > 100:
        points = points[-100:]

    items = deque(recentcalculations.items())
    for i, (key, value) in enumerate(items):
        if array_equal(value, points):
            
            # Move the item to the beginning of the deque
            items.rotate(-i)
            # Convert the deque back to a dictionary
            recentcalculations = dict(items)
            return items[0][0]
        

    # Check if there are enough points for calculation
    if len(points) < 2:
        return .1
    # Calculate daily returns
    returns = np.diff(points) / points[:-1]

    # Calculate standard deviation of daily returns
    daily_volatility = np.std(returns)

    # Annualize volatility
    annualized_volatility = np.sqrt(252) * daily_volatility

    recentcalculations[annualized_volatility] = points
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

        self.option = Op(european=True,kind=self.option_type,s0=float(self.stockobj.price)*100,k=self.strike_price*100,t=self.expiration_date,sigma=calculate_volatility(self.stockobj.graphrangelists['month']),r=0.05)
        if ogprice:
            self.ogvalue = ogprice
        else:
            self.ogvalue = self.option.getPrice(method="BSM",iteration=1)

        self.lastvalue = [self.stockobj.price*100,self.get_value(True)]# [stock price, option value] Used to increase performance by not recalculating the option value every time
        
        
    def __eq__(self,other):
        return [self.stockobj,self.strike_price,self.option_type,self.expiration_date] == [other.stockobj,other.strike_price,other.option_type,other.expiration_date]
    
    def self_volatility(self):
        """returns the volatility of the option"""
        return calculate_volatility(self.stockobj.graphrangelists['month'])
        
    def percent_change(self):
        """returns the percent change of the option"""
        return ((self.get_value() - (self.ogvalue)) / (self.ogvalue)) * 100
    def get_inputs(self):
        return (self.option_type,self.stockobj.price,self.strike_price,self.expiration_date,calculate_volatility(self.stockobj.graphrangelists['month']),0.05,)
    
    # create a method to return an exact copy of the object
    def get_copy(self,quantity=1) -> 'StockOption':        
            return StockOption(self.stockobj,self.strike_price,self.expiration_date,self.option_type,quantity)
    
    def advance_time(self):
        self.expiration_date -= 1
        self.option.t = self.expiration_date

    def get_value(self,bypass=False):
        """""Bypass is used to force a recalculation of the option value"""
        if bypass or (self.stockobj.price/self.lastvalue[0]) > 1.01 or (self.stockobj.price/self.lastvalue[0]) < 0.99:# if the stock price has changed by more than 2%
            self.option.s0 = float(self.stockobj.price)*100
            self.option.k = self.strike_price*100
            self.option.sigma = calculate_volatility(self.stockobj.graphrangelists['month'])
            
            self.lastvalue = [self.stockobj.price*100,self.option.getPrice(method="BSM",iteration=1)]
            return self.lastvalue[1]
        return self.lastvalue[1]
    

# Option prices are impacted by 4 major elements i.e. delta, gamma, theta, vega.

# Theta is time decay works in reducing the premium as per the time to expiry.

# Vega is volatility, very difficult to explain, let’s just say option prices increase with the increase in volatility.

# Delta is the ratio of option price change as a percentage of underlying change.
    
# Gamma is the rate of change of delta with respect to the change in the underlying price.
# The massive price change is due to something called Gamma acceleration. Let’s just say that as the option moves nearer to the stock price, it increases faster. Not linearly but exponentially.