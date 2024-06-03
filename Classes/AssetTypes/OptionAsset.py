from optionprice import Option as Op
from Classes.AssetTypes.Asset import Asset
import numpy as np
from collections import deque
# ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO']


    
class OptionAsset(Asset):
    def __init__(self,player,stockobj,strikePrice:int,expiration_date:int,option_type:str,creationdate:str,quantity:int,porfolioPercent=None,ogprice=None,color=None) -> None:
        super().__init__(player,stockobj, creationdate, " "+option_type, ogprice, quantity, porfolioPercent, color=color)
        
        self.strikePrice = strikePrice
        self.expiration_date = expiration_date
        self.option_type = option_type
        self.option = Op(european=True,kind=self.option_type,s0=float(self.stockobj.price)*100,k=self.strikePrice*100,t=self.expiration_date,sigma=self.getVolatility(),r=0.05)
        ogprice = ogprice if ogprice else self.getValue(bypass=True,fullvalue=True)
        # print(f"{self.name}, {porfolioPercent} {self.portfolioPercent}")
        if porfolioPercent == None:
            
            self.portfolioPercent = ogprice/(player.getNetworth())# have to set this after the object is created
            # print(f"dont, {self.portfolioPercent}, {ogprice} {networth}") 
            
        self.lastvalue = [self.stockobj.price*100,self.getValue(bypass=True,fullvalue=False)]# [stock price, option value] Used to increase performance by not recalculating the option value every time
        self.updateCount = 0

    def __eq__(self,other):
        if not isinstance(other,OptionAsset):
            return False
        return [self.stockobj,self.strikePrice,self.option_type,self.expiration_date,self.date,self.ogvalue,self.portfolioPercent] == [other.stockobj,other.strikePrice,other.option_type,other.expiration_date,other.date,other.ogvalue,self.portfolioPercent]

    def __iadd__(self,other):
        if self == other:
            extraValue = (other.getValue(bypass=True)+self.getValue(bypass=True))
            self.portfolioPercent = extraValue/(self.playerObj.getNetworth()+other.getValue(bypass=True))
            self.quantity += other.quantity
            return self
        raise ValueError(f'{type(self).__name__} objects must be the same to add them together')

    def savingInputs(self):
        return (self.stockobj.name,self.strikePrice,self.expiration_date,self.option_type,self.date,self.quantity,self.portfolioPercent,self.ogvalue,self.color)


    def copy(self):
        return OptionAsset(self.playerObj,self.stockobj,self.strikePrice,self.expiration_date,self.option_type,str(self.date),self.quantity,self.portfolioPercent,ogprice=self.getValue(bypass=True))

    def getValue(self,bypass=False,fullvalue=True):
        """""Bypass is used to force a recalculation of the option value
        Full value is value*quantity otherwise it is just the value of the option"""
        if bypass:
            self.option.s0 = float(self.stockobj.price)*100
            self.option.k = self.strikePrice*100
            self.option.sigma = self.getVolatility()
            
            self.lastvalue = [self.stockobj.price*100,self.option.getPrice(method="BSM",iteration=1)]
            return (self.lastvalue[1] * self.quantity) if fullvalue else self.lastvalue[1]
        # if ((self.stockobj.price*100)/self.lastvalue[0]) > 1.001 or ((self.stockobj.price*100)/self.lastvalue[0]) < 0.999:# if the stock price has changed by more than 2%
        # print("percent",abs((self.stockobj.price*100)-self.lastvalue[0])/self.lastvalue[0],abs((self.stockobj.price*100)-self.lastvalue[0]))
        # if self.updateCount > 60:# if the stock price has changed by more than 2%
        #     # print('recalculating option value',bypass)
        #     self.option.s0 = float(self.stockobj.price)*100
        #     self.option.k = self.strikePrice*100
        #     self.option.sigma = self.getVolatility()
            
        #     self.lastvalue = [self.stockobj.price*100,self.option.getPrice(method="MC",iteration=200)]
        #     return (self.lastvalue[1] * self.quantity) if fullvalue else self.lastvalue[1]
 
        return (self.lastvalue[1] * self.quantity) if fullvalue else self.lastvalue[1]

# class OptionAsset:
#     def __init__(self,stockobj,strikePrice,expiration_date,option_type,creationdate,quantity=1,ogprice=None) -> None:
#         """Option is controls 100 shares of a stock, so quantity is controlling 100*quantity shares"""
#         self.stockobj = stockobj
#         self.date = creationdate
#         self.strikePrice = strikePrice
#         self.expiration_date = int(expiration_date)
#         self.option_type = str(option_type)
#         self.color = (0,0,0)
#         self.name = f'{self.stockobj.name} {self.option_type}'
#         self.quantity = quantity

#         self.option = Op(european=True,kind=self.option_type,s0=float(self.stockobj.price)*100,k=self.strikePrice*100,t=self.expiration_date,sigma=calculate_volatility(tuple(self.stockobj.graphs['1Y'])),r=0.05)
        # if ogprice:
        #     self.ogvalue = ogprice
        # else:
        #     self.ogvalue = self.option.getPrice(method="BSM",iteration=1)

#         self.lastvalue = [self.stockobj.price*100,self.getValue(bypass=True,fullvalue=False)]# [stock price, option value] Used to increase performance by not recalculating the option value every time
    
#     def __str__(self) -> str:
#         return f'{self.name}'
    
    # def __eq__(self,other):
    #     if not isinstance(other,OptionAsset):
    #         return False
    #     return [self.stockobj,self.strikePrice,self.option_type,self.expiration_date,self.date] == [other.stockobj,other.strikePrice,other.option_type,other.expiration_date,other.date]
    
#     def __iadd__(self,other):
        
#         if self == other:
#             self.quantity += other.quantity
#             self.ogvalue += other.ogvalue
#             return self
#         raise ValueError('StockOption objects must be the same to add them together')

    
    # def self_volatility(self):
    #     """returns the volatility of the option"""
    #     return calculate_volatility(tuple(self.stockobj.graphs['1Y']))
        
#     def percent_change(self):
#         """returns the percent change of the option"""
#         return ((self.getValue() - (self.ogvalue)) / (self.ogvalue)) * 100
#     def get_inputs(self):
#         return (self.option_type,self.stockobj.price,self.strikePrice,self.expiration_date,calculate_volatility(tuple(self.stockobj.graphs['1Y'])),0.05,)
    
#     # create a method to return an exact copy of the object
#     def copy(self) -> 'OptionAsset':        
#             return OptionAsset(self.stockobj,self.strikePrice,self.expiration_date,self.option_type,self.date,quantity=self.quantity,ogprice=self.getValue(bypass=True))
#     def resetOgValue(self):
#         self.ogvalue = self.getValue(True)
#     def advance_time(self):
#         self.expiration_date -= 1
#         self.option.t = self.expiration_date
#     def sell(self,player,_,quantity):
#         """sells the option, need this so I can call a generic .sell for each asset in portfolio"""
#         player.sellOption(self,quantity)

    # def getValue(self,bypass=False,fullvalue=True):
    #     """""Bypass is used to force a recalculation of the option value
    #     Full value is value*quantity otherwise it is just the value of the option"""
    #     if bypass:
    #         self.option.s0 = float(self.stockobj.price)*100
    #         self.option.k = self.strikePrice*100
    #         self.option.sigma = calculate_volatility(tuple(self.stockobj.graphs['1Y']))
            
    #         self.lastvalue = [self.stockobj.price*100,self.option.getPrice(method="BSM",iteration=1)]
    #         return (self.lastvalue[1] * self.quantity) if fullvalue else self.lastvalue[1]
    #     if ((self.stockobj.price*100)/self.lastvalue[0]) > 1.001 or ((self.stockobj.price*100)/self.lastvalue[0]) < 0.999:# if the stock price has changed by more than 2%
    #         # print('recalculating option value',bypass)
    #         self.option.s0 = float(self.stockobj.price)*100
    #         self.option.k = self.strikePrice*100
    #         self.option.sigma = calculate_volatility(tuple(self.stockobj.graphs['1Y']))
            
    #         self.lastvalue = [self.stockobj.price*100,self.option.getPrice(method="MC",iteration=200)]
    #         return (self.lastvalue[1] * self.quantity) if fullvalue else self.lastvalue[1]
    #     return (self.lastvalue[1] * self.quantity) if fullvalue else self.lastvalue[1]
    

# Option prices are impacted by 4 major elements i.e. delta, gamma, theta, vega.

# Theta is time decay works in reducing the premium as per the time to expiry.

# Vega is volatility, very difficult to explain, let’s just say option prices increase with the increase in volatility.

# Delta is the ratio of option price change as a percentage of underlying change.
    
# Gamma is the rate of change of delta with respect to the change in the underlying price.
# The massive price change is due to something called Gamma acceleration. Let’s just say that as the option moves nearer to the stock price, it increases faster. Not linearly but exponentially.