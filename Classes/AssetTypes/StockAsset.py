from Classes.AssetTypes.Asset import Asset
from datetime import datetime as d

class StockAsset(Asset):
    def __init__(self,stockobj,creationdate,ogvalue,quantity) -> None:
        """Stock Asset is a child of the Asset class"""
        super().__init__(stockobj,creationdate,'',ogvalue,quantity,stockobj.color)

    def __eq__(self,other):
        if not isinstance(other,StockAsset):
            return False
        return [self.stockobj,self.ogvalue,self.date] == [other.stockobj,self.ogvalue,other.date]
    
    def getInputs(self):
        return (self.stockobj,self.date.getTime(),self.name,self.ogvalue,self.color,self.quantity)
    def savingInputs(self):
        return (self.stockobj.name,self.date,int(self.ogvalue),self.quantity)
    def getValue(self,bypass=False,fullvalue=True):
        """returns the value of the stock"""
        # print(self.stockobj.price)
        return int((self.stockobj.price) * self.quantity) if fullvalue else self.stockobj.price
    