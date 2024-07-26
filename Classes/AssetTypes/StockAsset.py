from Classes.AssetTypes.Asset import Asset
from datetime import datetime as d

class StockAsset(Asset):
    def __init__(self,player,stockObj,creationDate,ogValue,quantity,dividends=0,portfolioPercent=None) -> None:
        """Stock Asset is a child of the Asset class"""
        super().__init__(player,stockObj,creationDate,'',ogValue,quantity,portfolioPercent,stockObj.color)
        self.dividends = 0
        
        if portfolioPercent == None:
            self.portfolioPercent = self.getValue(bypass=True)/(player.getNetworth())

    def __eq__(self,other):
        if not isinstance(other,StockAsset):
            return False
        return [self.stockObj,self.ogValue,self.date] == [other.stockObj,self.ogValue,other.date]
    
    # def getInputs(self):
    #     return (self.stockObj,self.date.getTime(),self.name,self.ogValue,self.color,self.quantity)
    def savingInputs(self):
        return (self.stockObj.name,self.date,float(self.ogValue),self.quantity,self.dividends,self.portfolioPercent)
    def getValue(self,bypass=False,fullvalue=True):
        """returns the value of the stock, bypass is used to force a recalculation of the stock value, fullvalue is value*quantity otherwise it is just the value of the stock"""
        # print(self.stockObj.price)
        return ((self.stockObj.price) * self.quantity) if fullvalue else self.stockObj.price

    def giveDividend(self,transact):
        """gives the stock asset a dividend"""
        amount = (self.stockObj.dividend*self.getValue())/4# quarterly dividends
        self.dividends += amount
        transact.addTransaction(f"Received ${amount} in dividends from",f"{self.stockObj.name}",f"Total Dividends ${self.dividends}")
    