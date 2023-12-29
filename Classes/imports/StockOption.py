from optionprice import Option as Op
import numpy as np

class StockOption:
    def __init__(self,stockobj,strike_price,expiration_date,option_type,leverage=1) -> None:
        self.stockobj = stockobj
        self.strike_price = strike_price
        self.expiration_date = int(expiration_date)
        self.option_type = str(option_type)
        self.leverage = leverage
        self.option = Op(european=True,
                    kind=self.option_type,
                    s0=float(self.stockobj.price*self.leverage),
                    k=self.strike_price*self.leverage,
                    t=self.expiration_date,
                    sigma=self.calculate_volatility(),
                    r=0.05)
        
        self.ogvalue = self.get_value()
        
    
    def calculate_volatility(self):
        points = self.stockobj.graphrangelists['month']
        # Check if there are enough points for calculation
        if len(points) < 2:
            return .1
        # Calculate daily returns
        returns = np.diff(points) / points[:-1]

        # Calculate standard deviation of daily returns
        daily_volatility = np.std(returns)

        # Annualize volatility
        annualized_volatility = np.sqrt(252) * daily_volatility

        return annualized_volatility
    def set_leverage(self,leverage):
        self.leverage = leverage

    def get_inputs(self):
        return (self.option_type,self.stockobj.price*self.leverage,self.strike_price*self.leverage,self.expiration_date,self.calculate_volatility(),0.05)
    # create a method to return an exact copy of the object
    def get_copy(self,leverage=1) -> 'StockOption':        
        return StockOption(self.stockobj,self.strike_price,self.expiration_date,self.option_type,leverage)
    def advance_time(self):
        self.expiration_date -= 1
        self.option.t = self.expiration_date

    def get_value(self):
        self.option.s0 = float(self.stockobj.price*self.leverage)
        self.option.k = self.strike_price*self.leverage
        self.option.sigma = self.calculate_volatility()
        # too slow, need to not do it mutliple times a second
        return self.option.getPrice(method="BSM",iteration=1)
    

# Option prices are impacted by 4 major elements i.e. delta, gamma, theta, vega.

# Theta is time decay works in reducing the premium as per the time to expiry.

# Vega is volatility, very difficult to explain, let’s just say option prices increase with the increase in volatility.

# Delta is the ratio of option price change as a percentage of underlying change.
    
# Gamma is the rate of change of delta with respect to the change in the underlying price.
# The massive price change is due to something called Gamma acceleration. Let’s just say that as the option moves nearer to the stock price, it increases faster. Not linearly but exponentially.