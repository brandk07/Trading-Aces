from Classes.AssetTypes.Asset import Asset
from datetime import datetime as d

class StockAsset(Asset):
    def __init__(self,stockobj,creationdate,ogvalue,quantity,networth,dividendTotal=0) -> None:
        """Stock Asset is a child of the Asset class"""
        super().__init__(stockobj,creationdate,'',ogvalue,quantity,0,stockobj.color)
        self.totalDividends = 0
        self.portfolioPercent = self.getValue(bypass=True)/(networth+self.getValue(bypass=True))

    def __eq__(self,other):
        if not isinstance(other,StockAsset):
            return False
        return [self.stockobj,self.ogvalue,self.date] == [other.stockobj,self.ogvalue,other.date]
    
    # def getInputs(self):
    #     return (self.stockobj,self.date.getTime(),self.name,self.ogvalue,self.color,self.quantity)
    def savingInputs(self):
        return (self.stockobj.name,self.date,float(self.ogvalue),self.quantity,self.portfolioPercent,self.totalDividends)
    def getValue(self,bypass=False,fullvalue=True):
        """returns the value of the stock, bypass is used to force a recalculation of the stock value, fullvalue is value*quantity otherwise it is just the value of the stock"""
        # print(self.stockobj.price)
        return ((self.stockobj.price) * self.quantity) if fullvalue else self.stockobj.price

    def giveDividend(self,transact):
        """gives the stock asset a dividend"""
        amount = (self.stockobj.dividend*self.getValue())/4# quarterly dividends
        self.totalDividends += amount
        transact.addTransaction(f"Received ${amount} in dividends from",f"{self.stockobj.name}",f"Total Dividends ${self.totalDividends}")
    