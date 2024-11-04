import pygame
from random import randint
import time
from Classes.Stock import Stock,POINTSPERGRAPH
from Defs import *
from pygame import gfxdraw
import numpy as np
from datetime import datetime, timedelta
from Classes.AssetTypes.LoanAsset import LoanAsset
# from Classes.AssetTypes.
# from Classes.imports.Messages import OptionMessage

class Player(Stock):
    

    def __init__(self,stocknames,color,transact,gametime) -> None:
        """Player class is a child of the Stock class price is the networth of the player"""
        name = 'Net Worth'
        super().__init__(name,color,gametime,0)
        
        self.name = name
        
        self.cash = 25000
        # if self.graphs[MINRANGE].size == 1:
        if  not all([len(graph) == POINTSPERGRAPH for graph in self.graphs.values()]):
            # print('cash is',self.cash)
            for key in self.graphs.keys():
                self.graphs[key] = np.array([],dtype=object)
                for _ in range(POINTSPERGRAPH):
                    self.graphs[key] = np.append(self.graphs[key],self.cash)

            # self.graphs = {key:np.array([],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
            
           
        # for (key,graph) in self.graphs.items():
        #     if graph.size == 1:
        #         self.graphs[key] = np.array([self.cash],dtype=object)
        self.stocks = []# list of lists containing the stockAsset objects
        self.options = []#list of option objects
        self.indexFunds = []#list of index fund objects
        self.lastLoanPayment = None#gets set right away in defs
        self.stockvalues = []
        self.loans = []
        self.messagedict = {}
        self.taxrate = 0.15
        self.transact = transact
        self.lifeTimeVolume,self.realizedGains,self.assetsTraded,self.taxesPaid,self.underTakenDebt,self.interestPaid = 0,0,0,0,0,0# Just some extra stats displayed in transaction menu
        self.assetText = {
            StockAsset:'Share',
            OptionAsset:'Option',
            IndexFundAsset:'Share'
        }
        self.gametime = gametime
        self.dividendYield = None
        self.updateOptions = 0# used to update the options every 120 frames

        # self.recent_movementvar = (None,None,(180,180,180)
    def getOptions(self):
        return self.options
    def getStocks(self):
        return self.stocks
    def getIndexFunds(self):
        return self.indexFunds
    def extraSavingData(self):
        data = []
        data.append(self.lastLoanPayment.strftime("%m/%d/%Y %I:%M:%S %p"))
        for i in [self.lifeTimeVolume,self.realizedGains,self.assetsTraded,self.underTakenDebt,self.taxesPaid,self.interestPaid]:
            data.append(i)
        return data
    def getExtraData(self,data,gametime):
        if data != None:
            self.lastLoanPayment = datetime.strptime(data[0],"%m/%d/%Y %I:%M:%S %p")
            self.lifeTimeVolume,self.realizedGains,self.assetsTraded,self.underTakenDebt,self.taxesPaid,self.interestPaid = data[1:]
        else:
            self.lastLoanPayment = gametime.time

    def newDay(self,gametime,stocklist:list):
        """Called at the start of a new day"""
        self.updateOptions = 0
        for option in self.options:
            option.getValue(bypass=True)
        for i in range(len(self.options)-1,-1,-1):
            print("Option has expired")
            if not self.options[i].optionLive():
                print("Option has expired for the player")
        for stock in stocklist:
            stock.updateDividendYield(gametime)
                # if not bigMessageList:
                    # bigMessageList.append(OptionMessage(self.options[i]))
            # self.options.pop(i)
            # print(self.options[i].name,self.options[i].daysToExpiration(gametime.time))
            # if self.options[i].daysToExpiration() <= 0:
            #     self.options[i].option.t = 0
            #     self.cash += self.options[i].option.getPrice(method="BSM",iteration=1)*self.options[i].quantity
            #     self.options.pop(i)
        # print('new day')
        
    def payDividend(self,stockObj=None,indexFundObj=None):
        """Pays the dividend to the player, called by the stock/index object when it reaches a new quarter/Month
        the stockObj one is called from the stockpriceEffects class in the update() method
        the indexFundObj is called here in the gameTick() method"""
        if stockObj == None and indexFundObj == None:
            return
        if stockObj != None and (stocksToPay:=[stock for stock in self.stocks if stock.stockObj == stockObj]):# if at least 1 of the stock is in the player's portfolio
            for stock in stocksToPay:
                amt = stock.giveDividend()

                for attr in ['cash', 'realizedGains', 'lifeTimeVolume']:
                    setattr(self, attr, getattr(self, attr) + amt)
                text = [
                    f"{self.gametime.getDate()}",
                    f"Received Dividend from {stockObj.name}",
                    f"+${limit_digits(amt,12)}",
                    f"{round(stockObj.dividendYield/4,2)}%",
                    f"${limit_digits(self.cash,12)}"
                ]
                self.transact.addTransaction(*text)

        elif indexFundObj != None and (indexfundsToPay:=[indexfund for indexfund in self.indexFunds if indexfund.stockObj == indexFundObj]):# if at least 1 of the index fund is in the player's portfolio
            for indexfund in indexfundsToPay:
                amt = indexfund.giveDividend()
                indexfund.dividends += amt
                for attr in ['cash', 'realizedGains', 'lifeTimeVolume']:#
                    setattr(self, attr, getattr(self, attr) + amt)
                
                text = [
                    f"{self.gametime.getDate()}",
                    f"Received Dividend from {indexFundObj.name}",
                    f"+${limit_digits(amt,12)}",
                    f"{round(indexfund.getDividendYield()/12,2)}%",
                    f"${limit_digits(self.cash,12)}"
                ]
                self.transact.addTransaction(*text)


    def gameTick(self,gamespeed:int,gametime):
        """Used to update the options every 120 frames"""
        self.updateOptions += gamespeed
        if self.updateOptions >= 512:
            self.updateOptions = 0
            for option in self.options:
                option.getValue(bypass=True)

        self.update_price(gamespeed,Player)
        if (gametime.time-self.lastLoanPayment) > timedelta(days=30):
            self.lastLoanPayment = gametime.time
            for loan in self.loans:
                self.addMonthlyLoanPayment(loan) 
            for indexfund in self.indexFunds:
                # indexfund.giveDividend()
                self.payDividend(indexFundObj=indexfund.stockObj)

    def buyAsset(self,newasset,customValue=None):
        """Custom Value will override the current value (Per Share Not Fullvalue)"""
        value = newasset.getValue(bypass=True,fullvalue=False) if customValue == None else customValue
        if newasset.quantity <= 0:
            return
        if isinstance(newasset,StockAsset):
            assetlist = self.stocks 
        elif isinstance(newasset,OptionAsset):
            assetlist = self.options
        elif isinstance(newasset,IndexFundAsset):
            assetlist = self.indexFunds

        if self.cash >= value*newasset.getQuantity():# if the player has enough money to buy the asset
            # ["Sold 39 Shares of","KSTON for $5,056.93","Balance $26,103.18"]
            text = [
                f"{self.gametime.getDate()}",
                f"Added {limit_digits(newasset.quantity,15,True)} {newasset.getStockObj().name} {newasset.getType() if type(newasset) == OptionAsset else ''} {self.assetText[type(newasset)]+('s' if newasset.quantity > 1 else '')}",
                f"-${limit_digits(newasset.getValue(bypass=True),12)}",
                f"${limit_digits(value,12)}",
                f"${limit_digits(self.cash-newasset.getValue(bypass=True),12)}"
            ]
            self.transact.addTransaction(*text)
            soundEffects['buy'].play()
            animationList.append(BuyAnimation(pygame.mouse.get_pos(),100,animationList))
            self.cash -= value*newasset.getQuantity()# fullvalue is True by default
            self.assetsTraded += newasset.getQuantity()
            self.lifeTimeVolume += value*newasset.getQuantity()
            for a in assetlist:# if the asset is already in the list, add the new asset to the old one
                if newasset == a:# use the __eq__ method to compare the assets
                    a += newasset# use the __iadd__ method to add the assets together
                    return# return if the asset is already in the list``
            
            assetlist.append(newasset.copy())# if the asset is not in the list, add it to the list
            
            print('cash is',self.cash)

    def sellAsset(self,asset,quantity,feePercent=1):
        """sells the quantity number of the asset object given
        won't sell more than the quantity of the asset"""
        quantity = int(quantity)
        if isinstance(asset,StockAsset):
            assetlist = self.stocks 
        elif isinstance(asset,OptionAsset):
            assetlist = self.options
        elif isinstance(asset,IndexFundAsset):
            assetlist = self.indexFunds

        if quantity > (quant:=assetlist[assetlist.index(asset)].quantity):# if the quantity is greater than the quantity of the asset
            quantity = quant
        # text = [
        #     f"Sold {quantity} {self.assetText[type(asset)]+('s' if quantity > 1 else '')} of",
        #     f"{asset.getStockObj().name} for ${limit_digits(asset.getValue(bypass=True,fullvalue=False),12)}",
        #     f"Balance ${limit_digits(self.cash+asset.getValue(bypass=True,fullvalue=False),12)}"
        # ]
        self.lifeTimeVolume += asset.getValue(bypass=True,fullvalue=False)*quantity
        loss_gain = asset.getValue(bypass=True,fullvalue=False)*quantity-asset.getOgVal()*quantity
        taxes = loss_gain*self.taxrate if loss_gain > 0 else 0
        self.taxesPaid += taxes
        loss_gain = loss_gain if loss_gain <= 0 else loss_gain*(1-self.taxrate)
        self.realizedGains += loss_gain if loss_gain > 0 else 0
        value = (asset.getValue(bypass=True,fullvalue=False)*quantity)-taxes
        text = [
            f"{self.gametime.getDate()}",
            f"Sold {limit_digits(quantity,15,True)} {asset.name} {self.assetText[type(asset)]+('s' if quantity > 1 else '')}",
             f"+${limit_digits(value,12)}",
            f"{'-' if loss_gain < 0 else '+'} ${limit_digits(abs(loss_gain),12) if loss_gain != 0 else '0'}",
            f"${limit_digits(self.cash+value,12)}"
        ]
        self.transact.addTransaction(*text)
        
        self.cash += asset.getValue(bypass=True,fullvalue=False)*quantity*feePercent# add the value of the asset to the cash
        print('cash is',self.cash,asset.getValue(bypass=True,fullvalue=False)*quantity)
        assetlist[assetlist.index(asset)].quantity -= quantity# subtract the quantity from the asset
        self.assetsTraded += quantity
        if assetlist[assetlist.index(asset)].quantity <= 0:# if the quantity of the asset is 0 or less, remove the asset from the list
            assetlist.remove(asset)
        
    # def exerciseOption(self,optionasset:OptionAsset):
    #     """Exercises the option"""
    #     print(f"Exercising Option {optionasset.name} for {optionasset.option.k} at {optionasset.option.s0}, value of ${optionasset.option.getPrice(method='BSM',iteration=1)}")
    #     self.cash += optionasset.option.getPrice(method="BSM",iteration=1)*optionasset.quantity
    #     self.options.remove(optionasset)

        

    
    def getNetworth(self):
        """returns the networth of the player"""
        allassets = self.stocks + self.options + self.indexFunds
        networth = self.cash + sum([asset.getValue() for asset in allassets])-sum([loan.principalLeft for loan in self.loans])
        if networth < 0.01:
            errors.addMessage('Bankrupt',txtSize=100,coords=[960,540])
            print(Exception('Bankrupt'))
            return networth
        else:
            return networth
        # return self.cash + sum([stock[0].cash*stock[2] for stock in self.stocks]) + sum([option.get_value() for option in self.options])
    def getAssets(self,amount:int=0):
        """returns the assets of the player, returns all of them if amount is 0 else returns the top [amount] assets"""
        if amount == 0:
            return self.stocks + self.options + self.indexFunds

        allassets = self.stocks + self.options + self.indexFunds
        allassets.sort(key=lambda x:x.getValue(),reverse=True)
    
        return allassets[:amount]
    
    def addLoan(self,loanObj):
        """adds a loan to the player"""
        self.loans.append(loanObj)
        self.underTakenDebt += loanObj.principal
        text = [
            f"{self.gametime.getDate()}",
            f"Added a Loan ",
             f"+${limit_digits(loanObj.principal,20,loanObj.principal>1000)}",
            f"N/A",
            f"${limit_digits(self.cash+loanObj.principal,20)}"
        ]
        self.transact.addTransaction(*text)
        soundEffects['buy'].play()
        animationList.append(BuyAnimation(pygame.mouse.get_pos(),100,animationList))
        self.cash += loanObj.principal

    def getMaxLoan(self):
        """returns the maximum amount of money the player can borrow"""
        est = self.getNetworth()*0.2
        return est if est > 5000 else 5000 # 20% of the networth of the player or 5000 whichever is greater
    def getCurrentDebt(self):
        """returns the total amount of money owed by the player"""
        return sum([loan.principalLeft for loan in self.loans])
    def getCurrentMaxLoan(self):
        """returns the maximum amount of money the player can borrow minus the total amount of money owed"""
        est = self.getMaxLoan()-sum([loan.principalLeft for loan in self.loans])
        est = max(est,0)
        return est
    def getMonthlyPayment(self):
        """returns the total monthly payment of all the loans"""
        return sum([loan.getLoanCalc() for loan in self.loans])
    def getDebtUtilization(self):
        """returns the debt utilization of the player"""
        return (self.getCurrentDebt()/self.getMaxLoan())*100
    def getAvgInterest(self):
        """returns the weighted average interest rate of all the loans"""
        total_principal = sum(loan.principal for loan in self.loans)
        weighted_sum = sum(loan.rate * loan.principal for loan in self.loans)
        return (weighted_sum / total_principal)*100 if total_principal != 0 else 0
    def getCurrentInterestRate(self):
        """returns the interest rate of the most recent loan"""
        return 4.5# ACTUALLY NEED TO CODE THIS SOME OTHER TIME IN THE FUTURE THANKS
    def removeLoan(self,loanObj:LoanAsset):
        """removes the loan from the player"""
        
        text = [
            f"{self.gametime.getDate()}",
            f"Paid off ${limit_digits(loanObj.principal,20,loanObj.principal>1000)} Loan",
            f"$0",
            f"-${limit_digits(loanObj.interestPaid,20)}",
            f"${limit_digits(self.cash,20)}"
        ]
        self.loans.remove(loanObj)
        self.transact.addTransaction(*text)

    def addMonthlyLoanPayment(self,loanObj):
        """adds a monthly payment to the loan
        should be called by the gameTick method
        This method is purely so that it can minus cash and add the transaction"""

        amount,interest = loanObj.addMonthlyPayment(self)
        self.cash -= amount
        self.interestPaid += interest
        text = [
            f"{self.gametime.getDate()}",
            f"Paid ${limit_digits(amount,20,amount>1000)} on Loan",
            f"-${limit_digits(amount,20,amount>1000)}",
            f"-${limit_digits(interest,20,interest>1000)}",
            f"${limit_digits(self.cash,20)}"
        ]
        self.transact.addTransaction(*text)
    def addLoanPayment(self,loanObj,amount):
        """adds a payment to the loan, NOT A MONTHLY PAYMENT - straight to the principal"""
        self.cash -= loanObj.addPayment(amount,self)
        text = [
            f"{self.gametime.getDate()}",
            f"Paid ${limit_digits(amount,20,amount>1000)} on Loan",
            f"-${limit_digits(amount,20,amount>1000)}",
            f"0",
            f"${limit_digits(self.cash,20)}"
        ]
        self.transact.addTransaction(*text)

        