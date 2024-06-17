from optionprice import Option as Op
import numpy as np
from collections import deque    
from random import randint
import datetime

class Asset:
    def __init__(self,player:object,stockobj:object,creationdate:str,nametext:str,ogvalue:float,quantity:int,portfolioPercent:float,color=None) -> None:
        """Parent class for all assets"""
        self.stockobj = stockobj
        self.playerObj = player
        self.date = creationdate
        self.portfolioPercent = portfolioPercent
        self.ogvalue = ogvalue# ogvalue is the value the asset orginally had, just for 1 asset
        self.color = (randint(50,255),randint(50,255),randint(50,255)) if color == None else color
        self.name = f'{self.stockobj.name}{nametext}'# nametext for options is the option type
        self.quantity = quantity
        self.dateobj = datetime.datetime.strptime(creationdate, "%m/%d/%Y %I:%M:%S %p")
        

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
        
    def getPercent(self):
        """returns the percent change of the option"""
        return ((self.getValue(fullvalue=False) - (self.ogvalue)) / (self.ogvalue)) * 100
    
    def getVolatility(self):
        """returns the volatility of the asset's stock"""
        return self.stockobj.getVolatility()
    
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
    