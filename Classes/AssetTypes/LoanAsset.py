from Classes.AssetTypes.Asset import Asset
from datetime import datetime as d
import numpy_financial as npf


import numpy_financial as npf

class LoanAsset:
    def __init__(self, rate, term, principal, principalLeft=None,interestPaid=None,termLeft=None) -> None:
        self.rate : float = rate# annual interest rate - ex. 5% = 0.05
        self.term : int = term# in months
        self.termLeft : int = termLeft if termLeft != None else term
        self.principal : float = principal# original loan amount
        self.principalLeft : float = principalLeft if principalLeft != None else principal
        self.interestPaid : float = interestPaid if interestPaid != None else 0

    def setValues(self,rate,term,principal):
        self.rate = rate
        self.term = term
        self.principal = principal


    def __eq__(self,other):
        if not isinstance(other,LoanAsset):
            return False
        return [self.rate,self.term,self.principal,self.principalLeft,self.interestPaid,self.termLeft] == [other.rate,other.term,other.principal,other.principalLeft,other.interestPaid,other.termLeft]
    def savingInputs(self):
        return (self.rate,self.term,self.principal,self.principalLeft,self.interestPaid,self.termLeft)
    def copy(self):
        return LoanAsset(self.rate,self.term,self.principal,self.principalLeft,self.interestPaid,self.termLeft)
    def getLoanCalc(self,rate=None,term=None,principal=None) -> float:
        # Calculate the monthly payment
        rate = self.rate if rate == None else rate
        term = self.termLeft if term == None else term
        principal = self.principalLeft if principal == None else principal
        return npf.pmt(rate / 12, term, -principal)
    def getOGVals(self) -> tuple:
        """Returns the values when the loan was created -> (monthly payment, total payment, total interest)"""
        payment = self.getLoanCalc()
        totalPayment = payment * self.term
        totalInterest = totalPayment - self.principal
        return (payment,totalPayment,totalInterest)

    def getMonthlyPayment(self):
        """Calculate the monthly payment"""
        return self.getLoanCalc()

    def getPrincipalPaid(self):
        """Calculate the total principal paid up to a certain period"""
        return self.principal - self.principalLeft

    def getTotalLeftInterest(self):
        """Calculate how much will be paid at current rate with interest"""
        # return self.getLoanCalc() * (self.term - self.paymentsMade)
        return self.getLoanCalc() * self.termLeft+self.interestPaid
    
    def addMonthlyPayment(self,player) -> float:
        """Add monthly payment to the loan - SHOULD BE CALLED BY THE PLAYER SO THAT THE MONEY COMES THROUGHT THE PLAYER CLASS"""
        payment = self.getLoanCalc()
        interest = self.principalLeft * self.rate / 12
        self.interestPaid += interest
        self.principalLeft -= payment - interest
        self.termLeft -= 1
        if self.principalLeft < .01:
            player.removeLoan(self)
        return payment

    def addPayment(self,amount,player) -> float:
        """Add One time payment to the loan - SHOULD BE CALLED BY THE PLAYER SO THAT THE MONEY COMES THROUGHT THE PLAYER CLASS"""

        self.principalLeft -= amount
        if self.principalLeft < .01:
            player.removeLoan(self)
        return amount