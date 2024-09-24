from Classes.AssetTypes.Asset import Asset
from datetime import datetime as d
import numpy_financial as npf

class LoanAsset():
    def __init__(self,player,creationDate,principal,loanterm,interestRate,interestPaid=0,principalLeft=None,loanType="Fixed") -> None:
        """Stock Asset is a child of the Asset class"""
        if principalLeft == None: principalLeft = principal# if principalLeft is not given then it is the same as the principal
        self.dividends = 0
        self.creationDate = creationDate
        self.principal : int|float = principal
        self.interestRate : float = interestRate# annual interest rate - ex. 5% = 0.05
        self.interestPaid : int|float = interestPaid
        self.principalLeft : int|float = principalLeft
        self.loanterm : float = loanterm# in years
        self.loanType : str = loanType# fixed
        self.playerObj = player

        
    
    def getLoanCalc(self):
        total_payments = self.loanterm * 12
        payment = npf.pmt(self.interestRate,total_payments,self.principalLeft)# payment per period
        return payment

    def getInterestPaid(self):
        total_payments = self.loanterm * 12
        payment = self.getLoanCalc()
        return total_payments*payment - self.principalLeft
    

    def savingInputs(self):
        return (str(self.creationDate),self.principal,self.loanterm,self.interestRate,self.interestPaid,self.principalLeft,self.loanType)
    
    def copy(self):
        return LoanAsset(self.playerObj,str(self.creationDate),self.principal,self.loanterm,self.interestRate,self.interestPaid,self.principalLeft,self.loanType)
    
    