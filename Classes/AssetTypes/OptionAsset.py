from optionprice import Option as Op
from Classes.AssetTypes.Asset import Asset
import numpy as np
from collections import deque
import datetime
# ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO']
DFORMAT = "%m/%d/%Y"
myOption = Op(european=True,kind="put",s0=9543.754571035066,k=10024.0,t=208,sigma=.154,r=0.05)
print(myOption.getPrice(method="BSM",iteration=1))
    
class OptionAsset(Asset):
    def __init__(self,player,stockObj,strikePrice:int,expirationDate:datetime.datetime,optionType:str,creationDate:str,quantity:int,porfolioPercent=None,ogPrice=None,color=None) -> None:
        super().__init__(player,stockObj, creationDate, " "+optionType, ogPrice, quantity, porfolioPercent, color=color)
        
        self.gametime : datetime.datetime = player.gametime
        self.strikePrice = strikePrice
        self.expirationDate = datetime.datetime.strptime(expirationDate, "%Y-%m-%d %H:%M:%S")
        self.optionType = optionType
    
        self.option = Op(european=True,kind=self.optionType,s0=float(self.stockObj.price)*100,k=self.strikePrice*100,t=self.daysToExpiration(self.gametime.time),sigma=self.getVolatility(),r=0.05)
        ogPrice = ogPrice if ogPrice else self.getValue(bypass=True,fullvalue=True)
        
        # print(f"{self.name}, {porfolioPercent} {self.portfolioPercent}")
        if porfolioPercent == None:
            
            self.portfolioPercent = ogPrice/(player.getNetworth())# have to set this after the object is created
            # print(f"dont, {self.portfolioPercent}, {ogPrice} {networth}") 
            
        self.lastvalue = self.getValue(bypass=True,fullvalue=False)# [stock price, option value] Used to increase performance by not recalculating the option value every time
        
        self.updateCount = 0

    def __eq__(self,other):
        if not isinstance(other,OptionAsset):
            return False
        return [self.stockObj,self.strikePrice,self.optionType,self.expirationDate,self.date,self.ogValue,self.portfolioPercent] == [other.stockObj,other.strikePrice,other.optionType,other.expirationDate,other.date,other.ogValue,self.portfolioPercent]

    def __iadd__(self,other):
        if self == other:
            extraValue = (other.getValue(bypass=True)+self.getValue(bypass=True))
            self.portfolioPercent = extraValue/(self.playerObj.getNetworth()+other.getValue(bypass=True))
            self.quantity += other.quantity
            return self
        raise ValueError(f'{type(self).__name__} objects must be the same to add them together')
    def getStrike(self): return self.strikePrice
    def getType(self): return self.optionType
    
    def savingInputs(self):
        return (self.stockObj.name,self.strikePrice,str(self.expirationDate),self.optionType,self.date,self.quantity,self.portfolioPercent,self.ogValue,self.color)
    def getExpDate(self):
        return self.expirationDate.strftime(DFORMAT)
    def daysToExpiration(self,gametimeTime:datetime.datetime):
        assert isinstance(gametimeTime,datetime.datetime), "gametimeTime must be a datetime object Use .time"
        return (self.expirationDate - gametimeTime).days
    
    def copy(self):
        return OptionAsset(self.playerObj,self.stockObj,self.strikePrice,str(self.expirationDate),self.optionType,str(self.date),self.quantity,self.portfolioPercent,ogPrice=self.getValue(bypass=True))

    def getValue(self,bypass=False,fullvalue=True):
        """""Bypass is used to force a recalculation of the option value
        Full value is value*quantity otherwise it is just the value of the option"""
        
        if bypass or self.updateCount > 60:
            self.option.s0 = float(self.stockObj.price)*100
            self.option.sigma = self.getVolatility()
            self.option.t = self.daysToExpiration(self.gametime.time)/365
  
            self.option.t = self.option.t if self.option.t > 0 else 0

            self.updateCount = 0

            self.lastvalue = self.option.getPrice(method="BSM",iteration=1)
            return (self.lastvalue * self.quantity) if fullvalue else self.lastvalue

        # if ((self.stockObj.price*100)/self.lastvalue[0]) > 1.001 or ((self.stockObj.price*100)/self.lastvalue[0]) < 0.999:# if the stock price has changed by more than 2%
        # print("percent",abs((self.stockObj.price*100)-self.lastvalue[0])/self.lastvalue[0],abs((self.stockObj.price*100)-self.lastvalue[0]))
        # if self.updateCount > 60:# if the stock price has changed by more than 2%
        #     # print('recalculating option value',bypass)
        #     self.option.s0 = float(self.stockObj.price)*100
        #     self.option.k = self.strikePrice*100
        #     self.option.sigma = self.getVolatility()
            
        #     self.lastvalue = [self.stockObj.price*100,self.option.getPrice(method="MC",iteration=200)]
        #     return (self.lastvalue[1] * self.quantity) if fullvalue else self.lastvalue[1]
        self.updateCount += 1
        return (self.lastvalue * self.quantity) if fullvalue else self.lastvalue

# class OptionAsset:
#     def __init__(self,stockObj,strikePrice,expirationDate,optionType,creationDate,quantity=1,ogPrice=None) -> None:
#         """Option is controls 100 shares of a stock, so quantity is controlling 100*quantity shares"""
#         self.stockObj = stockObj
#         self.date = creationDate
#         self.strikePrice = strikePrice
#         self.expirationDate = int(expirationDate)
#         self.optionType = str(optionType)
#         self.color = (0,0,0)
#         self.name = f'{self.stockObj.name} {self.optionType}'
#         self.quantity = quantity

#         self.option = Op(european=True,kind=self.optionType,s0=float(self.stockObj.price)*100,k=self.strikePrice*100,t=self.expirationDate,sigma=calculate_volatility(tuple(self.stockObj.graphs['1Y'])),r=0.05)
        # if ogPrice:
        #     self.ogValue = ogPrice
        # else:
        #     self.ogValue = self.option.getPrice(method="BSM",iteration=1)

#         self.lastvalue = [self.stockObj.price*100,self.getValue(bypass=True,fullvalue=False)]# [stock price, option value] Used to increase performance by not recalculating the option value every time
    
#     def __str__(self) -> str:
#         return f'{self.name}'
    
    # def __eq__(self,other):
    #     if not isinstance(other,OptionAsset):
    #         return False
    #     return [self.stockObj,self.strikePrice,self.optionType,self.expirationDate,self.date] == [other.stockObj,other.strikePrice,other.optionType,other.expirationDate,other.date]
    
#     def __iadd__(self,other):
        
#         if self == other:
#             self.quantity += other.quantity
#             self.ogValue += other.ogValue
#             return self
#         raise ValueError('StockOption objects must be the same to add them together')

    
    # def self_volatility(self):
    #     """returns the volatility of the option"""
    #     return calculate_volatility(tuple(self.stockObj.graphs['1Y']))
        
#     def percent_change(self):
#         """returns the percent change of the option"""
#         return ((self.getValue() - (self.ogValue)) / (self.ogValue)) * 100
#     def get_inputs(self):
#         return (self.optionType,self.stockObj.price,self.strikePrice,self.expirationDate,calculate_volatility(tuple(self.stockObj.graphs['1Y'])),0.05,)
    
#     # create a method to return an exact copy of the object
#     def copy(self) -> 'OptionAsset':        
#             return OptionAsset(self.stockObj,self.strikePrice,self.expirationDate,self.optionType,self.date,quantity=self.quantity,ogPrice=self.getValue(bypass=True))
#     def resetOgValue(self):
#         self.ogValue = self.getValue(True)
#     def advance_time(self):
#         self.expirationDate -= 1
#         self.option.t = self.expirationDate
#     def sell(self,player,_,quantity):
#         """sells the option, need this so I can call a generic .sell for each asset in portfolio"""
#         player.sellOption(self,quantity)

    # def getValue(self,bypass=False,fullvalue=True):
    #     """""Bypass is used to force a recalculation of the option value
    #     Full value is value*quantity otherwise it is just the value of the option"""
    #     if bypass:
    #         self.option.s0 = float(self.stockObj.price)*100
    #         self.option.k = self.strikePrice*100
    #         self.option.sigma = calculate_volatility(tuple(self.stockObj.graphs['1Y']))
            
    #         self.lastvalue = [self.stockObj.price*100,self.option.getPrice(method="BSM",iteration=1)]
    #         return (self.lastvalue[1] * self.quantity) if fullvalue else self.lastvalue[1]
    #     if ((self.stockObj.price*100)/self.lastvalue[0]) > 1.001 or ((self.stockObj.price*100)/self.lastvalue[0]) < 0.999:# if the stock price has changed by more than 2%
    #         # print('recalculating option value',bypass)
    #         self.option.s0 = float(self.stockObj.price)*100
    #         self.option.k = self.strikePrice*100
    #         self.option.sigma = calculate_volatility(tuple(self.stockObj.graphs['1Y']))
            
    #         self.lastvalue = [self.stockObj.price*100,self.option.getPrice(method="MC",iteration=200)]
    #         return (self.lastvalue[1] * self.quantity) if fullvalue else self.lastvalue[1]
    #     return (self.lastvalue[1] * self.quantity) if fullvalue else self.lastvalue[1]
    

# Option prices are impacted by 4 major elements i.e. delta, gamma, theta, vega.

# Theta is time decay works in reducing the premium as per the time to expiry.

# Vega is volatility, very difficult to explain, let’s just say option prices increase with the increase in volatility.

# Delta is the ratio of option price change as a percentage of underlying change.
    
# Gamma is the rate of change of delta with respect to the change in the underlying price.
# The massive price change is due to something called Gamma acceleration. Let’s just say that as the option moves nearer to the stock price, it increases faster. Not linearly but exponentially.