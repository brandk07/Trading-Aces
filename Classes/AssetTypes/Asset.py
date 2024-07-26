from optionprice import Option as Op
import numpy as np
from collections import deque    
from random import randint
import datetime

class Asset:
    def __init__(self,player:object,stockObj:object,creationDate:str,nameText:str,ogValue:float,quantity:int,portfolioPercent:float,color=None) -> None:
        """Parent class for all assets"""
        self.stockObj = stockObj
        self.playerObj = player
        self.date = creationDate
        self.portfolioPercent = portfolioPercent
        self.ogValue = ogValue# ogValue is the value the asset orginally had, just for 1 asset
        self.color = (randint(50,255),randint(50,255),randint(50,255)) if color == None else color
        self.name = f'{self.stockObj.name}{nameText}'# nameText for options is the option type
        self.quantity = quantity
        self.dateobj = datetime.datetime.strptime(creationDate, "%m/%d/%Y %I:%M:%S %p")
        

    def __str__(self) -> str:
        return f'{self.name}'
    
    def __eq__(self,other):
        raise NotImplementedError('This method must be implemented in the child class')
    
    def __iadd__(self,other):
        if self == other:
            extraValue = (other.getValue(bypass=True)+self.getValue(bypass=True))
            self.portfolioPercent = extraValue/(self.playerObj.getNetworth()+other.getValue(bypass=True))
            self.quantity += other.quantity
            return self
        raise ValueError(f'{type(self).__name__} objects must be the same to add them together')
    def getStockObj(self): return self.stockObj
    def getOgVal(self): return self.ogValue

    def getPercent(self):
        """returns the percent change of the option"""
        return ((self.getValue(fullvalue=False) - (self.ogValue)) / (self.ogValue)) * 100
    
    def getVolatility(self):
        """returns the volatility of the asset's stock"""
        return self.stockObj.getVolatility()
    
    def savingInputs(self):
        """returns the all the inputs needed to construct a new object"""
        raise NotImplementedError('This method must be implemented in the child class')

    def copy(self):    
       """Method returns an exact copy of the object"""    
       raise NotImplementedError('This method must be implemented in the child class')

    def sell(self,player,quantity):
        """sells the Asset"""
        player.sellAsset(self,quantity)

    def getValue(self,bypass=False,fullvalue=True):
        """""Bypass is used to force a recalculation of the asset value (used for options since it is compute intensive)
        Full value is value*quantity otherwise it is just the value of the asset"""
        raise NotImplementedError('This method must be implemented in the child class')
    