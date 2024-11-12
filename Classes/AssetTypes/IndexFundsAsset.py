from Classes.AssetTypes.Asset import Asset
from datetime import datetime as d

class IndexFundAsset(Asset):
    def __init__(self,player,stockObj,creationDate,ogValue,quantity,dividends=0,portfolioPercent=None) -> None:
        """Index Fund Asset is a child of the Asset class (StockObj is really a IndexFundObj)"""
        super().__init__(player,stockObj,creationDate,'',ogValue,quantity,portfolioPercent,stockObj.color)
        self.dividends = dividends# the dividends that the stock has given
        
        if portfolioPercent == None:
            self.portfolioPercent = self.getValue(bypass=True)/(player.getNetworth())

    def __eq__(self,other):
        if not isinstance(other,IndexFundAsset):
            return False
        return [self.stockObj,self.ogValue,self.date] == [other.stockObj,self.ogValue,other.date]
    
    # def getInputs(self):
    #     return (self.stockObj,self.date.getTime(),self.name,self.ogValue,self.color,self.quantity)
    
    def savingInputs(self):
        return (self.stockObj.name,self.date,float(self.ogValue),self.quantity,self.dividends,self.portfolioPercent)
    def copy(self):
        return IndexFundAsset(self.playerObj,self.stockObj,self.date,self.ogValue,self.quantity,self.dividends,self.portfolioPercent)
    def getValue(self,bypass=False,fullvalue=True):
        """returns the value of the stock, bypass is used to force a recalculation of the stock value, fullvalue is value*quantity otherwise it is just the value of the stock"""
        # print(self.stockObj.price)
        return ((self.stockObj.price) * self.quantity) if fullvalue else self.stockObj.price

    def getDividendYield(self):
        """returns the dividend yield of the stock"""
        # return round(sum([s.dividendYield for s in self.stockObj.combinStocks])/len(self.stockObj.combinStocks),3)
        return self.stockObj.getDividendYield()
    
    def giveDividend(self):
        """gives the stock asset a dividend"""
        amount = ((self.getDividendYield()/100)*self.getValue())/12# Monthly dividends
        self.dividends += amount
        return amount