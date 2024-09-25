from Classes.AssetTypes.Asset import Asset
from datetime import datetime as d
import numpy_financial as npf


import numpy_financial as npf

class LoanAsset:
    def __init__(self, rate, term, principal, paymentsMade=0,loanType="Fixed"):
        self.rate : float = rate# annual interest rate - ex. 5% = 0.05
        self.term : int = term# in months
        self.principal : float = principal
        self.paymentsMade : int = paymentsMade
        self.loanType : str = loanType# fixed
    def setValues(self,rate,term,principal,paymentsMade=0,loanType="Fixed"):
        self.rate = rate
        self.term = term
        self.principal = principal
        self.paymentsMade = paymentsMade
        self.loanType = loanType
    def __eq__(self,other):
        return self.rate == other.rate and self.term == other.term and self.principal == other.principal and self.paymentsMade == other.paymentsMade and self.loanType == other.loanType
    def savingInputs(self):
        return (self.rate,self.term,self.principal,self.paymentsMade,self.loanType)
    def copy(self):
        return LoanAsset(self.rate,self.term,self.principal,self.paymentsMade,self.loanType)
    def getLoanCalc(self):
        # Calculate the monthly payment
        return npf.pmt(self.rate / 12, self.term, -self.principal)
    def getOGVals(self) -> tuple:
        """Returns the values when the loan was created -> (monthly payment, total payment, total interest)"""
        payment = self.getLoanCalc()
        totalPayment = payment * self.term
        totalInterest = totalPayment - self.principal
        return (payment,totalPayment,totalInterest)
    
    def getInterestPaid(self):
        """Calculate the total interest paid up to a certain period"""
        total_interest_paid = 0
        for p in range(1, self.paymentsMade + 1):
            interest_payment = npf.ipmt(self.rate / 12, p, self.term, -self.principal)
            total_interest_paid += interest_payment
        return total_interest_paid

    def getPrincipalPaid(self):
        """Calculate the total principal paid up to a certain period"""
        interest = self.getInterestPaid()
        return self.getLoanCalc() * self.paymentsMade - interest

    def getTotalLeftInterest(self):
        """Calculate how much will be paid at current rate with interest"""
        return self.getLoanCalc() * (self.term - self.paymentsMade)
    def getPrincipalLeft(self):
        """Calculate how much principal is left"""
        return self.principal - self.getPrincipalPaid()
    