import pygame
from random import randint
import time
from Classes.BigClasses.Stock import Stock,POINTSPERGRAPH
from Defs import *
from pygame import gfxdraw
import numpy as np
from datetime import datetime, timedelta
from Classes.AssetTypes.LoanAsset import LoanAsset
from Classes.BigClasses.RunTypes import CareerRun
# from Classes.AssetTypes.
# from Classes.imports.Messages import OptionMessage
class CashStock(Stock):
    def __init__(self, color, gametime, gameRun, player):
        """CashStock is a child of the Stock class, it is really just for the cash graph"""
        self.name = "Cash"
        self.player = player
        super().__init__(self.name, color, gametime, 0, gameRun, player)

        if not all([len(graph) == POINTSPERGRAPH for graph in self.graphs.values()]):
            for key in self.graphs.keys():
                self.graphs[key] = deque([self.player.cash],maxlen=POINTSPERGRAPH)
                for _ in range(POINTSPERGRAPH):
                    self.graphs[key].append(self.player.cash)
        
class Player(Stock):
    

    def __init__(self,stocknames,color,transact,gametime,gameRun) -> None:
        """Player class is a child of the Stock class price is the networth of the player"""
        name = 'Networth'
        super().__init__(name,color,gametime,0,gameRun,self)
        
        self.name = name
        
        self.cash = STARTCASH
        # if self.graphs[MINRANGE].size == 1:
        if not all([len(graph) == POINTSPERGRAPH for graph in self.graphs.values()]):
            # print('cash is',self.cash)
            for key in self.graphs.keys():
                # self.graphs[key] = np.array([],dtype=object)
                self.graphs[key] = deque([self.cash],maxlen=POINTSPERGRAPH)
                for _ in range(POINTSPERGRAPH):
                    # self.graphs[key] = np.append(self.graphs[key],self.cash)
                    self.graphs[key].append(self.cash)

            # self.graphs = {key:np.array([],dtype=object) for key in self.graphrangeoptions.keys()}#the lists for each graph range
            

        self.stocks = []# list of lists containing the stockAsset objects
        self.options = []#list of option objects
        self.indexFunds = []#list of index fund objects
        self.lastLoanPayment = None#gets set right away in defs
        self.cashStock = CashStock(color,gametime,gameRun,self)
        self.currentRun = gameRun
        self.stockvalues = []
        self.loans = []
        self.menuList = None
        self.screenManager = None
        self.messagedict = {}
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
    def save_data(self):
        self.cashStock.save_data()
        super().save_data()
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
            if not self.options[i].optionLive():
                self.screenManager.setScreen('Options')
                self.screenManager.screens['Options'].forceExerciseOption(self.options[i])
                

        for stock in stocklist:
            stock.updateDividendYield(gametime)

        
    def payDividend(self,stockObj=None,indexFundObj=None):
        """Pays the dividend to the player, called by the stock/index object when it reaches a new quarter/Month
        the stockObj one is called from the stockpriceEffects class in the update() method
        the indexFundObj is called here in the gameTick() method"""
        if self.runStateCheck(): return
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
                    f"+${limit_digits(amt,20)}",
                    f"{round(stockObj.dividendYield/4,2)}%",
                    f"${limit_digits(self.cash,20)}"
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
                    f"+${limit_digits(amt,20)}",
                    f"{round(indexfund.getDividendYield()/12,2)}%",
                    f"${limit_digits(self.cash,20)}"
                ]
                self.transact.addTransaction(*text)


    def gameTick(self,gamespeed:int,gametime,step):
        """Used to update the options every 120 frames, step is the rate at which the 1 price movement will go in as"""
        self.updateOptions += gamespeed
        if self.updateOptions >= 512:
            self.updateOptions = 0
            for option in self.options:
                option.getValue(bypass=True)

            # Only checked every 512 frames for performance reasons
            if (gametime.time-self.lastLoanPayment) > timedelta(days=30):
                self.lastLoanPayment = gametime.time
                for loan in self.loans:
                    self.addMonthlyLoanPayment(loan) 
                for indexfund in self.indexFunds:
                    # indexfund.giveDividend()
                    self.payDividend(indexFundObj=indexfund.stockObj)

        self.update_price(gamespeed,step)
        self.cashStock.update_price(gamespeed,step)
        

    def buyAsset(self,newasset,customValue=None):
        """Custom Value will override the current value (Per Share Not Fullvalue)"""
        if self.runStateCheck(): return
        value = newasset.getValue(bypass=True,fullvalue=False) if customValue == None else customValue
        if newasset.quantity <= 0:
            return
        if isinstance(newasset,StockAsset):
            assetlist = self.stocks 
        elif isinstance(newasset,OptionAsset):
            assetlist = self.options
        elif isinstance(newasset,IndexFundAsset):
            assetlist = self.indexFunds

        if len(self.getAssets()) >= self.currentRun.getCurrVal('Asset Storage'):
            if not [asset for asset in self.getAssets() if asset == newasset]:# if the asset is not already in the list - otherwise it will just add the quantity to the asset
                errors.addMessage('Insufficient Asset Storage',txtSize=100,coords=[960,540])# player has too many assets
                soundEffects['error'].play()
                return

        if self.cash >= value*newasset.getQuantity():# if the player has enough money to buy the asset
            # ["Sold 39 Shares of","KSTON for $5,056.93","Balance $26,103.18"]
            
            text = [
                f"{self.gametime.getDate()}",
                f"Added {limit_digits(newasset.quantity,20,True)} {newasset.getStockObj().name} {newasset.getType() if type(newasset) == OptionAsset else ''} {self.assetText[type(newasset)]+('s' if newasset.quantity > 1 else '')}",
                f"-${limit_digits(newasset.getValue(bypass=True),20)}",
                f"${limit_digits(value,20)}",
                f"${limit_digits(self.cash-newasset.getValue(bypass=True),20)}"
            ]
            self.transact.addTransaction(*text)
            soundsDict = {StockAsset:"buyStock",OptionAsset:"buyOption",IndexFundAsset:"buyStock"}
            soundEffects[soundsDict[type(newasset)]].play()
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

    def sellAsset(self,asset,quantity,feePercent=1) -> int:
        """sells the quantity number of the asset object given
        won't sell more than the quantity of the asset"""
        if self.runStateCheck(): return
        if quantity <= 0: return 0
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
        taxes = loss_gain*self.currentRun.getCurrVal("Tax Rate")/100 if loss_gain > 0 else 0
        self.taxesPaid += taxes
        loss_gain = loss_gain if loss_gain <= 0 else loss_gain*(1-self.currentRun.getCurrVal("Tax Rate")/100)
        self.realizedGains += loss_gain if loss_gain > 0 else 0
        value = (asset.getValue(bypass=True,fullvalue=False)*quantity)-taxes
        soundEffects['sellGain' if loss_gain > 0 else 'sellLoss'].play()
        text = [
            f"{self.gametime.getDate()}",
            f"Sold {limit_digits(quantity,20,True)} {asset.name} {self.assetText[type(asset)]+('s' if quantity > 1 else '')}",
             f"+${limit_digits(value,20)}",
            f"{'-' if loss_gain < 0 else '+'} ${limit_digits(abs(loss_gain),20) if loss_gain != 0 else '0'}",
            f"${limit_digits(self.cash+value,20)}"
        ]
        self.transact.addTransaction(*text)
        value = asset.getValue(bypass=True,fullvalue=False)*quantity*feePercent
        self.cash += value# add the value of the asset to the cash
        print('cash is',self.cash,asset.getValue(bypass=True,fullvalue=False)*quantity)
        assetlist[assetlist.index(asset)].quantity -= quantity# subtract the quantity from the asset
        self.assetsTraded += quantity
        if assetlist[assetlist.index(asset)].quantity <= 0:# if the quantity of the asset is 0 or less, remove the asset from the list
            assetlist.remove(asset)
        return value
        
    def removeAsset(self,asset):
        """removes the asset from the player's portfolio"""
        if self.runStateCheck(): return
        if isinstance(asset,StockAsset):
            assetlist = self.stocks 
        elif isinstance(asset,OptionAsset):
            assetlist = self.options
        elif isinstance(asset,IndexFundAsset):
            assetlist = self.indexFunds
        text = [
            f"{self.gametime.getDate()}",
            f"Removed {asset.getQuantity()} {asset.name} {self.assetText[type(asset)]+('s' if asset.getQuantity() > 1 else '')}",
            f"0",
            f"-{asset.ogValue*asset.getQuantity()}",
            f"${limit_digits(self.cash,20)}"
        ]
        soundEffects['sellLoss'].play()
        self.transact.addTransaction(*text)
        assetlist.remove(asset)

    def exerciseOption(self,optionObj:OptionAsset,quantity):
        """Executes the option
        Assumes that the player has enough money/stocks to execute the option"""
        if self.runStateCheck(): return
        if quantity <= 0: return 0
        if optionObj.optionType == "call":
            cost = optionObj.getStrike()*quantity*100
            self.cash -= cost
            self.stocks.append(StockAsset(self,optionObj.stockObj,self.gametime.time,optionObj.getStrike(),quantity*100))
            text = [
                f"{self.gametime.getDate()}",
                f"Executed {optionObj.getQuantity()} {optionObj.stockObj.name} Option{'s' if optionObj.getQuantity() != 1 else ''}",
                f"-${limit_digits(cost,20)}",
                f"+{limit_digits(quantity*100,20,True)} Share of {optionObj.stockObj.name}",
                f"${limit_digits(self.cash,20)}"
            ]
            self.transact.addTransaction(*text)
            soundEffects['buyStock'].play()
            optionObj.quantity -= quantity
            if optionObj.getQuantity() == 0:
                self.options.remove(optionObj)
                
        elif optionObj.optionType == "put":   
            value = optionObj.getStrike()*quantity*100
            stockQuantity = quantity*100# the quantity of stocks that the player will sell
            for stock in [s for s in self.stocks if s.stockObj == optionObj.stockObj]:# all the stocks that match the stock of the option
                if stock.quantity <= stockQuantity:
                    stockQuantity -= stock.quantity
                    self.stocks.remove(stock)
                else:
                    stock.quantity -= stockQuantity
                    break
            self.cash += value
            text = [
                f"{self.gametime.getDate()}",
                f"Executed {optionObj.getQuantity()} {optionObj.stockObj.name} Option{'s' if optionObj.getQuantity() != 1 else ''}",
                f"+${limit_digits(value,20)}",
                f"-{limit_digits(quantity*100,20,True)} Shares of {optionObj.stockObj.name}",
                f"${limit_digits(self.cash,20)}"
            ]
            self.transact.addTransaction(*text)
            soundEffects['sellGain'].play()
            optionObj.quantity -= quantity
            if optionObj.getQuantity() == 0:
                self.options.remove(optionObj)
    
    def purchaseCareerUpgrade(self,uString:str,careerRun:CareerRun):
        """Purchases the career upgrade"""
        if self.runStateCheck(): return
        cost = careerRun.getNextCost(uString)

        if self.cash >= cost:
            self.cash -= cost
            text = [
                f"{self.gametime.getDate()}",
                f"Purchased {uString}",
                f"-${limit_digits(cost,20)}",
                f"N/A",
                f"${limit_digits(self.cash,20)}"]
            careerRun.advanceUpgradeOrUnlock(uString)
            self.transact.addTransaction(*text)
            soundEffects['buyStock'].play()
        else:
            soundEffects['error'].play()
            errors.addMessage('Not Enough Cash',txtSize=100,coords=[960,540])
    def runStateCheck(self):
        """Check this anytime something is bought or sold"""
        if self.currentRun.state == 'complete':
            errors.addMessage('View only mode, run already complete',txtSize=100,coords=[960,540])
            return True
    def updateRunAssetSpread(self):
        """updates the asset spread of the game run"""
        self.gameRun.updateAssetSpread([sum([asset.getValue() for asset in self.stocks]),sum([asset.getValue() for asset in self.options]),sum([asset.getValue() for asset in self.indexFunds]),self.cash,self.getCurrentDebt()])
    def getStockQuantity(self,stockObj):
        """returns the number of stocks the player has of the stockObj"""
        return sum([stock.quantity for stock in self.stocks if stock.stockObj == stockObj])
        
    def getNumStocks(self,stockObj):
        """returns the number of stocks the player has of the stockObj"""
        return sum([stock.quantity for stock in self.stocks if stock.stockObj == stockObj])
    
    def getNumIndexFunds(self,indexFundObj):
        """returns the number of index funds the player has of the indexFundObj"""
        return sum([asset.quantity for asset in self.indexFunds if asset.stockObj == indexFundObj])

    def getNetworth(self):
        """returns the networth of the player"""
        allassets = self.stocks + self.options + self.indexFunds
        networth = self.cash + sum([asset.getValue() for asset in allassets])-sum([loan.principalLeft for loan in self.loans])
        if networth < 0:
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
        if self.runStateCheck(): return
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
        soundEffects['buyLoan'].play()
        
        animationList.append(BuyAnimation(pygame.mouse.get_pos(),100,animationList))
        self.cash += loanObj.principal
    def getCash(self):
        """returns the cash of the player"""
        return self.cash
    def getMaxPurchaseQty(self,asset):
        """returns the maximum quantity of stocks the player can buy"""
        return int(self.cash/asset.price)
    def getMaxLoan(self):
        """returns the maximum amount of money the player can borrow"""
        est = self.getNetworth()*self.currentRun.getCurrVal("Max Loan Amount")
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
        if self.runStateCheck(): return
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
        if self.runStateCheck(): return
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
        if self.runStateCheck(): return
        self.cash -= loanObj.addPayment(amount,self)
        text = [
            f"{self.gametime.getDate()}",
            f"Paid ${limit_digits(amount,20,amount>1000)} on Loan",
            f"-${limit_digits(amount,20,amount>1000)}",
            f"0",
            f"${limit_digits(self.cash,20)}"
        ]
        self.transact.addTransaction(*text)

        