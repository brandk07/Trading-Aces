from Classes.imports.optionVal import OptionVal as Op
from Classes.AssetTypes.Asset import Asset
from Classes.AssetTypes.StockAsset import StockAsset
import numpy as np
from collections import deque
from random import randint,random
from datetime import timedelta,datetime
from functools import lru_cache 
# from Classes.imports.BigMessage import OptionMessage
from Defs import *
# ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO']
DFORMAT = "%m/%d/%Y"

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
HOLIDAYS = [(1,1),(1,15),(2,19),(3,29),(5,27),(6,19),(7,4),(9,2),(11,28),(12,25)]

def isOpen(time:datetime):
    """Checks if the market is open or not
    returns a tuple of (bool,reason)"""
    assert isinstance(time,datetime), "time must be a datetime object"

    if (time.month,time.day) in HOLIDAYS:
        return False
    if WEEKDAYS[time.weekday()] in ['Saturday','Sunday']:
        return False
    if not(((time.hour == 9 and time.minute >= 30) or time.hour > 9) and time.hour < 16):
        return False
    return True




def getCloseOpenDate(time : datetime) -> datetime:
    if isOpen(time): return time

    extime = time
    extime = extime.replace(hour=9,minute=31,second=0)
    while isOpen(extime) == False:#  Makes sure the expiration date is a trading day
        extime = extime+timedelta(days=1)
        # print(f"extime at {extime}, for time, {time}, {isOpen(extime)}")
    # print(f"closest is {extime}, for time, {time}")
    return extime

# @lru_cache(maxsize=128)
#         def getDays(year,month,day,hour):
#             print(f"getting days for {year,month,day,hour}")
#             print()
#             currentTime = datetime(year,month,day,9,30)
#             d = currentTime
#             daysPast = 0
#             while d < self.expirationDate:
#                 d += timedelta(days=1)
#                 if isOpen(d):
#                     daysPast += 1
#             hours = 0
#             if isOpen(self.gametime.time):
#                 minutes = self.gametime.time.minute/60
#                 hours = max(1-((hour + minutes - 9)/6.5),.1)
#             return round(daysPast + hours,1)
class TimeGetter:
    def __init__(self,optionAsset,gametime) -> None:
        self.lastinputs = []
        self.gametime = gametime
        self.lastvalue = None
        self.optionAsset : OptionAsset = optionAsset

    def __call__(self,year,month,day,hour):
        if self.lastinputs == (year,month,day,hour):
            # print("done this", self.lastvalue)
            return self.lastvalue
        currentTime = datetime(year,month,day,9,30)
        d = currentTime
        daysPast = 0
        while d < self.optionAsset.expirationDate:
            d += timedelta(days=1)
            if isOpen(d):
                daysPast += 1
        # hours = 1
        hours = 1
        
        if isOpen(self.gametime.time):
            # print("open")
            minutes = self.gametime.time.minute/60
            hours = 1-((hour + minutes - 9)/6.5)
        # print(f"is Open current {currentTime}, {isOpen(currentTime)} hour {hour}")
        if isOpen(currentTime) and hour >= 16:
            
            daysPast -= 1
        if not isOpen(currentTime):
            daysPast -= 1

        # print(f"hour {hour}, {isOpen(self.gametime.time)}, {self.gametime.time} hours -> {hours}, {daysPast}")
            
            
        self.lastinputs = (year,month,day,hour)
        self.lastvalue = round(daysPast + hours - 1,1)
        # print("did it ", self.lastvalue)
        return self.lastvalue


class OptionAsset(Asset):
    def __init__(self,player,stockObj,strikePrice:int,expirationDate:datetime,optionType:str,creationDate:str,quantity:int,porfolioPercent=None,ogValue=None,color=None) -> None:
        super().__init__(player,stockObj, creationDate, " "+optionType, ogValue, quantity, porfolioPercent, color=color)
        
        self.gametime : datetime = player.gametime
        self.timeGetter = TimeGetter(self,self.gametime)
        self.strikePrice = strikePrice
        self.expirationDate = datetime.strptime(expirationDate, "%Y-%m-%d %H:%M:%S") if isinstance(expirationDate,str) else expirationDate
        self.expirationDate = getCloseOpenDate(self.expirationDate)# Makes sure the expiration date is a trading day
        self.optionType = optionType
    
        self.option = Op(european=True,kind=self.optionType,s0=float(self.stockObj.price)*100,k=self.strikePrice*100,t=self.daysToExpiration(),sigma=self.getVolatility(),r=0.05)
        self.ogValue = self.ogValue if self.ogValue != None else self.getValue(bypass=True,fullvalue=False)# ogValue is the value the asset orginally had, just for 1 asset
        
        # print(f"{self.name}, {porfolioPercent} {self.portfolioPercent}")
        if porfolioPercent == None:
            
            self.portfolioPercent = self.getValue(bypass=True,fullvalue=True)/(player.getNetworth())# have to set this after the object is created
            # print(f"dont, {self.portfolioPercent}, {ogValue} {networth}") 
            
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
    def copy(self):
        return OptionAsset(self.playerObj,self.stockObj,self.strikePrice,str(self.expirationDate),self.optionType,str(self.date),self.quantity,self.portfolioPercent,ogValue=self.getValue(bypass=True,fullvalue=False),color=self.color)
    def getStrike(self): return self.strikePrice
    def getType(self): return self.optionType
    def setValues(self,strikePrice=None,expDate=None,optionType=None,quantity=None,creationDate=None):
        if strikePrice: self.strikePrice = strikePrice
        if expDate: self.expirationDate = expDate
        if optionType: self.optionType = optionType
        if quantity: self.quantity = quantity
        if creationDate: 
            self.date = creationDate if isinstance(creationDate,str) else creationDate.strftime("%m/%d/%Y %I:%M:%S %p")
        self.expirationDate = getCloseOpenDate(self.expirationDate)# Makes sure the expiration date is a trading day
        self.option.setValues(strike=self.strikePrice*100,days=self.daysToExpiration(),optionType=self.optionType)
        self.ogValue = self.getValue(bypass=True,fullvalue=False); self.portfolioPercent = self.getValue(bypass=True,fullvalue=True)/(self.playerObj.getNetworth())
    def savingInputs(self):
        return (self.stockObj.name,self.strikePrice,str(self.expirationDate),self.optionType,self.date,self.quantity,self.portfolioPercent,self.ogValue,self.color)
    def getExpDate(self):
        return self.expirationDate.strftime(DFORMAT)
    def getExerciseStock(self):
        return StockAsset(self.playerObj,self.stockObj,self.gametime.time,self.strikePrice,self.quantity*100)
    def daysToExpiration(self):
        # assert isinstance(gametimeTime,datetime), "gametimeTime must be a datetime object Use .time"
        
        # if self in self.playerObj.options:
        # daysPast = self.getDaysSelf(self.gametime.time.year,self.gametime.time.month,self.gametime.time.day,self.gametime.time.hour)
        daysPast = self.timeGetter(self.gametime.time.year,self.gametime.time.month,self.gametime.time.day,self.gametime.time.hour)
        return daysPast
    def optionLive(self):
        return self.daysToExpiration() > 0
    def getValue(self,bypass=False,fullvalue=True):
        """""Bypass is used to force a recalculation of the option value
        Full value is value*quantity otherwise it is just the value of the option"""
        
        # if self.daysToExpiration() < 0:
            # self.option.setValues(days=0)
            # if self in self.playerObj.options:
                
            # if self in self.playerObj.options:
            #     self.playerObj.sellAsset(self,self.quantity)
            # return self.lastvalue * self.quantity
        if bypass or self.updateCount > 60:
            self.option.setValues(underPrice=float(self.stockObj.price)*100,volatility=self.getVolatility(),days=self.daysToExpiration()/365)
  
            self.option.t = self.option.t if self.option.t > 0 else 0

            self.updateCount = 0

            self.lastvalue = self.option.getPrice(method="BSM",iteration=1)
            return (self.lastvalue * self.quantity) if fullvalue else self.lastvalue

        self.updateCount += 1
        return (self.lastvalue * self.quantity) if fullvalue else self.lastvalue

# Option prices are impacted by 4 major elements i.e. delta, gamma, theta, vega.

# Theta is time decay works in reducing the premium as per the time to expiry.

# Vega is volatility, very difficult to explain, let’s just say option prices increase with the increase in volatility.

# Delta is the ratio of option price change as a percentage of underlying change.
    
# Gamma is the rate of change of delta with respect to the change in the underlying price.
# The massive price change is due to something called Gamma acceleration. Let’s just say that as the option moves nearer to the stock price, it increases faster. Not linearly but exponentially.