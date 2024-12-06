
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

        self.orderBox = OrderBox((1050,605),(510,365))
        self.exerciseSelection : SelectionBar = SelectionBar()# Exercise, Sell, or Dimiss
        self.numPad = Numpad(displayText=False,nums=('DEL','0','MAX'))
        
        self.determineColor = lambda optionType: (127,25,255) if optionType == "put" else (50, 180, 169)# determines the color of the asset
    def drawn(self):
        return self.selectOption != None

    def setSelected(self,option):
        """Sets the exercise option to the given option"""
        self.selectOption = option

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
        self.numPad.draw(screen,(650,645),(390,345),"Shares",mousebuttons,maxQuantity)# draw the numpad
        
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
        self.numPad.draw(screen,(650,645),(390,345),"Shares",mousebuttons,maxQuantity)# draw the numpad

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
        self.numPad.draw(screen,(650,645),(390,345),"Options",mousebuttons,maxQuantity)# draw the numpad

        # Loads the orderBox with the information for the put option based on the numPad's quantity
        sellInfotxts = f"Allows the the option to be sold for it's estimated value instead of exercising it with a 2% fee"
        
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

        drawCenterTxt(screen, 'EXERCISE CHOICES', 120, (180, 180, 180), (1257, 105), centerY=False)

        self.exerciseSelection.draw(screen,["Exercise","Sell","Dismiss"],(650, 210),(1250,100),mousebuttons,txtsize=75)

        separatedTxts = []
        if self.exerciseSelection.getSelected() != "Dismiss":
            drawCenterTxt(screen, 'Option Quantity', 60, (180, 180, 180), (845, 600), centerY=False)# draws the title for the numpad


        match self.exerciseSelection.getSelected():
            case "Exercise":
                if self.selectOption.getType() == "call":
                    exerciseInfotxts = self.exerciseCallLogic(screen,mousebuttons)
                else:
                    exerciseInfotxts = self.exercisePutLogic(screen,mousebuttons)
                separatedTxts = separate_strings(exerciseInfotxts,4)
            case "Sell":
                separatedTxts = separate_strings(self.sellOptionLogic(screen,mousebuttons),4)
            case "Dismiss":
                separatedTxts = separate_strings(f"Dismisses and removes the option without any action. This is useful if the option is worthless",4)
                self.orderBox.loadData("Removing Option",f"$0",[("Action Irreversible","-","")])

        for i,string in enumerate(separatedTxts):# loop through the textlist and store the text info in the textinfo list
            drawCenterTxt(screen, string, 60, (180, 180, 180), (980, 325+50*i),centerY=False)


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

            
    def drawReqAndPay(self,screen:pygame.Surface,mousebuttons:int):
        """Draws the requirements and payment info for the exercise option"""

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(660, 315, 1230, 280),5,10)# box around the explaination text and the information
        
        drawCenterTxt(screen, 'Max Potential', 65, (0, 0, 0), (1655, 335), centerY=False)

        req = f"{limit_digits(self.selectOption.getQuantity(),20,True)} Option{'s' if self.selectOption.getQuantity() != 1 else ''}"
        payment = "None"
        if self.exerciseSelection.getSelected() == "Exercise":
            
            amt = self.selectOption.getQuantity()*100
            match self.selectOption.getType():
                case "call":
                    req = f"${limit_digits(amt*self.selectOption.getStrike(),20)}"# cost to buy the shares
                    payment = f"{limit_digits(amt,20,True)} shares of {self.selectOption.stockObj.name}"# shares to buy

                case "put":
                    req = f"{limit_digits(amt,20,True)} shares of {self.selectOption.stockObj.name}"# shares to sell
                    payment = f"${limit_digits(amt*self.selectOption.getStrike(),20)}"# payment for selling the shares

        elif self.exerciseSelection.getSelected() == "Sell":
            payment = f"${limit_digits(self.selectOption.getValue(fullvalue=False),20)} Per Unit"

        drawLinedInfo(screen,(1430,375),(450,215),[("Requires",f"{req}"),("Yields",f"{payment}")],45,TXTCOLOR)
        

    def drawScreen(self,screen,mousebuttons):
        if self.selectOption not in self.player.options:
            self.selectOption = None
            return None 
        
        self.selectedGraph.setStockObj(self.selectOption.stockObj)
        self.selectedGraph.drawFull(screen, (200,210),(450,340),"SellSelected",True,"Normal")

        self.drawOptionInfo(screen,self.gametime)
        self.drawExerciseChoices(screen,mousebuttons)
        self.drawReqAndPay(screen,mousebuttons)
        result = drawClickableBoxWH(screen, (1575,880),(325,80),"Cancel", 45, (180,180,180), (45,0,0), mousebuttons,fill=True)
        if result:
            self.selectOption = None