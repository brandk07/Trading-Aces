from optionprice import Option as Op

class Option:
    def __init__(self,stockobj,strike_price,expiration_date,option_type) -> None:
        self.stockobj = stockobj
        self.strike_price = strike_price
        self.expiration_date = expiration_date
        self.option_type = option_type
        self.ogvalue = self.get_value()

    def __str__(self) -> str:
        return self.stockobj.name
    
    def get_value(self):
        obj = Op(european=True,
                    kind=self.option_type,
                    s0=self.stockobj.price,
                    k=self.strike_price,
                    t=self.expiration_date,
                    sigma=self.stockobj.volatility,
                    r=0.05)
        return obj.getPrice(method="BSM",iteration=50000)