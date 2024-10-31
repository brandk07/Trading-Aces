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
        pass
    def savingInputs(self):
        return (self.rate,self.term,self.principal)
    def copy(self):
        return LoanAsset(self.rate,self.term,self.principal)
    def getLoanCalc(self):
        # Calculate the monthly payment
        return npf.pmt(self.rate / 12, self.termLeft, -self.principalLeft)
    def getOGVals(self) -> tuple:
        """Returns the values when the loan was created -> (monthly payment, total payment, total interest)"""
        payment = self.getLoanCalc()
        totalPayment = payment * self.term
        totalInterest = totalPayment - self.principal
        return (payment,totalPayment,totalInterest)

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
        if self.principalLeft <= 0:
            player.removeLoan(self)
        return payment

    def addPayment(self,amount,player) -> float:
        """Add One time payment to the loan - SHOULD BE CALLED BY THE PLAYER SO THAT THE MONEY COMES THROUGHT THE PLAYER CLASS"""
        if amount > self.principalLeft:
            player.removeLoan(self)
        self.principalLeft -= amount
        return amount