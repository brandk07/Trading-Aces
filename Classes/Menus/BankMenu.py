import pygame
from Defs import *
from pygame import gfxdraw
from Classes.Menus.Menu import Menu
from Classes.imports.StockVisualizer import StockVisualizer
from Classes.imports.UIElements.SelectionElements import SelectionBar,MenuSelection
from Classes.imports.UIElements.PerfChart import PerfChart
from Classes.imports.UIElements.Numpad import Numpad
from Classes.imports.UIElements.OrderBox import OrderBox
from Classes.AssetTypes.IndexFundsAsset import IndexFundAsset
from Classes.imports.UIElements.Latterscroll import LinedLatter
from Classes.AssetTypes.LoanAsset import LoanAsset
import datetime
from Classes.imports.UIElements.SideScroll import SideScroll,CdCard,LoanCard


class BankMenu(Menu):
    def __init__(self,stocklist,gametime,player,transactions,tmarket,indexFunds:list,currentRun) -> None:
        super().__init__(currentRun)
        self.menuSelection = MenuSelection((200,105),(520,100),["Investments","Loans","Transactions"],45)
        # self.overView = OverView(player,transactions)
        self.menuSelection.setSelected("Investments")
        self.transactionScreen = TransactionScreen(transactions,player)
        self.loanScreen = LoanScreen(gametime,player,stocklist,self.currentRun)
        self.investScreen = InvestmentScreen(stocklist.copy(),gametime,player,tmarket,indexFunds.copy())
        self.menudrawn = False

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, player,gametime):

        self.menuSelection.draw(screen)
        
        match self.menuSelection.getSelected():
            # case "Overview":
            #     self.overView.draw(screen)
            case "Transactions":
                self.transactionScreen.draw(screen,gametime)
            case "Investments":
                self.investScreen.draw(screen,gametime)
            case "Loans":
                self.loanScreen.draw(screen)

class TransactionScreen:
    def __init__(self,transactions,player) -> None:
        self.player = player    
        self.transactions = transactions
        self.linedLatter = LinedLatter((1245,655),120)
    def draw(self,screen,gametime):
        # screen.blit(s_render("STATS",70,(220,220,220)),(200,210))
        drawCenterTxt(screen,"STATS",70,(220,220,220),(415,210),centerY=False)
        pygame.draw.rect(screen,(0,0,0),(200,265,430,705),5,border_radius=10)# rect for the stats

        vals = [self.player.lifeTimeVolume,self.player.realizedGains,self.player.taxesPaid,self.player.underTakenDebt,self.player.assetsTraded,self.player.interestPaid]

        strs = ["Lifetime Volume","Gains (Realized)","Taxes Paid","Debt UnderTaken","Assets Traded","Interest Paid"]
        data = [(string,("$"+limit_digits(val,20,val > 10000)) if string != strs[-2] else limit_digits(val,25,True)) for string,val in zip(strs,vals)]
        drawLinedInfo(screen,(210,275),(410,680),data,40,(220,220,220),diffSizes=(35,55))




        drawCenterTxt(screen,"TRANSACTIONS",70,(220,220,220),(1267,210),centerX=True,centerY=False)
        pygame.draw.rect(screen,(0,0,0),(635,265,1265,705),5,border_radius=10)# rect for the transactions

        txts = ["Date","Action","Balance Change","Profit/Unit Cost","Balance"]
        coords = [(705,275),(950,275),(1240,275),(1500,275),(1760,275)]
        for i,txt in enumerate(txts):
            drawCenterTxt(screen,txt,40,(220,220,220),coords[i],centerY=False)
        coords = [(705-635,20),(950-635,20),(1240-635,20),(1500-635,20),(1760-635,20)]

        if len(self.transactions.getTransactions()) == 0:
            self.linedLatter.setStrCoords([(1267-635,20)])
            self.linedLatter.setStrings([[["No Transactions",55,(220,220,220)]]])
        else:
            self.linedLatter.setStrCoords(coords)
            data = []
            for line in self.transactions.getTransactions():
                data.append([])
                for i,string in enumerate(line):
                    color = (220,220,220)
                    if i == 2:
                        color = (230,10,10) if "-" in string else (10,230,10)
                    elif i == 3:
                        if '-' in string: color = (230,10,10)
                        elif '+' in string: color = (10,230,10)
                    
                    data[-1].append((string,40,color))
                    
            self.linedLatter.setStrings(data)
        self.linedLatter.draw(screen,(640,315))

        # # print(self.transactions.getTransactions())
        # for i,transaction in enumerate(self.transactions.getTransactions()):
        #     # pygame.draw.rect(screen,(0,0,0),(735,315+(i*75),1155,65),3,border_radius=10)
        #     # draw a line between each one
        #     if i != 0:
        #         pygame.draw.line(screen,(0,0,0),(745,310+(i*75)),(1845,310+(i*75)),3)

        #     for ii,txt in enumerate(transaction):
        #         color = (220,220,220)
        #         if ii == 2:
        #             color = (230,10,10) if "-" in txt else (10,230,10)
        #         drawCenterTxt(screen,txt,32,color,(coords[ii][0],330+(i*75)),centerY=False)+


class CustomLoanCreator:
    def __init__(self,numpad,player) -> None:
        self.loanAmt, self.loanTerm = None, None
        self.player = player
        self.loanObj : LoanAsset = None
        self.numpad : Numpad = numpad
        self.numpadDisplay = None# LoanAmt or LoanTerm
    
    def stopCreating(self):
        self.loanAmt, self.loanTerm, self.loanObj, self.numpadDisplay = None, None, None, None
    def getLoanObj(self):
        return self.loanObj
    
    def drawLoanAmt(self,screen):
        drawCenterTxt(screen, 'Loan Amount', 45, (180, 180, 180), (575,225), centerX=False,centerY=False)

        if self.loanAmt is None and self.numpadDisplay != "LoanAmt":# if the loan amount has not been set
            result = drawClickableBoxWH(screen, (565,260), (300,65),"Set Value", 45, (160,160,160), (0,0,0),fill=True)
            if result:
                self.numpadDisplay = "LoanAmt"; self.numpad.reset()
        elif self.numpadDisplay == "LoanAmt" and self.loanAmt is None:# if the box has been clicked, but no value has been confirmed
            self.numpad.draw(screen,(200,215),(350,280),"",self.player.getCurrentMaxLoan())
            result = drawClickableBoxWH(screen, (210,475), (330,65),"Confirm Loan Amount", 45, (160,160,160), (0,0,0),fill=True)
            drawCenterTxt(screen, f"${self.numpad.getNumstr('',haveSes=False)}", 55, (225,225,225), (715, 292))
            if result:
                self.loanAmt = self.numpad.getValue()
                self.numpadDisplay = None
                self.numpad.reset()
            
            if self.loanAmt == 0: self.loanAmt = None
        else:
            # result = drawClickableBox(screen, (709, 250), f"${limit_digits(self.loanAmt,25,self.loanAmt>1000)}", 55, (200,200,200), (0,0,0),,border=False,centerX=True)
            pygame.draw.rect(screen,(0,0,0),(565,260,300,65),5,border_radius=10)
            result = drawClickableTxt(screen, (710, 292), f"${limit_digits(self.loanAmt,25,self.loanAmt>1000)}", 55, (225,225,225), (0,0,0),centerX=True,centerY=True)
            if result: self.numpadDisplay = "LoanAmt"; self.loanAmt = None

    def drawLoanTerm(self,screen):
        drawCenterTxt(screen, 'Loan Term', 45, (180, 180, 180), (575,330), centerX=False,centerY=False)

        if self.loanTerm is None and self.numpadDisplay != "LoanTerm":
            result = drawClickableBoxWH(screen, (565,365), (300,65),"Set Value", 45, (160,160,160), (0,0,0),fill=True)
            if result:
                self.numpadDisplay = "LoanTerm"; self.numpad.reset()
        elif self.numpadDisplay == "LoanTerm" and self.loanTerm is None:
            self.numpad.draw(screen,(200,215),(350,280),"",120)
            # self.numpad.draw(screen,(200,215),(350,335),"Loan Amount",0)
            result = drawClickableBoxWH(screen, (210,475), (330,65),"Confirm Loan Term", 45, (160,160,160), (0,0,0),fill=True)
            drawCenterTxt(screen, self.numpad.getNumstr('Month'), 55, (225,225,225), (715, 397))
            if result:
                self.loanTerm = self.numpad.getValue()
                self.numpadDisplay = None
                self.numpad.reset()
            
            if self.loanTerm == 0: self.loanTerm = None
        else:
            # result = drawClickableBox(screen, (715, 355), f"{self.loanTerm} Months", 55, (200,200,200), (0,0,0), ,border=False,centerX=True)
            pygame.draw.rect(screen,(0,0,0),(565,365,300,65),5,border_radius=10)    
            result = drawClickableTxt(screen, (715, 397), f"{self.loanTerm} Months", 55, (225,225,225), (0,0,0),centerX=True,centerY=True)
            if result: self.numpadDisplay = "LoanTerm"; self.loanTerm = None
        
    def drawLoanCreation(self,screen,interestRate):

        self.drawLoanAmt(screen)
        self.drawLoanTerm(screen)
        
        if self.loanAmt and self.loanTerm:
            if self.loanObj:
                self.loanObj.setValues(interestRate,self.loanTerm,self.loanAmt)
            else:
                self.loanObj = LoanAsset(interestRate,self.loanTerm,self.loanAmt)
        else:
            self.loanObj = None
        

class LoanScreen:
    def __init__(self,gametime,player,stocklist,currentRun) -> None:
        self.player = player
        self.currentRun = currentRun
        self.gametime = gametime
        self.numpad = Numpad(False,maxDecimals=0)
        self.paymentNumpad = Numpad(False)
        self.customLoanCreator = CustomLoanCreator(self.numpad,player)
        self.sideScroll = SideScroll((200,555),(1240,415),(375,375))
        self.orderBox = OrderBox((1445,215),(455,335),gametime)
        self.state = "View"# Creation, View, Modify
        self.networthGraph = StockVisualizer(gametime,player,stocklist)
        
        # data = {"term":12,"monthly payment":random.randint(10,250_000),"principal":10000,"remaining":16000}
        cardList = []
        # for i in range(35):
        #     data = {"term":random.randint(1,78),"monthly payment":random.randint(10,10000),"principal":random.randint(10,1000000),"remaining":random.randint(10,1000000)}
        #     cardList.append(LoanCard(f"Loan {i}",self.sideScroll,data,(375,375)))
        self.sideScroll.loadCards(cardList)
        self.addingPayment = False# Adding a payment to a existing loan (only in the modify state)


        
        
    def drawLoanCreator(self,screen,loanObj:LoanAsset):
       
        self.customLoanCreator.drawLoanCreation(screen,self.currentRun.getCurrVal("Loan Interest")/100)

        result = drawClickableBoxWH(screen, (565,470), (300,65),"Cancel", 45, (180,180,180), (45,0,0),fill=True)
        if result:
            self.customLoanCreator.stopCreating()
            self.state = "View"

        drawCenterTxt(screen,"Monthly Payment",40,(180,180,180),(885,295),centerX=False)
        if loanObj:
            payment,total,totalInterest = loanObj.getOGVals()
            drawCenterTxt(screen,f"${limit_digits(payment,20,payment>1000)}",115,(220,220,220),(1115,295),centerX=False)# draw the monthly payment

            info = [("Principal",f"${limit_digits(loanObj.principal,20,loanObj.principal>1000)}"),("Interest",f"${limit_digits(totalInterest,20,totalInterest>1000)}"),("Total",f"${limit_digits(total,20,total>1000)}")]
            if self.player.getMaxLoan() != 0:
                debtLimitPercent = ((loanObj.principal/self.player.getMaxLoan())*100)
                self.orderBox.loadData("1 Loan",f"$0",[("Principal",f"${limit_digits(loanObj.principal,20,loanObj.principal>1000)}",""),("Debt Limit %",f"{limit_digits(debtLimitPercent,20)}%","")])
                result = self.orderBox.draw(screen)
                if result:
                    self.player.addLoan(loanObj)
                    self.customLoanCreator.stopCreating()
                    self.state = "View"
                    # {"term":12,"monthly payment":random.randint(10,250_000),"principal":10000,"remaining":16000}
                    data = {"term":loanObj.termLeft,"monthly payment":payment,"principal":loanObj.principal,"remaining":loanObj.principal}
                    spot = 1 if not self.sideScroll.cards else max([int(c.name.split()[1]) for c in self.sideScroll.cards])+1
                    self.sideScroll.addCard(LoanCard(f"Loan {spot}",self.sideScroll,data))
                    loanObj = None
            else:
                print("max loan is zero")
                # self.sideScroll.addCard(LoanCard(f"Loan {len(self.player.loans)}",self.sideScroll,{"term":loanObj.term,"monthly payment":payment,"principal":loanObj.principal,"remaining":loanObj.principal}))
                # self.customLoanCreator.stopCreating()
        else:
            drawCenterTxt(screen,"N/A",115,(220,220,220),(1115,295),centerX=False)
            info = [("Principal","N/A"),("Interest","N/A"),("Total","N/A")]

        pygame.draw.rect(screen,(0,0,0),(870,350,555,190),5,border_radius=10)# box for the loan info
        drawLinedInfo(screen,(880,355),(535,180),info,38,(220,220,220))

        if self.customLoanCreator.numpadDisplay is None:
            drawCenterTxt(screen,"Custom Loan",70,(220,220,220),(375,225),centerY=False)
            if not self.customLoanCreator.loanAmt or not self.customLoanCreator.loanTerm:
                drawCenterTxt(screen,"Need to Set",60,(220,220,220),(375,300),centerY=False)
                if not self.customLoanCreator.loanAmt:
                    drawCenterTxt(screen,"- Loan Amount",45,(180,180,180),(375,360),centerY=False)
                if not self.customLoanCreator.loanTerm:
                    drawCenterTxt(screen,"- Loan Term",45,(180,180,180),(375,410),centerY=False)
            else:
                drawCenterTxt(screen,"All Set",55,(180,180,180),(375,300),centerY=False)

    def veiwState(self,screen):
        
        self.networthGraph.drawFull(screen,(1445,215),(455,335),"Loan Networth",True,"Normal")
        # drawCenterTxt(screen,"Loan Controls",70,(220,220,220),(375,225),centerY=False)

        drawCenterTxt(screen,"Loan Controls",70,(220,220,220),(375,225),centerY=False)
        drawCenterTxt(screen,"Create a Loan",45,(180,180,180),(375,300),centerY=False)
        drawCenterTxt(screen,"or Modify an",45,(180,180,180),(375,340),centerY=False)
        drawCenterTxt(screen,"Existing Loan",45,(180,180,180),(375,380),centerY=False)

        # txt = f"${limit_digits(self.player.getCurrentDebt(),20,self.player.getCurrentDebt()>1000)}"
        # drawCenterTxt(screen,txt,getTSizeNums(txt,600,155),(210,190,190),(997,382))
        # drawCenterTxt(screen,"Total Debt",55,(180,180,180),(997,225),centerY=False)
        info = [
            ("Max Debt Allowed",f"${limit_digits(self.player.getMaxLoan(),25)}"),
            ("Total Debt",f"${limit_digits(self.player.getCurrentDebt(),25,self.player.getCurrentDebt()>1000)}"),
            ("Lifetime Interest Paid",f"${limit_digits(self.player.interestPaid,20,self.player.interestPaid>1000)}"),
            ("Lifetime Debt Undertaken",f"${limit_digits(self.player.underTakenDebt,20,self.player.underTakenDebt>1000)}"),
        ]
        drawLinedInfo(screen,(565,225),(865,310),info,50,(200,200,200))




        result = drawClickableBox(screen, (375, 450), "+ Create New", 50, (200,200,200), (0,80,0),centerX=True,fill=True)
        if result:
            self.state = "Creation"
            self.customLoanCreator.stopCreating()



    def loanModifyingState(self,screen,loan:LoanAsset):

        if not self.addingPayment:
            drawCenterTxt(screen,"Modifying Loan",70,(220,220,220),(375,225),centerY=False)
            
            drawCenterTxt(screen,f"{self.sideScroll.getCard().name}",45,(180,180,180),(375,300),centerY=False)
        

        drawCenterTxt(screen, 'One Time Payment', 45, (180, 180, 180), (715,225), centerY=False)

        # drawCenterTxt(screen, 'Principal Remaining', 45, (180, 180, 180), (1135,225), centerX=False,centerY=False)
        # drawBoxedTextWH(screen, (1130,260), (300,65), f"${limit_digits(loan.principalLeft,20,loan.principalLeft>1000)}", 55, (220,220,220))
        
        # drawCenterTxt(screen, 'Principal Paid', 45, (180, 180, 180), (1135,330), centerX=False,centerY=False)
        # drawBoxedTextWH(screen, (1130,365), (300,65), f"${limit_digits(loan.principal,20,loan.principal>1000)}", 55, (220,220,220))
        
        # drawCenterTxt(screen, 'Interest Paid', 45, (180, 180, 180), (1135,435), centerX=False,centerY=False)
        # drawBoxedTextWH(screen, (1130,470), (300,65), f"${limit_digits(loan.interestPaid,20,loan.interestPaid>1000)}", 55, (220,220,220))
        info = [
            ('Principal Remaining',f"${limit_digits(loan.principalLeft,20,loan.principalLeft>1000)}"),
            ("Principal Paid",f"${limit_digits(loan.principal,20,loan.principal>1000)}"),
            ("Interest Paid",f"${limit_digits(loan.interestPaid,20,loan.interestPaid>1000)}"),
            ("Term Remaining",f"{loan.termLeft} Months"),
            ("Original Term",f"{loan.term} Months"),
            ("Interest Rate",f"{limit_digits(loan.rate*100,20)}%")
        ]
        drawLinedInfo(screen,(875,225),(550,315),info,40,(200,200,200),border=5)
        # pygame.draw.rect(screen,(0,0,0),(870,225,560,310),5,border_radius=10)# box for the loan info

        if not self.addingPayment:
            result = drawClickableBoxWH(screen, (565,275), (300,85),"+ Add Payment", 45, (160,160,160), (0,0,0),fill=True)
            self.networthGraph.drawFull(screen,(1445,215),(455,335),"Loan Networth",True,"Normal")
            if result: self.addingPayment = True

        if self.addingPayment:# if the user is adding a payment
            drawBoxedTextWH(screen, (565,260), (300,65), f"${limit_digits(self.paymentNumpad.getValue(),20,self.paymentNumpad.getValue()>1000)}", 55, (220,220,220))
            self.paymentNumpad.draw(screen,(200,215),(350,280),"",min(self.player.cash,loan.principalLeft))
            val = self.paymentNumpad.getValue()
            princ = loan.principalLeft

            drawCenterTxt(screen, 'New Est Monthly', 45, (180, 180, 180), (715,345), centerY=False)
            drawBoxedTextWH(screen, (565,380), (300,65), f"${limit_digits(loan.getLoanCalc(principal=loan.principalLeft-val),20,loan.getLoanCalc(principal=loan.principalLeft-val)>1000)}", 55, (220,220,220))

            
            result = drawClickableBoxWH(screen, (565,470), (300,65),"Cancel", 45, (180,180,180), (200,0,0))
            # result = drawClickableBox(screen, (565, 470), "Cancel", 45, (200,200,200), (225,0,0),)# draw the cancel button
            if result: self.addingPayment = False
            
            self.orderBox.loadData(f"-${limit_digits(val,25)}",f"${limit_digits(val,25)}",[("Principal Remaining ",f"${limit_digits(princ,20,princ>1000)}",""),("Principal After",f"${limit_digits(princ-val,20,princ-val>1000)}","")])
            result = self.orderBox.draw(screen)
            if result:
                self.player.addLoanPayment(loan,val)# add the payment to the loan
                self.addingPayment = False
    
    def refillLoanCards(self):
        cardList = []
        for i,loan in enumerate(self.player.loans):
            data = {"term":loan.termLeft,"monthly payment":loan.getMonthlyPayment(),"principal":loan.principal,"remaining":loan.principalLeft}
            cardList.append(LoanCard(f"Loan {i}",self.sideScroll,data))

        self.sideScroll.loadCards(cardList)

    def draw(self,screen):

        

        pygame.draw.rect(screen,(0,0,0),(200,215,350,335),5,border_radius=10)# box for the numpad

        pygame.draw.rect(screen,(0,0,0),(555,215,885,335),5,border_radius=10)# box for the loan Modifications
        if len(self.sideScroll.cards) != len(self.player.loans):
            self.refillLoanCards()
        for loan,card in zip(self.player.loans,self.sideScroll.cards):# update the loan cards
            card.updateData({"term":loan.termLeft,"monthly payment":loan.getMonthlyPayment(),"principal":loan.principal,"remaining":loan.principalLeft})
        

        self.sideScroll.draw(screen)
        if self.sideScroll.getCard() != None:
            self.state = "Modify"
            loanObj : LoanAsset = self.player.loans[self.sideScroll.getCard(index=True)]
        if self.state == "Modify" and self.sideScroll.getCard() is None:
            self.state = "View"

        if not self.sideScroll.cards:# if there are no cards
            drawCenterTxt(screen,"No Current Loans",110,(220,220,220),(820,700),centerY=False)


        
        pygame.draw.rect(screen,(0,0,0),(1445,555,455,415),5,border_radius=10)# box for the loan info
        drawCenterTxt(screen,"Debt Info",55,(0,0,0),(1445+227,565),centerY=False)
        
        info = [
            ("Debt Utilization",f"{limit_digits(self.player.getDebtUtilization(),25)}%"),
            ("Total Debt",f"${limit_digits(self.player.getCurrentDebt(),25,self.player.getCurrentDebt()>1000)}"),
            ("# of Loans",f"{len(self.player.loans)}"),
            ("Monthly Payment",f"${limit_digits(self.player.getMonthlyPayment(),25,self.player.getMonthlyPayment()>1000)}"),
            ("Interest Rate",f"{limit_digits(self.currentRun.getCurrVal("Loan Interest"),25)}%")
        ]
        drawLinedInfo(screen,(1455,615),(435,355),info,40,(215,215,215))

        

        if self.state == "Creation":
            loanObj : LoanAsset = self.customLoanCreator.getLoanObj()
            self.drawLoanCreator(screen,loanObj)
        elif self.state == "View":
            self.veiwState(screen)
        elif self.state == "Modify":
            self.loanModifyingState(screen,loanObj)
        
        # screen.blit(s_render("Monthly Payment",40,(220,220,220)),(885,275))
        
        


# class OverView:
#     def __init__(self,player,transactions) -> None:
#         self.player = player
#         self.transactions = transactions
#     def draw(self,screen):
#         pass

class InvestmentScreen:#
    def __init__(self,stocklist,gametime,player,tmarket,indexFunds) -> None:
        self.player = player
        self.sideScroll = SideScroll((200,210),(1200,450),(375,400))
        bankIcons = {}
        
        self.sideScroll.loadCards(list(bankIcons.values()))

        self.fundNumpad = Numpad(False,maxDecimals=0)
        self.fundOrderBox = OrderBox((1410,670),(475,300),gametime)

        self.indexFunds = indexFunds.copy(); self.indexFunds.append(tmarket)
        # self.indexGraphs : dict[str:StockVisualizer] = {}
        # for indexFund in self.indexFunds:
        #     self.indexGraphs[indexFund.name] = StockVisualizer(gametime,indexFund,stocklist)
        self.indexGraph = StockVisualizer(gametime,self.indexFunds[0],self.indexFunds)

        self.fundSelection = SelectionBar(horizontal=False)
        self.fundPerfChart = PerfChart((620,300))
        
        self.getRealSelc = lambda fakeSelect: ['Tech Digital Innovation Fund','Industrial Evolution Index Fund','Future Health Momentum',"Total Market"][["TDIF","IEIF", "FHMF","Total"].index(fakeSelect)]# Need since the fund names are abbreviated
        
        self.fundDescriptions = {
            "TDIF":"A specialized technology sector fund tracking emerging tech companies focused on quantum computing, neural interfaces, and cloud solutions, weighted based on market capitalization and innovation potential scores from industry analysts. (QSYN,NRLX,CMDX)",
            "IEIF":"A comprehensive industrial sector fund following next-generation manufacturing and logistics companies, with emphasis on automation, sustainable materials, and supply chain optimization. Portfolio balanced between established and emerging players. (PRBM, GFRG, ASCS)",
            "FHMF":"A healthcare sector fund tracking companies in personalized medicine, healthcare analytics, and senior care services. Weighted using a proprietary blend of clinical trial progress, market share, and long-term growth metrics. (BGTX, MCAN, VITL)",
            "Total":"Total Market is a index fund that tracks the entire market, providing a diversified portfolio of companies. It contains all 9 stocks in the market."
        }
        
    # def drawAssetInfo(self,screen,gametime,assetType):
  

        # if assetType == "Index Funds":
        #     txt = "An index fund is an investment that tracks the performance of an entire market, rather than a single stock. It accomplishes this by holding a portfolio of multiple companies within the market. This diversification helps to reduce risk and volatility, making index funds a popular choice for long-term investors."
        #     drawCenterTxt(screen,"Index Funds",60,(180,180,180),(1647,220),centerY=False)
        # txt = separate_strings(txt,7)
        # for i,line in enumerate(txt):
        #     # screen.blit(s_render(line,30,(220,220,220)),(1425,300+(i*40)))
        #     drawCenterTxt(screen,line,30,(220,220,220),(1647,300+(i*40)))
    def drawBuySellInfo(self,screen:pygame.Surface,gametime,fund):
        """Draws the info underneath On the left of the screen about the fund"""
        pygame.draw.rect(screen,(0,0,0),(1410,210,475,450),5,border_radius=10)# box around the buy/sell info
        drawCenterTxt(screen,"Fund Info",55,(180,180,180),(1647,220),centerY=False)
        strings = ["Open","High (1M)","Low (1M)","Dividend","Volatility"]
        g = gametime.time
        marketOpenTime = datetime.datetime.strptime(f"{g.month}/{g.day}/{g.year} 9:30:00 AM", "%m/%d/%Y %I:%M:%S %p")
        values = [
            f"${limit_digits(fund.getPointDate(marketOpenTime,gametime),12)}",
            f"${limit_digits(max(fund.graphs['1M']),12)}",
            f"${limit_digits(min(fund.graphs['1M']),12)}",
            f"{limit_digits(fund.getDividendYield(),12)}%",
            f"{limit_digits(fund.getVolatility()*100,12)}%"
            
        ]
        # info = {key:value for key,value in zip(keys,values)}
        info = [(string,value) for string,value in zip(strings,values)]
        drawLinedInfo(screen,(1410,270),(475,380),info,40,TXTCOLOR)

        pygame.draw.rect(screen,(0,0,0),(930,105,950,95),5,border_radius=10)# box for the max qty and qty owned
        maxQty = limit_digits(self.player.getMaxPurchaseQty(fund),20,True)
        qtyOwned = limit_digits(self.player.getNumIndexFunds(fund),20,True)
        drawCenterTxt(screen,f"Max Qty : {maxQty}",65,(180,180,180),(1167,152))
        drawCenterTxt(screen,f"Qty Owned : {qtyOwned}",65,(180,180,180),(1647,152))

    def drawIndexFundInfo(self,screen,gametime,fund):
        """Draws the information for the index fund (middle of the screen)"""
        drawCenterTxt(screen,self.getRealSelc(fund.name),50 if fund.name != "Total" else 60,fund.color,(1167,220),centerY=False)
        lines = 7
        if fund.name == "Total":
            lines = 5

        txt = self.fundDescriptions[fund.name]

        txt = separate_strings(txt,lines)
        for i,line in enumerate(txt):
            # screen.blit(s_render(line,30,(220,220,220)),(1425,300+(i*40)))
            drawCenterTxt(screen,line,35,(180,180,180),(1167,300+(i*40)))

    def drawIndexFunds(self,screen,gametime):

        self.fundSelection.draw(screen,["TDIF","IEIF", "FHMF","Total"],(200,210),(100,355),colors=[f.color for f in self.indexFunds])
        
        
        if self.fundSelection.getSelected() != None:
            # realName = self.getRealSelc(self.fundSelection.getSelected())# get the real name of the fund
            fund = [fund for fund in self.indexFunds if fund.name == self.fundSelection.getSelected()][0]# get the fund object
            # self.indexGraphs[self.fundSelection.getSelected()].drawFull(screen,(305,210),(620,450),self.fundSelection.getSelected(),True,"Normal")# draw the graph for the fund
            self.indexGraph.setStockObj(fund)
            self.indexGraph.drawFull(screen,(305,210),(620,450),"Main Investment Graph",True,"Normal")# draw the graph for the fund

            currentQ = gametime.getCurrentQuarter()# current game quarter

            self.fundPerfChart.updateData({f"Q{(i+(currentQ+1)-1)%4+1}":limit_digits(fund.getQuarterReturns((i+(currentQ+1)-1)%4+1,gametime),15) for i in range(4)})# update the data for the perf chart
            self.fundPerfChart.draw(screen,(305,670))# perf chart for the fund


            self.fundNumpad.draw(screen,(930,670),(475,320),"Shares",(0 if fund.price == 0 else int(self.player.cash/fund.price)))# draw the numpad
            pygame.draw.rect(screen,(0,0,0),(930,670,475,300),5,border_radius=10)# draw the numpad box

            pricePer = limit_digits(fund.getValue(),15)# price per share
            data = [("Value",f"${pricePer}","x")]# data for the order box
            totalCost = fund.getValue()*self.fundNumpad.getValue()*(1-2/100)# total cost of the shares

            self.fundOrderBox.loadData(self.fundNumpad.getNumstr('Share'),f"${limit_digits(totalCost,22)}",data)# load the data into the order box
            result = self.fundOrderBox.draw(screen)# draw the order box

            self.drawIndexFundInfo(screen,gametime,fund)

            self.drawBuySellInfo(screen,gametime,fund)
            
            if result and self.fundNumpad.getValue() > 0:# if the order box is clicked and the value is greater than 0
                fundObj = IndexFundAsset(self.player,fund,gametime.time,fund.price,self.fundNumpad.getValue())
                self.player.buyAsset(fundObj)

    def draw(self,screen,gametime):
        

        pygame.draw.rect(screen,(0,0,0),(930,210,475,450),5,border_radius=10)# for the indexFund info (deeper in depth for specific fund)
        self.drawIndexFunds(screen,gametime)

