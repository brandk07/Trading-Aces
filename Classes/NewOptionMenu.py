import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.Menu import Menu
import numpy as np
from Classes.imports.Bar import SliderBar
from Classes.AssetTypes.OptionAsset import OptionAsset,getCloseOpenDate
from Classes.StockVisualizer import StockVisualizer
# from Classes.imports.OrderScreen import OrderScreen
from Classes.imports.Latterscroll import CustomColorLatter
from Classes.Stock import Stock
from Classes.imports.PieChart import PieChart
from Classes.Gametime import GameTime
from Classes.imports.BarGraph import BarGraph
from Classes.imports.Numpad import Numpad
from Classes.imports.SelectionElements import SelectionBar
from datetime import timedelta,datetime
from Classes.imports.OrderBox import OrderBox

class CustomOptionCreator:
    def __init__(self,player,optionObj) -> None:
        # self.newOptionInfo = None# list containing info for the new option that is being created, [strikePrice, expirationDate]
        self.strikePrice,self.expDate = None,None
        self.creatingOption = False
        self.player = player
        self.optionObj:Optiontrade = optionObj
        self.strikePad : Numpad = Numpad(displayText=False,nums=('DEL','0','.'))
        self.datePad : Numpad = Numpad(displayText=False,nums=('DEL','0','MAX'))
        self.oTypeSelect : SelectionBar = SelectionBar()
        self.cucOptionScrll = CustomColorLatter()
        self.numPadDisplay = None# Strike, or Date
        self.newOptionObj = None
        self.savedOptions : list[OptionAsset] = []# stores the saved options OptionAsset objects
        self.determineColor = lambda optionType: (127,25,255) if optionType == "put" else (50, 180, 169)# determines the color of the asset
    def removeSelc(self):
        self.selectOption = None
    def stopCreating(self):
        self.creatingOption = False
    
    def drawType(self,screen,mousebuttons):
        drawCenterTxt(screen, 'Type', 45, (200, 200, 200), (1700, 275), centerY=False)
        
        self.oTypeSelect.draw(screen, ["call","put"], (1575, 315), (250, 50), mousebuttons, colors=[(50, 180, 169),(127,25,255)],txtsize=35)
    
    def drawStrike(self,screen,mousebuttons,stock:Stock):
        drawCenterTxt(screen, 'Strike', 45, (180, 180, 180), (1530, 427), centerX=False)

        if self.strikePrice == None and self.numPadDisplay != "Strike":# if the strike price has not been set
            result = drawClickableBox(screen, (1875, 427), "Set Value", 45, (0,0,0), (160,160,160), mousebuttons,centerY=True,fill=True,topLeftX=True)
            if result:# if the box has been clicked to set the value (numpad displayed)
                self.numPadDisplay = "Strike"# changing it to strike so that the numpad will be displayed
        
        elif self.numPadDisplay == "Strike" and self.strikePrice == None:# if the box has been clicked, but no value has been confirmed
            self.strikePad.draw(screen,(1050,190),(450,340),"",mousebuttons,stock.price*2)# draw the numpad
            result = drawClickableBoxWH(screen, (1050, 510), (450,50),"Confirm Strike Value", 45, (160,160,160), (0,0,0), mousebuttons,fill=True)

            self.strikePrice = self.strikePad.getValue() if result else self.strikePrice
            self.numPadDisplay = None if result else self.numPadDisplay
            drawCenterTxt(screen, f"${self.strikePad.getNumstr(haveSes=False)}", 55, (200, 200, 200), (1850, 428),centerX=False,fullX=True)

            if self.strikePrice == 0: self.strikePrice = None# if the value is 0, then it is not a valid value
        
        else:# if the value has been confirmed
            
            result = drawClickableBox(screen, (1862, 428), f"${self.strikePad.getValue()}", 55, (200,200,200), (0,0,0), mousebuttons,centerY=True,border=False,topLeftX=True)
            if result: 
                self.numPadDisplay = "Strike"; self.strikePrice = None

    def drawDate(self,screen,mousebuttons,gametime:GameTime):
        dateTxt = s_render('Exp Date', 40, (200, 200, 200))
        screen.blit(dateTxt, (1530, 537-dateTxt.get_height()/2))
        # print(self.expDate)
        if self.expDate == None and self.numPadDisplay != "Date":
            result = drawClickableBox(screen, (1875, 537), "Set Date", 45, (0,0,0), (170,170,170),mousebuttons,centerY=True,fill=True,topLeftX=True)
            if result:# if the box has been clicked to set the date (numpad displayed)
                self.numPadDisplay = "Date"# changing it to date so that the numpad will be displayed

        elif self.numPadDisplay == "Date" and self.expDate == None:# if the box has been clicked, but no value has been confirmed
            
            self.datePad.draw(screen,(1050,190),(450,340),"Day",mousebuttons,365*3)# draw the numpad, max value of 3 years
            result = drawClickableBoxWH(screen, (1050, 510), (450,50),"Confirm Date", 45, (160,160,160), (0,0,0), mousebuttons,fill=True)

            self.expDate = self.datePad.getValue() if result else self.expDate
            self.numPadDisplay = None if result else self.numPadDisplay
            if result:
                newNumDays = (getCloseOpenDate(gametime.time+timedelta(days=self.datePad.getValue()))-gametime.time).days# gets the number of days from the current date to the new date (trading day)
                self.datePad.setValue(newNumDays)


            drawCenterTxt(screen, f"{self.datePad.getNumstr('Day',upperCase=False)}", 55, (200, 200, 200), (1860, 500),centerX=False,centerY=False,fullX=True)

            timeOffset = gametime.time+timedelta(days=self.datePad.getValue())
            drawCenterTxt(screen, f"{timeOffset.strftime('%m/%d/%Y')}", 40, (175, 175, 175), (1860, 545),centerX=False,centerY=False,fullX=True)

            if self.expDate == 0: self.expDate = None
        else:# if the value has been confirmed
            result = drawClickableBox(screen, (1885, 485), f"{self.datePad.getNumstr('Day',upperCase=False)}", 55, (200,200,200), (0,0,0), mousebuttons,border=False,topLeftX=True)
            if result: 
                self.numPadDisplay = "Date"; self.expDate = None
            timeOffset = gametime.time+timedelta(days=self.datePad.getValue())
            drawCenterTxt(screen, f"{timeOffset.strftime('%m/%d/%Y')}", 40, (120, 120, 120), (1860, 545),centerX=False,centerY=False,fullX=True)
    
    def drawEstPrice(self,screen,saveResult:bool,gametime:GameTime,stock:Stock):
        drawCenterTxt(screen, 'Est Price', 40, (200, 200, 200), (1530, 642), centerX=False)
            
        if self.strikePrice != None and self.expDate != None:# if the strike price and expiration date have been set
            if self.numPadDisplay == None:# if the value has been confirmed
                timeOffset = (gametime.time+timedelta(days=self.datePad.getValue()))
                
                if self.newOptionObj == None:# if the new option object has not been created
                    self.newOptionObj = OptionAsset(self.player,stock,self.strikePrice,timeOffset,self.oTypeSelect.getSelected(),str(gametime),1)
                else:# if the new option object has been created
                    self.newOptionObj.setValues(strikePrice=self.strikePrice,expDate=timeOffset,optionType=self.oTypeSelect.getSelected())
                
                price = self.newOptionObj.getValue(bypass=True)
                drawCenterTxt(screen, f"${limit_digits(price,15)}", 55, (200, 200, 200), (1860, 620), centerX=False, centerY=False,fullX=True)
                
                if saveResult:# if the save button has been clicked
                    self.savedOptions.append(self.newOptionObj)# save the new option
                    self.selectOption = self.newOptionObj# select the new option
                    self.strikePrice,self.newOptionObj,self.expDate = None, None, None# reset the new option info
                    self.datePad.reset(); self.strikePad.reset()# reset the numpad
                    self.creatingOption = False# stop creating the option

        if self.strikePrice == None or self.expDate == None or self.numPadDisplay != None:# if the strike price or expiration date have not been set
            drawCenterTxt(screen, f"N/A", 55, (200, 200, 200), (1860, 620), centerX=False, centerY=False,fullX=True)

    def drawCustOptions(self,screen:pygame.Surface,mousebuttons:int,gametime:GameTime,stock:Stock):
        """Handles the logic for creating a custom option"""

        
        if not self.creatingOption:# if there is no new option being created (display the create new option button)

            result = drawClickableBox(screen, (1700, 270), "+ Create New", 50, (200,200,200), (0,80,0), mousebuttons,centerX=True,fill=True)
            if result:
                self.creatingOption = True; self.selectOption = None; self.optionObj.removeSelc()
                
        else:# if there is a new option being created
            self.selectOption = None
            coords = [(265,110),(380,95),(480,115),(600,85)]# stores the y and height of the boxes [Type, strike, exp date, est price]
            for i,coord in enumerate(coords):
                pygame.draw.rect(screen,(0,0,0),pygame.Rect(1510,coord[0],375,coord[1]),5,10)

            self.drawType(screen,mousebuttons)# Draws, and handles the logic for setting the option type

            self.drawStrike(screen,mousebuttons,stock)# Draws, and handles the logic for setting the strike price
            
            self.drawDate(screen,mousebuttons,gametime)# Draws, and handles the logic for setting the expiration date
            
            saveResult = drawClickableBox(screen, (1515, 690), "Save", 45, (200,200,200), (0,225,0), mousebuttons)# draw the save button

            self.drawEstPrice(screen,saveResult,gametime,stock)# Draws, and handles the logic for setting the estimated price

            cancelResult = drawClickableBox(screen, (1750, 690), "Cancel", 45, (200,200,200), (225,0,0), mousebuttons)# draw the cancel button
            if cancelResult:
                self.strikePrice,self.expDate = None,None
                self.newOptionObj = None
                self.creatingOption = False
        return self.savedOptions

    def drawSavedOptions(self,screen:pygame.Surface,mousebuttons:int,gametime:GameTime,stock:Stock):
 
        # Coords for the latter scroll
        x,y = 1520, 770
        w,h = 365, 170
        if not self.creatingOption:
            y,h = 600, 340
            drawCenterTxt(screen, 'Saved Option', 45, (200, 200, 200), (1700, y-50), centerY=False)
            
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(x-5,y-10,w+10,h+10),5,10)
        
        optionList = [o for o in self.savedOptions if o.getStockObj() == stock]
        if len(optionList) == 0:
            drawCenterTxt(screen, f'No Saved {stock.name} Options', 40, (200, 200, 200), (1700, y+30), centerY=False)
            return None
        # DRAWING THE LATTER SCROLL
        daysLeft = lambda option: f'{option.daysToExpiration()} Day{"s" if option.daysToExpiration() > 1 else ""}'
        get_text = lambda option : [f'${limit_digits(option.getStrike(),12)} ',f'{option.getType().capitalize()}',f'{daysLeft(option)}']# returns the text for the stock
        textlist = [get_text(option) for option in optionList]# stores 3 texts for each asset in the stocks list

        textinfo = []# stores the text info for the latter scroll [text,fontsize,color]
        coords = [[(20,15)] for i in range(len(textlist))]

        for i,(text,option) in enumerate(zip(textlist,optionList)):# loop through the textlist and store the text info in the textinfo list
           
            polytexts = []# temporary list to store the text info for each asset
            polytexts.extend([[text[0],40,(255,255,255)],[text[1],40,self.determineColor(option.getType())],[text[2],40,(190,190,190)]])# appends the text info for the asset            
            textinfo.append(polytexts)
            coords[i].append(((text[0],25),15))
            coords[i].append(((text[1],165),15))

        self.cucOptionScrll.storetextinfo(textinfo); self.cucOptionScrll.set_textcoords(coords)# stores the text info and the coords for the latter scroll

        ommitted = self.cucOptionScrll.store_rendercoords((x, y), (w,y+h),80,0,0)
        select = self.selectOption if self.selectOption in optionList else None# Ensuring that the selected stock is in the optionlist
        selectedindex = None if select == None else optionList.index(select)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)
        
        newselected = self.cucOptionScrll.draw_polys(screen, (x, y), (w, y+h), mousebuttons, selectedindex, True, *[self.determineColor(option.getType()) for option in optionList[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        
        if newselected != None: self.creatingOption = False
        if select == None:# if the latterscroll didn't contain the selected asset before
            self.selectOption = self.selectOption if newselected == None else optionList[newselected]
        else:# if the latterscroll contained the selected asset before, then it can set it to none if you select it again
            self.selectOption = None if newselected == None else optionList[newselected]

        # self.selectOption = self.selectOption if newselected == None else optionList[newselected]# Changes selected stock if the new selected has something
        txt = s_render(f"{ommitted[0]} - {ommitted[1]-1} out of {len(optionList)} Options",35,(0,0,0))
        screen.blit(txt,(1700-txt.get_width()/2,950))
        return self.selectOption

class SellOptionScreen:
    def __init__(self,stocklist,gametime,player,screenSelection) -> None:
        self.player = player
        self.stocklist:list = stocklist
        self.gametime = gametime
        self.ownedScroll = CustomColorLatter()
        self.selectedGraph : StockVisualizer = StockVisualizer(gametime,stocklist[0],stocklist)
        self.netWorthGraph : StockVisualizer = StockVisualizer(gametime,player,stocklist)
        self.selectOption = None
        self.sortby = "Expiration"
        self.numpad = Numpad(displayText=False)
        self.screenSelection : SelectionBar = screenSelection# stores the screen selection object from the main game screen
        self.exerciseMenu : ExerciseOptionScreen = ExerciseOptionScreen(stocklist,gametime,player)
        self.orderBox = OrderBox((1030,615),(385,345))
        
        self.determineColor = lambda optionType: (127,25,255) if optionType == "put" else (50, 180, 169)# determines the color of the asset

    def drawSellingMechanics(self,screen:pygame.Surface,mousebuttons:int,gametime:GameTime,stock:Stock):

        pricePer = limit_digits(self.selectOption.getValue(bypass=True,fullvalue=False),15)
        fee = self.selectOption.getValue(bypass=False,fullvalue=False)*self.numpad.getValue()*2/100
        data = [("Value",f"${pricePer}","x"),(f"{2}% Fee", f"${limit_digits(fee,22)}","-")]

        totalCost = self.selectOption.getValue(bypass=False,fullvalue=False)*self.numpad.getValue()*(1-2/100)

        self.numpad.draw(screen,(670,600),(375,375),"Option",mousebuttons,self.selectOption.getQuantity())# draw the numpad
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(685, 615, 340, 335),5,10)# draw the box for the numpad

        self.orderBox.loadData(self.numpad.getNumstr('Option'),f"${limit_digits(totalCost,22)}",data)
        
        
        result = self.orderBox.draw(screen,mousebuttons)
        # # drawCenterTxt(screen, f"{self.numpad.getNumstr('Option')}", 65, (200, 200, 200), (1180, 630), centerY=False)
  
        # drawCenterTxt(screen, f"x ${limit_digits(self.selectOption.getValue(bypass=True,fullvalue=False),15)}", 55, (200, 200, 200), (1080, 710), centerX=False,centerY=False)

        
        # screen.blit(s_render(f"x {2}% fee", 55, (200, 200, 200)), (1085, 770))

        # # line inbetween 
        # pygame.draw.rect(screen,(200,200,200),pygame.Rect(1035, 820, 290, 5))

       

        # drawCenterTxt(screen, f"Total: ${limit_digits(totalCost,17)}", 65, (200, 200, 200), (1180, 845), centerY=False)

        # result = drawClickableBox(screen, (1180, 900), "Sell Quantity", 55, (200,200,200), (0,225,0) if self.numpad.getValue() > 0 else (0,0,0), mousebuttons,centerX=True)# draw the sell button

        if result and self.numpad.getValue() > 0:
            self.player.sellAsset(self.selectOption,self.numpad.getValue(),feePercent=1.02)


    def drawSellingInfo(self,screen:pygame.Surface,mousebuttons:int,gametime:GameTime,stock:Stock):
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1435, 105, 455, 520),5,10)# box around all the info
        drawCenterTxt(screen, 'Selling Info', 55, (0, 0, 0), (1662, 115),centerY=False)
        pygame.draw.line(screen, (0, 0, 0), (1450, 165), (1450+425, 165), 5)# line under selling info title

        sellInfotxts = ['Allows you to sell the option', 'before date of expiration at a', f"2% fee of it's estimated value"]
        
        for i,string in enumerate(sellInfotxts):
            drawCenterTxt(screen, string, 35, (200, 200, 200), (1662, 175+40*i),centerY=False)
        
        drawCenterTxt(screen, 'Exercise Info', 55, (0, 0, 0), (1662, 300), centerY=False)
        pygame.draw.line(screen, (0, 0, 0), (1450, 350), (1450+425, 350), 5)# line under exercise info title

        if self.selectOption != None:
            result = drawClickableBoxWH(screen, (1460, 520), (405,90), "EXERCISE SCREEN", 55, (0,0,0), (200,200,200), mousebuttons,fill=True)
            if result:
                self.exerciseMenu.setSelected(self.selectOption)

            exerciseInfotxts = f"When the option reaches it's expiration date, it can be exercised to "
            amt = self.selectOption.getQuantity()*100
            if self.selectOption.getType() == "call":
                exerciseInfotxts += f"buy {limit_digits(amt,20,True)} shares of {self.selectOption.stockObj.name} at ${self.selectOption.getStrike()} a share for a cost of ${limit_digits(amt*self.selectOption.getStrike(),20)}"
            else:# if the option is a put
                exerciseInfotxts += f"sell {limit_digits(amt,20,True)} shares of {self.selectOption.stockObj.name} at ${self.selectOption.getStrike()} a share"
            # print(separate_strings(exerciseInfotxts,5))
            for i,string in enumerate(separate_strings(exerciseInfotxts,4)):
                drawCenterTxt(screen, string, 35, (200, 200, 200), (1662, 365+40*i),centerY=False)

    def drawOptionInfo(self,screen:pygame.Surface, gametime):
        option = self.selectOption
        stockNameTxt = s_render(option.stockObj.name, 120, option.stockObj.color)
        optionTypeTxt = s_render(option.getType().capitalize(), 120, self.determineColor(option.getType()))
        totalWidth = stockNameTxt.get_width()+optionTypeTxt.get_width()+30
        screen.blit(stockNameTxt, (nameTxtX:=1047-totalWidth/2, 110))
        
        screen.blit(optionTypeTxt, (nameTxtX+stockNameTxt.get_width()+30, 110))

        # EXPIRATION INFO
        drawCenterTxt(screen, 'Expiration Info', 50, (0, 0, 0), (865, 220), centerY=False)
        # line under the title
        pygame.draw.line(screen, (0, 0, 0), (690, 270), (690+350, 270), 5)

        strings = ["Trading Days","Actual Days","Exp Date","Purchased"]
        g = gametime.time
        values = [
            f"{option.daysToExpiration()} Day{'s' if option.daysToExpiration() != 1 else ''}",
            f"{(option.getExpDate(False)-g).days} Day{'s' if option.getExpDate(False)-g != 1 else ''}",
            f"{option.getExpDate()}",
            f"{option.getPurchaseDate().strftime('%m/%d/%Y')}",
        ]
        # info = {key:value for key,value in zip(keys,values)}
        info = [(string,value) for string,value in zip(strings,values)]
        drawLinedInfo(screen,(680,290),(370,360),info,37,TXTCOLOR)
        

        # Other Info
        drawCenterTxt(screen, 'Other Info', 50, (0, 0, 0), (1245, 220), centerY=False)
        pygame.draw.line(screen, (0, 0, 0), (1070, 270), (1070+350, 270), 5)

        strings = ["Strike","Type","Dividend","Volatility"]
        values = [
            f"${option.getStrike()}",
            f"{option.optionType}",
            f"{limit_digits(option.stockObj.dividend,12)}%",
            f"{limit_digits(option.stockObj.getVolatility()*100,12)}%"
        ]
        info = [(string,value) for string,value in zip(strings,values)]
        drawLinedInfo(screen,(1060,290),(370,360),info,37,TXTCOLOR)

    def drawOwnedOptions(self,screen:pygame.Surface,mousebuttons:int):

        strike = drawClickableBoxWH(screen, (210, 910), (220,50), "Value", 45, (0,0,0), (200,200,200), mousebuttons,fill=True)
        exp = drawClickableBoxWH(screen, (455, 910), (220,50),"Expiration", 45, (0,0,0), (200,200,200), mousebuttons,fill=True)
        self.sortby = "Value" if strike else self.sortby
        self.sortby = "Expiration" if exp else self.sortby

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(200,210,465,665),5,10)# draws the box around the latter scroll
        drawCenterTxt(screen, 'Owned Options', 45, (180, 180, 180), (390, 220), centerY=False)

        
        # DRAWING THE LATTER SCROLL
        optionList = self.player.getOptions()
        if len(optionList) == 0:
            drawCenterTxt(screen, 'No Owned Options', 40, (200, 200, 200), (390, 300), centerY=False)
            return None
        if self.sortby == "Expiration":
            optionList.sort(key=lambda x: x.daysToExpiration())
        elif self.sortby == "Value":
            optionList.sort(key=lambda x: x.getValue(),reverse=True)
        # determineColor = lambda optionType: (127,25,255) if optionType == "put" else (50, 180, 169)# determines the color of the asset
        # dateText = lambda date: f'{date.month}/{date.day}/{date.year}'# returns the date in the format mm/dd/yyyy
        daysLeft = lambda option: f'{option.daysToExpiration()} Day{"s" if option.daysToExpiration() > 1 else ""}'
        get_text = lambda option : [f'{option.stockObj.name} {option.getType().capitalize()}',f"{limit_digits(option.getQuantity(),20,True)} Option{'s' if option.getQuantity() != 1 else ''}",f'${limit_digits(option.getValue(fullvalue=True),20)} ',f'{daysLeft(option)}']# returns the text for the stock
        textlist = [get_text(option) for option in optionList]# stores 3 texts for each asset in the stocks list

        textinfo = []# stores the text info for the latter scroll [text,fontsize,color]
        coords = [[(20,15),(30,60)] for i in range(len(textlist))]

        for i,(text,option) in enumerate(zip(textlist,optionList)):# loop through the textlist and store the text info in the textinfo list
            if self.selectOption == option:
                option.getValue(bypass=True)

            polytexts = []# temporary list to store the text info for each asset  - self.determineColor(option.getType())
            polytexts.extend([[text[0],45,option.stockObj.color],[text[1],40,(190,190,190)],[text[2],45,(220,220,220)],[text[3],40,(190,190,190)]])# appends the text info for the asset            
            textinfo.append(polytexts)
            coords[i].append((220,15))
            coords[i].append((230,60))

        self.ownedScroll.storetextinfo(textinfo); self.ownedScroll.set_textcoords(coords)# stores the text info and the coords for the latter scroll
        ommitted = self.ownedScroll.store_rendercoords((205, 270), (455,875),145,0,0,updatefreq=120)
    
        select = self.selectOption if self.selectOption in optionList else None# Ensuring that the selected stock is in the optionlist
        selectedindex = None if select == None else optionList.index(select)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)

        # newselected = self.ownedScroll.draw_polys(screen, (205, 270), (370,950), mousebuttons, selectedindex, True, *[self.determineColor(option.getType()) for option in optionList[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        newselected = self.ownedScroll.draw_polys(screen, (205, 270), (455,875), mousebuttons, selectedindex, True, *[brightenCol(self.determineColor(option.getType()),0.25) for option in optionList[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset

        if select == None:# if the latterscroll didn't contain the selected asset before
            self.selectOption = self.selectOption if newselected == None else optionList[newselected]# Changes selected stock if the new selected has something
        else:# if the latterscroll contained the selected asset before, then it can set it to none if you select it again
            self.selectOption = None if newselected == None else optionList[newselected]

        drawCenterTxt(screen, f"{ommitted[0]} - {ommitted[1]-1} out of {len(optionList)} Options", 35, (0, 0, 0), (432, 875), centerY=False)

    def drawScreen(self,screen,mousebuttons):
        
        if self.exerciseMenu.drawn():# if the exercise menu is drawn
            self.exerciseMenu.drawScreen(screen,mousebuttons)
        else:# if the exercise menu is not drawn
            if self.selectOption != None and self.selectOption not in self.player.getOptions():
                self.selectOption = None


            if self.selectOption == None:
                self.netWorthGraph.drawFull(screen, (1350,100),(550,500),"SellNetWorth",True,"Normal")

            self.drawOwnedOptions(screen,mousebuttons)
            self.drawSellingInfo(screen,mousebuttons,self.gametime,self.stocklist[0])
            if self.selectOption != None:
                self.drawOptionInfo(screen,self.gametime)
                
                self.drawSellingMechanics(screen,mousebuttons,self.gametime,self.stocklist[0])
                self.selectedGraph.setStockObj(self.selectOption.stockObj)
                self.selectedGraph.drawFull(screen, (1435,630),(465,345),"SellSelected",True,"Normal")
                # self.netWorthGraph.drawFull(screen, (1350,350),(550,250),"SellNetWorth",True,"Normal")

class ExerciseOptionScreen:

    def __init__(self,stocklist,gametime,player) -> None:
        self.player = player
        self.stocklist:list = stocklist
        self.gametime = gametime
        self.selectedGraph : StockVisualizer = StockVisualizer(gametime,stocklist[0],stocklist)

        self.selectOption = None

        self.exerciseSelection : SelectionBar = SelectionBar()# Exercise, Sell, or Dimiss
        
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
    
    def drawExerciseOptions(self,screen:pygame.Surface,mousebuttons:int):

        drawCenterTxt(screen, 'EXERCISE OPTIONS', 120, (180, 180, 180), (1257, 105), centerY=False)

        self.exerciseSelection.draw(screen,["Exercise","Sell","Dismiss"],(650, 210),(1250,100),mousebuttons,txtsize=75)

        seperatedTxts = []

        if self.exerciseSelection.getSelected() == "Exercise":
            exerciseInfotxts = f"Executes the option and gives the right to "
            amt = self.selectOption.getQuantity()*100
            if self.selectOption.getType() == "call":
                exerciseInfotxts += f"buy {limit_digits(amt,20,True)} shares of {self.selectOption.stockObj.name} at ${self.selectOption.getStrike()} a share for a cost of ${limit_digits(amt*self.selectOption.getStrike(),20)}"
            else:# if the option is a put
                exerciseInfotxts += f"sell {limit_digits(amt,20,True)} shares of {self.selectOption.stockObj.name} at ${self.selectOption.getStrike()} a share"
            seperatedTxts = separate_strings(exerciseInfotxts,4)
        
        elif self.exerciseSelection.getSelected() == "Sell":
            sellInfotxts = f"Allows you to sell the option for it's estimated value instead of exercising it, 2% fee of it's estimated value"
            seperatedTxts = separate_strings(sellInfotxts,4)
       
        elif self.exerciseSelection.getSelected() == "Dismiss":
            seperatedTxts = f"Dismisses and removes the option without any action,","-Useful if the option is worthless"

        for i,string in enumerate(seperatedTxts):# loop through the textlist and store the text info in the textinfo list
            drawCenterTxt(screen, string, 65, (200, 200, 200), (1265, 350+50*i),centerY=False)
    
    def drawReqAndPay(self,screen:pygame.Surface,mousebuttons:int):
        """Draws the requirements and payment info for the exercise option"""
        
        drawCenterTxt(screen, 'Requirements', 65, (0, 0, 0), (850, 640), centerY=False)
        pygame.draw.line(screen, (0, 0, 0), (675, 690), (675+350, 690), 5)# line under requirements title

        drawCenterTxt(screen, 'Payment', 65, (0, 0, 0), (1285, 640), centerY=False)
        pygame.draw.line(screen, (0, 0, 0), (1110, 690), (1110+350, 690), 5)# line under payment title
        
        req = "None"
        if self.exerciseSelection.getSelected() == "Exercise":
            
            amt = self.selectOption.getQuantity()*100
            if self.selectOption.getType() == "call":
                req = f"${limit_digits(amt*self.selectOption.getStrike(),20)}"# cost to buy the shares
            else:# if the option is a put
                req = f"{limit_digits(amt,20,True)} shares of {self.selectOption.stockObj.name}"# shares to sell

        drawCenterTxt(screen, req, 55, (200, 200, 200), (850, 720), centerY=False)

        payment = "None"
        if self.exerciseSelection.getSelected() == "Exercise":
            amt = self.selectOption.getQuantity()*100
            if self.selectOption.getType() == "call":
                payment = f"{limit_digits(amt,20,True)} shares of {self.selectOption.stockObj.name}"
            else:# if the option is a put
                payment = f"{limit_digits(amt*self.selectOption.getStrike(),20)}"
        elif self.exerciseSelection.getSelected() == "Sell":
            payment = f"{limit_digits(self.selectOption.getValue(fullvalue=False),20)}"
        drawCenterTxt(screen, payment, 55, (200, 200, 200), (1285, 720), centerY=False)
        

    def drawScreen(self,screen,mousebuttons):
        
        
        self.selectedGraph.setStockObj(self.selectOption.stockObj)
        self.selectedGraph.drawFull(screen, (200,210),(450,340),"SellSelected",True,"Normal")

        self.drawOptionInfo(screen,self.gametime)
        self.drawExerciseOptions(screen,mousebuttons)
        self.drawReqAndPay(screen,mousebuttons)
        




class Optiontrade(Menu):
    def __init__(self,stocklist:list,gametime,player):
        # self.icon = pygame.image.load(r'Assets\Portfolio\portfolio2.png').convert_alpha()

        self.icon = pygame.image.load(r'Assets\Menu_Icons\noblack_option3.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (140, 100))
        super().__init__(self.icon)
        self.player = player
        self.stocklist = stocklist
        self.gametime = gametime
        self.preMadeOptions = {}
        self.menudrawn = False
        self.fillPreMadeOptions()
        self.stockGraph : StockVisualizer = StockVisualizer(gametime,stocklist[0],stocklist)
        self.stockSelection : SelectionBar = SelectionBar()
        self.screenSelection : SelectionBar = SelectionBar()# Buy or Sell
        self.screenSelection.setSelected("Sell")

        self.customOptionSc = CustomOptionCreator(player,self)    
        self.sellingScreen = SellOptionScreen(stocklist,gametime,player,self.screenSelection)    
        
        self.quantNumPad : Numpad = Numpad(displayText=False,nums=('DEL','0','MAX'))
        stocknames = [stock.name for stock in stocklist]
        self.findStockObj = lambda name: stocklist[stocknames.index(name)] 
        self.avaOptionScrll = CustomColorLatter()
    
        self.savedOptions = []# stores the saved options OptionAsset objects
        self.selectOption = None
        self.determineColor = lambda optionType: (127,25,255) if optionType == "put" else (50, 180, 169)# determines the color of the asset
    def removeSelc(self):
        self.selectOption = None

    def createRandomOption(self,stock:Stock):
        def getRandomDate(gametime):
            extime = str(gametime.time+timedelta(days=random.randint(3,400)))
            while gametime.isOpen(datetime.strptime(extime, "%Y-%m-%d %H:%M:%S")) == False:#  Makes sure the expiration date is a trading day
                extime = str(gametime.time+timedelta(days=random.randint(3,400)))
            return extime
        optionType = random.choice(['call','put'])
        strikeprice = random.randint(math.floor(stock.price*0.8)*100,math.ceil(stock.price*1.05)*100)/100
        extime = getRandomDate(self.gametime)
        oObj = OptionAsset(self.player,stock,strikeprice,extime,optionType,str(self.gametime),1)
        return oObj

    def fillPreMadeOptions(self):        
        for stock in self.stocklist:
            self.preMadeOptions[stock] = []
            for _ in range(8):
                self.preMadeOptions[stock].append(self.createRandomOption(stock))

    def drawAvailableOptions(self,screen:pygame.Surface,mousebuttons:int,gametime:GameTime,stock:Stock):
        
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(200,210,380,740),5,10)
        # pygame.draw.rect(screen,(20,20,20),pygame.Rect(200,235,380,715),border_radius=10)
        avOptiontxt = s_render('Available Options', 45, (255, 255, 255))
        screen.blit(avOptiontxt, (390-avOptiontxt.get_width()/2, 220))

        
        # DRAWING THE LATTER SCROLL
        optionList = self.preMadeOptions[stock]
        # determineColor = lambda optionType: (127,25,255) if optionType == "put" else (50, 180, 169)# determines the color of the asset
        # dateText = lambda date: f'{date.month}/{date.day}/{date.year}'# returns the date in the format mm/dd/yyyy
        daysLeft = lambda option: f'{option.daysToExpiration()} Day{"s" if option.daysToExpiration() > 1 else ""}'
        get_text = lambda option : [f'${limit_digits(option.getValue(fullvalue=False),15)} ',f'{option.getType().capitalize()}',f'{daysLeft(option)}',f'{option.getExpDate()}']# returns the text for the stock
        textlist = [get_text(option) for option in optionList]# stores 3 texts for each asset in the stocks list

        textinfo = []# stores the text info for the latter scroll [text,fontsize,color]
        coords = [[(20,15),(30,60)] for i in range(len(textlist))]

        for i,(text,option) in enumerate(zip(textlist,optionList)):# loop through the textlist and store the text info in the textinfo list
            if self.selectOption == option:
                option.getValue(bypass=True)

            polytexts = []# temporary list to store the text info for each asset
            polytexts.extend([[text[0],50,(255,255,255)],[text[1],45,self.determineColor(option.getType())],[text[2],50,(190,190,190)],[text[3],30,(170,170,170)]])# appends the text info for the asset            
            textinfo.append(polytexts)
            coords[i].append(((text[1],150),15))
            coords[i].append(((text[1],155),60))

        self.avaOptionScrll.storetextinfo(textinfo); self.avaOptionScrll.set_textcoords(coords)# stores the text info and the coords for the latter scroll
        ommitted = self.avaOptionScrll.store_rendercoords((205, 270), (370,950),135,0,0,updatefreq=60)
    
        select = self.selectOption if self.selectOption in optionList else None# Ensuring that the selected stock is in the optionlist
        selectedindex = None if select == None else optionList.index(select)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)

        # newselected = self.avaOptionScrll.draw_polys(screen, (205, 270), (370,950), mousebuttons, selectedindex, True, *[self.determineColor(option.getType()) for option in optionList[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        newselected = self.avaOptionScrll.draw_polys(screen, (205, 270), (370,950), mousebuttons, selectedindex, True, *[brightenCol(self.determineColor(option.getType()),0.25) for option in optionList[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        if newselected != None: self.customOptionSc.stopCreating()

        if select == None:# if the latterscroll didn't contain the selected asset before
            self.selectOption = self.selectOption if newselected == None else optionList[newselected]# Changes selected stock if the new selected has something
        else:# if the latterscroll contained the selected asset before, then it can set it to none if you select it again
            self.selectOption = None if newselected == None else optionList[newselected]

        if self.selectOption != None and self.selectOption not in self.savedOptions:
            self.customOptionSc.removeSelc()
        txt = s_render(f"{ommitted[0]} - {ommitted[1]-1} out of {len(optionList)} Options",35,(0,0,0))
        screen.blit(txt,(390-txt.get_width()/2,950))


    def drawCustomOptions(self,screen:pygame.Surface,mousebuttons:int,gametime:GameTime,stock:Stock):

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1500,210,400,740),5,10)
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1500,210,400,50),5,10)

        drawCenterTxt(screen, 'Custom Options', 45, (200, 200, 200), (1700, 220), centerY=False)

        self.savedOptions = self.customOptionSc.drawCustOptions(screen,mousebuttons,gametime,stock)

        changeIt = False# only should be changed if the result is not none
        if self.selectOption != None and self.selectOption in self.savedOptions: 
            changeIt = True# if the selectOption is in this list then it should be changed
        result = self.customOptionSc.drawSavedOptions(screen,mousebuttons,gametime,stock)
        if changeIt:
            self.selectOption = result
        else: 
            self.selectOption = self.selectOption if result == None else result


    def drawOptionInfo(self,screen:pygame.Surface, gametime, stock:Stock):
        """Draws the info underneath the stock graph for the selected option"""
        strings = ["Strike","Ex Date","Days Till Ex","Dividend","Volatility","Allocation"]
        getAllo = lambda price : (price/(self.player.getNetworth()+price))*100# gets the allocation of the option
        values = [
            f"${self.selectOption.getStrike()}",
            f"{self.selectOption.getExpDate()}",
            f"{self.selectOption.daysToExpiration()}",
            f"{limit_digits(stock.dividend,12)}%",
            f"{limit_digits(stock.getVolatility()*100,12)}%",
            f"{limit_digits(getAllo(self.selectOption.getValue()),12)}%"
        ]
        # info = {key:value for key,value in zip(keys,values)}
        info = [(string,value) for string,value in zip(strings,values)]
        drawLinedInfo(screen,(590,660),(435,330),info,35,TXTCOLOR)

    def drawselectOption(self,screen:pygame.Surface,mousebuttons:int,gametime:GameTime,stock:Stock):
        if self.selectOption == None:
            return
        option = self.selectOption
        stockNameTxt = s_render(f"{stock.name}", 85, stock.color)# renders the stock name
        screen.blit(stockNameTxt, (585, 565))

        optionTypeTxt = s_render(f"({option.getType().capitalize()})", 50, self.determineColor(option.getType()))# renders the option type
        screen.blit(optionTypeTxt, (595+stockNameTxt.get_width(), 565+stockNameTxt.get_height()/2-optionTypeTxt.get_height()/2))

        self.drawOptionInfo(screen,gametime,stock)# draws the info underneath the stock graph for the selected option
        # print(self.player.cash,option.getValue(bypass=True,fullvalue=False))
        if option.getValue(bypass=True,fullvalue=False) > 0.01:
            maxQuant = int(self.player.cash//option.getValue(bypass=True,fullvalue=False))
        else:
            maxQuant = 0
        self.quantNumPad.draw(screen,(1050,190),(450,340),"Option",mousebuttons,maxQuant)# draw the numpad
        # self.selectOption.setValues(quantity=self.quantNumPad.getValue())# set the quantity of the option

        drawCenterTxt(screen, f"{self.quantNumPad.getNumstr('Option')}", 65, (200, 200, 200), (1275, 600), centerY=False)

        optionValTxt = s_render(f"x ${limit_digits(option.getValue(bypass=True,fullvalue=False),15)}", 55, (200, 200, 200))
        screen.blit(optionValTxt, (1180, 680))

        fee = 0 if self.selectOption in self.preMadeOptions[stock] else 2 
        screen.blit(s_render(f"x {fee}% fee", 55, (200, 200, 200)), (1180, 740))

        # line inbetween 
        pygame.draw.rect(screen,(200,200,200),pygame.Rect(1130, 790, 300, 5))

        totalCost = self.selectOption.getValue(bypass=True,fullvalue=False)*self.quantNumPad.getValue()*(1+fee/100)

        drawCenterTxt(screen, f"Total: ${limit_digits(totalCost,17)}", 65, (200, 200, 200), (1275, 815), centerY=False)

        result = drawClickableBox(screen, (1275, 880), "Confirm Purchase", 55, (200,200,200), (0,225,0) if self.quantNumPad.getValue() > 0 else (0,0,0), mousebuttons,centerX=True)# draw the buy button
        if result and self.quantNumPad.getValue() > 0:
            self.selectOption.setValues(quantity=self.quantNumPad.getValue(),creationDate=gametime.time)# set the quantity of the option
            print(self.quantNumPad.getValue(),"is the selected quantity")
            self.player.buyAsset(self.selectOption)
            print(self.selectOption.savingInputs())
            self.selectOption.setValues(quantity=1)# set back to 1
            self.selectOption = None
            self.quantNumPad.reset()
            




    def drawStockInfo(self,screen:pygame.Surface, gametime, stock:Stock):
        """Draws the info underneath the stock graph on the left"""
        if self.selectOption != None:
            return
        # if self.newOptionInfo == None or (self.newOptionInfo and type(self.strikePrice) != bool) and (self.newOptionInfo and type(self.newOptionInfo[1]) != bool):
        if self.customOptionSc.numPadDisplay == None and self.selectOption == None:   
            strings = ["Open","High (1M)","Low (1M)","Dividend","Volatility"]
            g = gametime.time
            marketOpenTime = datetime.strptime(f"{g.month}/{g.day}/{g.year} 9:30:00 AM", "%m/%d/%Y %I:%M:%S %p")
            values = [
                f"${limit_digits(stock.getPointDate(marketOpenTime,gametime),12)}",
                f"${limit_digits(max(stock.graphs['1M']),12)}",
                f"${limit_digits(min(stock.graphs['1M']),12)}",
                f"{limit_digits(stock.dividend,12)}%",
                f"{limit_digits(stock.getVolatility()*100,12)}%"
            ]
            # info = {key:value for key,value in zip(keys,values)}
            info = [(string,value) for string,value in zip(strings,values)]
            drawLinedInfo(screen,(1055,220),(435,370),info,40,TXTCOLOR)
    def checkOptionDates(self):
        """Checks if the options are still live, if not then it replaces them"""
        for option in self.savedOptions:
            if not option.optionLive():
                self.savedOptions.remove(option)
        for key,options in self.preMadeOptions.items():
            for i in range(len(options)):
                if not options[i].optionLive():# if the option is not live
                    self.preMadeOptions[key][i] = self.createRandomOption(key)# create a new random option
        if self.selectOption != None and not self.selectOption.optionLive():
            self.selectOption = None
            
    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player,gametime):
        
        self.screenSelection.draw(screen, ["Buy","Sell"], (200, 105), (375, 50), mousebuttons, colors=[(0,225,0),(225,0,0),(225,255,0)],txtsize=40)
        if self.screenSelection.getSelected() == "Buy":
            self.checkOptionDates()# Ensures that the options are still live

            if self.stockSelection.draw(screen, [stock.name for stock in stocklist], [585, 105], [1325, 65], mousebuttons, colors=[stock.color for stock in stocklist],txtsize=35):
                self.newOptionInfo = None
                self.newOptionObj = None
                self.selectOption = None

            stock = self.findStockObj(self.stockSelection.getSelected())
            self.stockGraph.setStockObj(stock)
            self.stockGraph.drawFull(screen, (585,210),(460,350),"OptionMenu Graph",True,"Normal")
            # if self.newOptionInfo == None or (self.newOptionInfo and type(self.strikePrice) != bool) and (self.newOptionInfo and type(self.newOptionInfo[1]) != bool):
            self.drawStockInfo(screen,gametime,stock)
            self.drawAvailableOptions(screen,mousebuttons,gametime,stock)
            self.drawCustomOptions(screen,mousebuttons,gametime,stock)
            self.drawselectOption(screen,mousebuttons,gametime,stock)
        elif self.screenSelection.getSelected() == "Sell":
            self.sellingScreen.drawScreen(screen,mousebuttons)


        


        
        

