
import pygame
from Defs import *
from Classes.imports.UIElements.SelectionElements import SelectionBar
from Classes.imports.UIElements.OrderBox import OrderBox
from Classes.imports.UIElements.Numpad import Numpad
from Classes.imports.StockVisualizer import StockVisualizer

class ExerciseOptionScreen:

    def __init__(self,stocklist,gametime,player) -> None:
        self.player = player
        self.stocklist:list = stocklist
        self.gametime = gametime
        self.selectedGraph : StockVisualizer = StockVisualizer(gametime,stocklist[0],stocklist)

        self.selectOption = None
        self.forced = False

        # self.orderBox = OrderBox((1050,605),(510,365),gametime)
        self.orderBox = OrderBox((665,605),(510,365),gametime)
        self.exerciseSelection : SelectionBar = SelectionBar(horizontal=False)# Exercise, Sell, or Dimiss
        self.exerciseSelection.setSelected("Exercise")
        self.numPad = Numpad(displayText=False,nums=('DEL','0','MAX'))
        
        self.determineColor = lambda optionType: (127,25,255) if optionType == "put" else (50, 180, 169)# determines the color of the asset
    def drawn(self):
        return self.selectOption != None

    def setSelected(self,option,forced=False):
        """Sets the exercise option to the given option"""
        self.selectOption = option
        self.forced = forced

    def drawOptionInfo(self,screen:pygame.Surface, gametime):
        option = self.selectOption; stock = option.stockObj

        stockNameTxt = s_render(f"{stock.name}", 100, stock.color)# renders the stock name
        screen.blit(stockNameTxt, (205, 560))

        optionTypeTxt = s_render(f"({option.getType().capitalize()})", 60, self.determineColor(option.getType()))# renders the option type
        screen.blit(optionTypeTxt, (215+stockNameTxt.get_width(), 570+stockNameTxt.get_height()/2-optionTypeTxt.get_height()/2))


        strings = ["Strike","Trading Days","Exp Date","Purchased"]
        values = [
            f"${option.getStrike()}",
            f"{option.daysToExpiration()} Day{'s' if option.daysToExpiration() != 1 else ''}",
            f"{option.getExpDate()}",
            f"{option.getPurchaseDate().strftime('%m/%d/%Y')}",
        ]
        info = [(string,value) for string,value in zip(strings,values)]
        drawLinedInfo(screen,(200,640),(435,300),info,37,TXTCOLOR)

    def exerciseCallLogic(self,screen,mousebuttons):
        """Handles the logic for exercising a call option"""
        # Draws the numpad for the quantity of shares to buy
        maxQuantity = min(self.selectOption.getQuantity(), int(self.player.cash/(self.selectOption.getStrike()*100)))# the maximum quantity of options that can be exercised
        self.numPad.draw(screen,(1180,605),(390,385),"Shares",mousebuttons,maxQuantity)# draw the numpad
        
        # Loads the orderBox with the information for the call option based on the numPad's quantity
        cost = self.numPad.getValue()*self.selectOption.getStrike()*100
        maxAmt = self.selectOption.getQuantity()*100# the maximum amount of shares that can be bought
        exerciseInfotxts = f"Executes the option and gives the right to "
        exerciseInfotxts += f"buy up to {limit_digits(maxAmt,20,True)} shares of {self.selectOption.stockObj.name} at ${self.selectOption.getStrike()} a share"
        currentAmt = self.numPad.getValue()*100# the current amount of shares that the player is buying throught the exercise
        self.orderBox.loadData(f"{limit_digits(self.numPad.getValue(),20,True)} Option{'s' if self.numPad.getValue() > 0 else ''}",f"${limit_digits(cost,20,True)}",[("Purchasing",f"{self.selectOption.stockObj.name}",""),("Quantity",f"{currentAmt}",""),("Cost",f"${limit_digits(cost,20,True)}","")])
        return exerciseInfotxts

    def exercisePutLogic(self,screen,mousebuttons):
        """Handles the logic for exercising a put option"""
        # Draws the numpad for the quantity of shares to sell
        numShares = self.player.getNumStocks(self.selectOption.stockObj)
        maxQuantity = min(int(numShares/100), self.selectOption.getQuantity())# the maximum quantity of options that can be exercised
        self.numPad.draw(screen,(1180,605),(390,385),"Shares",mousebuttons,maxQuantity)# draw the numpad

        # Loads the orderBox with the information for the put option based on the numPad's quantity
        amt = self.numPad.getValue()*100# the amount of shares that the player is selling
        maxAmt = self.selectOption.getQuantity()*100# the maximum amount of shares that can be sold
        exerciseInfotxts = f"Executes the option and gives the right to "
        exerciseInfotxts += f"sell up to {limit_digits(maxAmt,20,True)} shares of {self.selectOption.stockObj.name} at ${self.selectOption.getStrike()} a share"
        value = amt*self.selectOption.getStrike()
        self.orderBox.loadData(f"{limit_digits(self.numPad.getValue(),20,True)} Options",f"${limit_digits(value,20)}",[("Selling",f"{self.selectOption.stockObj.name}",""),("Num Shares",f"{limit_digits(amt,20,True)}","")])
        return exerciseInfotxts
    
    def sellOptionLogic(self,screen,mousebuttons):
        """Handles the logic for selling an option"""
        # Draws the numpad for the quantity of shares to sell
        maxQuantity = self.selectOption.getQuantity()# the maximum quantity of options that can be sold
        # self.numPad.draw(screen,(650,645),(390,345),"Options",mousebuttons,maxQuantity)# draw the numpad
        self.numPad.draw(screen,(1180,605),(390,385),"Options",mousebuttons,maxQuantity)# draw the numpad

        # Loads the orderBox with the information for the put option based on the numPad's quantity
        sellInfotxts = f"Allows the the option to be sold for it's estimated value at a 2% fee instead of exercising it"
        
        amt = self.numPad.getValue()# the amount of shares that the player is selling
        value = self.selectOption.getValue(bypass=True,fullvalue=False)# the value of the option just 1
        totalVal = value*amt# the total value of the options
        netgl = (value - self.selectOption.getOgVal())*amt# net gain/loss
        tax,fee  = self.player.taxrate * (0 if netgl <= 0 else netgl), totalVal * .02# the tax and fee for selling the option
        totalVal = totalVal - fee - tax
        self.orderBox.loadData(f"{limit_digits(amt,20,True)} Share{'s' if amt!=1 else ''}",f"${limit_digits(totalVal,20,True)}",[("Value",f"${limit_digits(value,20,value>1000)}","x"),(f"{round(self.player.taxrate*100,2)}% Tax",f"${limit_digits(tax,20)}","-"),(f"2% Fee",f"${limit_digits(fee,20)}","-")])
        return sellInfotxts
    
    def drawExerciseChoices(self,screen:pygame.Surface,mousebuttons:int):
        """Draws the Choices for exercising the option"""

        drawCenterTxt(screen, 'CHOICES', 100, (180, 180, 180), (1735, 120), centerY=False)
        drawCenterTxt(screen, self.exerciseSelection.getSelected(), 120, (180, 180, 180), (1110, 105), centerY=False)


        self.exerciseSelection.draw(screen,["Exercise","Sell","Dismiss"],(1560, 210),(340,380),mousebuttons,colors=[(19, 133, 100), (199, 114, 44), (196, 22, 62)],txtsize=75)

        separatedTxts = []
        if self.exerciseSelection.getSelected() != "Dismiss":
            # drawCenterTxt(screen, 'Option Quantity', 60, (180, 180, 180), (1735, 600), centerY=False)# draws the title for the numpad
            for i,string in enumerate(separate_strings("Use numpad for quantity selection",3)):# loop through the textlist and store the text info in the textinfo list
                drawCenterTxt(screen, string, 60, (180, 180, 180), (1735, 650+55*i),centerX=True,centerY=False)

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(660, 210, 890, 115),5,10)# box around the explaination text and the information
        # pygame.draw.rect(screen,(0,0,0),pygame.Rect(1185, 595, 360, 375),5,10)# box around the numpad
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1185, 605, 720, 365),5,10)# box around the numpad
        match self.exerciseSelection.getSelected():
            case "Exercise":
                if self.selectOption.getType() == "call":
                    exerciseInfotxts = self.exerciseCallLogic(screen,mousebuttons)
                else:
                    exerciseInfotxts = self.exercisePutLogic(screen,mousebuttons)
                separatedTxts = separate_strings(exerciseInfotxts,2)
            case "Sell":
                separatedTxts = separate_strings(self.sellOptionLogic(screen,mousebuttons),2)
            case "Dismiss":
                separatedTxts = separate_strings(f"Dismisses and removes the option without any action. This is useful if the option is worthless",2)
                self.orderBox.loadData("Removing Option",f"$0",[("Action Irreversible","-","")])

        for i,string in enumerate(separatedTxts):# loop through the textlist and store the text info in the textinfo list
            drawCenterTxt(screen, string, 55, (180, 180, 180), (1110, 225+45*i),centerX=True,centerY=False)


        result = self.orderBox.draw(screen,mousebuttons)

        if result:# if the order box has been clicked
            match self.exerciseSelection.getSelected():
                case "Exercise":
                    if self.selectOption.getType() == "call":
                        # self.player.buyStock(self.selectOption.stockObj,amt,self.selectOption.getStrike())
                        self.player.exerciseOption(self.selectOption,self.numPad.getValue())

                    else:# if the option is a put
                        self.player.exerciseOption(self.selectOption,self.numPad.getValue())
                case "Sell":
                    self.player.sellAsset(self.selectOption,self.numPad.getValue(),feePercent=1.02)
                case "Dismiss":
                    self.player.removeAsset(self.selectOption)
                    self.forced = False

            
    def drawReqAndPay(self,screen:pygame.Surface,mousebuttons:int):
        """Draws the requirements and payment info for the exercise option"""

        # pygame.draw.rect(screen,(0,0,0),pygame.Rect(660, 315, 1230, 280),5,10)# box around the explaination text and the information
        
        # drawCenterTxt(screen, 'Max Potential', 65, (170, 170, 170), (1655, 335), centerY=False)

        # drawCenterTxt(screen, 'Exercising One', 60, (170, 170, 170), (1250, 335), centerY=False)

        req = f"{limit_digits(self.selectOption.getQuantity(),20,True)} Option{'s' if self.selectOption.getQuantity() != 1 else ''}"
        maxPayment, onePayment, maxReq = "None","None","None"
        oneReq = f"1 {self.selectOption.name} Option"
        capacity = f"{limit_digits(self.selectOption.getQuantity(),20,True)} Options"
        
        if self.exerciseSelection.getSelected() == "Exercise":
            
            amt = self.selectOption.getQuantity()*100
            match self.selectOption.getType():
                case "call":
                    maxReq = f"${limit_digits(amt*self.selectOption.getStrike(),20)}"# cost to buy the shares
                    maxPayment = f"{limit_digits(amt,20,True)} shares of {self.selectOption.stockObj.name}"# shares to buy
                    oneReq = f"${limit_digits(self.selectOption.getStrike()*100,20)}"# cost to exercise one option
                    onePayment = f"100 Shares of {self.selectOption.stockObj.name}"# shares to buy with one option
                    possessed = f"{limit_digits(self.player.cash,25,True)} Shares"
                    capacity = f"{limit_digits(self.player.cash/(self.selectOption.getStrike()*100),25,True)}"
                    

                case "put":
                    maxReq = f"{limit_digits(amt,20,True)} shares of {self.selectOption.stockObj.name}"# shares to sell
                    maxPayment = f"${limit_digits(amt*self.selectOption.getStrike(),20)}"# payment for selling the shares
                    oneReq = f"100 Shares of {self.selectOption.stockObj.name}"# shares to sell with one option
                    onePayment = f"${limit_digits(self.selectOption.getStrike()*100,20)}"# payment for selling one option
                    possessed = f"{self.player.getNumStocks(self.selectOption.stockObj)} Shares"
                    capacity = f"{limit_digits(self.player.getNumStocks(self.selectOption.stockObj)/100,25,True)}"

        elif self.exerciseSelection.getSelected() == "Sell":
            maxPayment = f"${limit_digits(self.selectOption.getValue(fullvalue=False),20)} Per Option"
            onePayment = f"${limit_digits(self.selectOption.getValue(fullvalue=False),20)} Per Option"
            maxReq = f"{limit_digits(self.selectOption.getQuantity(),20,True)} Options"
            # oneReq = f"1 {self.selectOption.name} Option"
            possessed = f"{limit_digits(self.selectOption.getQuantity(),20,True)} Options"
        elif self.exerciseSelection.getSelected() == "Dismiss":
            possessed = f"{limit_digits(self.selectOption.getQuantity(),20,True)} Options"
            onePayment = "$0"
        # colors = [
        #     # (25, 40, 80),    # Deep navy blue
        #     # (224, 27, 165),   # Violet 
        #     (207, 185, 21),   # Gold
            
        #     (186, 167, 19),      # Gold
        #     # (0, 170, 170),   # Aqua
        #     (143, 128, 14)
        # ]
        drawLinedInfo(screen,(1100,330),(420,260),[("Option Qty","Max"),("Requires",f"{maxReq}"),("Yields",f"{maxPayment}"),("Present Capacity",capacity)],38,color=(207, 142, 21))
        ownedOrcash = "Cash" if self.exerciseSelection.getSelected() == "Sell" else "Shares Owned" 
        drawLinedInfo(screen,(665,330),(420,260),[("Option Qty","1"),("Requires",f"{oneReq}"),("Yields",f"{onePayment}"),(ownedOrcash,possessed)],38,color=(207, 185, 21))
        # drawLinedInfo(screen,(1460,375),(420,215),[("Requires",f"{maxReq}"),("Yields",f"{maxPayment}"),("Present Capacity",capacity)],38,TXTCOLOR)
        # drawLinedInfo(screen,(1040,375),(420,215),[("Requires",f"{oneReq}"),("Yields",f"{onePayment}"),("Possessed",possessed)],38,TXTCOLOR)
        

    def drawScreen(self,screen,mousebuttons):
        if self.selectOption not in self.player.options:
            self.selectOption = None; self.forced = False
            return None 
        
        self.selectedGraph.setStockObj(self.selectOption.stockObj)
        self.selectedGraph.drawFull(screen, (200,210),(450,340),"SellSelected",True,"Normal",mousebuttons)
        if self.forced:
            drawCenterTxt(screen, 'Option Expired', 120, (185, 0, 0), (205, 105),centerX=False, centerY=False)

        self.drawOptionInfo(screen,self.gametime)
        self.drawExerciseChoices(screen,mousebuttons)
        self.drawReqAndPay(screen,mousebuttons)

        result = drawClickableBoxWH(screen, (1565,880),(325,80),"Cancel", 45, (180,180,180), (45,0,0), mousebuttons,fill=True)
        if result: self.selectOption = None; self.forced = False