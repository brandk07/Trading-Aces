import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.Menu import Menu
import numpy as np
from Classes.imports.Bar import SliderBar
from Classes.AssetTypes.OptionAsset import OptionAsset
from Classes.StockVisualizer import StockVisualizer
# from Classes.imports.OrderScreen import OrderScreen
from Classes.imports.Latterscroll import CustomColorLatter
from Classes.Stock import Stock
from Classes.imports.PieChart import PieChart
from Classes.Gametime import GameTime
from Classes.imports.BarGraph import BarGraph
from Classes.imports.Numpad import Numpad
from Classes.imports.SelectionBar import SelectionBar
from datetime import timedelta,datetime

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
        self.menudrawn = True
        self.fillPreMadeOptions()
        self.stockGraph : StockVisualizer = StockVisualizer(gametime,stocklist[0],stocklist)
        self.stockSelection : SelectionBar = SelectionBar()
        self.oTypeSelect : SelectionBar = SelectionBar()
        self.strikeNumPad : Numpad = Numpad(displayText=False,nums=('DEL','0','.'))
        self.dateNumPad : Numpad = Numpad(displayText=False,nums=('DEL','0','MAX'))
        self.quantNumPad : Numpad = Numpad(displayText=False,nums=('DEL','0','MAX'))
        stocknames = [stock.name for stock in stocklist]
        self.findStockObj = lambda name: stocklist[stocknames.index(name)] 
        self.avaOptionScrll,self.cucOptionScrll = CustomColorLatter(),CustomColorLatter()
        # self.selectedOption = None
        self.newOptionInfo = None# list containing info for the new option that is being created, [strikePrice, expirationDate]
        self.newOptionObj = None
        self.savedOptions = []# stores the saved options OptionAsset objects
        # self.selectedOption = None
        self.selectedOption = None
        self.determineColor = lambda optionType: (127,25,255) if optionType == "put" else (50, 180, 169)# determines the color of the asset

    def fillPreMadeOptions(self):

        def getRandomStrike(stock:Stock,optiontype:str):
            return random.randint(math.floor(stock.price*0.8)*100,math.ceil(stock.price*1.05)*100)/100
            # self.calloptions.append(OptionAsset(player,stock,strikeprice,extime,'call',str(gametime),1))

        def getRandomDate(gametime):
            extime = str(gametime.time+timedelta(days=random.randint(3,400)))
            while gametime.isOpen(datetime.strptime(extime, "%Y-%m-%d %H:%M:%S")) == False:#  Makes sure the expiration date is a trading day
                extime = str(gametime.time+timedelta(days=random.randint(3,400)))
            return extime
        for stock in self.stocklist:
            self.preMadeOptions[stock] = []
            for _ in range(8):
                optionType = random.choice(['call','put'])
                strikeprice = getRandomStrike(stock,optionType)
                extime = getRandomDate(self.gametime)
                oObj = OptionAsset(self.player,stock,strikeprice,extime,optionType,str(self.gametime),1)
                self.preMadeOptions[stock].append(oObj)

    def drawAvailableOptions(self,screen:pygame.Surface,mousebuttons:int,gametime:GameTime,stock:Stock):
        
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(200,210,380,740),5,10)
        # pygame.draw.rect(screen,(20,20,20),pygame.Rect(200,235,380,715),border_radius=10)
        avOptiontxt = s_render('Available Options', 45, (255, 255, 255))
        screen.blit(avOptiontxt, (390-avOptiontxt.get_width()/2, 220))

        
        # DRAWING THE LATTER SCROLL
        optionList = self.preMadeOptions[stock]
        # determineColor = lambda optionType: (127,25,255) if optionType == "put" else (50, 180, 169)# determines the color of the asset
        # dateText = lambda date: f'{date.month}/{date.day}/{date.year}'# returns the date in the format mm/dd/yyyy
        daysLeft = lambda option: f'{option.daysToExpiration(gametime.time)} Day{"s" if option.daysToExpiration(gametime.time) > 1 else ""}'
        get_text = lambda option : [f'${limit_digits(option.getValue(),15)} ',f'{option.getType().capitalize()}',f'{daysLeft(option)}',f'{option.getExpDate()}']# returns the text for the stock
        textlist = [get_text(option) for option in optionList]# stores 3 texts for each asset in the stocks list

        textinfo = []# stores the text info for the latter scroll [text,fontsize,color]
        coords = [[(20,15),(30,60)] for i in range(len(textlist))]

        for i,(text,option) in enumerate(zip(textlist,optionList)):# loop through the textlist and store the text info in the textinfo list
            if self.selectedOption == option:
                option.getValue(bypass=True)

            polytexts = []# temporary list to store the text info for each asset
            polytexts.extend([[text[0],50,(255,255,255)],[text[1],45,self.determineColor(option.getType())],[text[2],50,(190,190,190)],[text[3],30,(170,170,170)]])# appends the text info for the asset            
            textinfo.append(polytexts)
            coords[i].append(((text[1],150),15))
            coords[i].append(((text[1],155),60))

        self.avaOptionScrll.storetextinfo(textinfo); self.avaOptionScrll.set_textcoords(coords)# stores the text info and the coords for the latter scroll
        ommitted = self.avaOptionScrll.store_rendercoords((205, 270), (370,950),135,0,0,updatefreq=60)
    
        select = self.selectedOption if self.selectedOption in optionList else None# Ensuring that the selected stock is in the optionlist
        selectedindex = None if select == None else optionList.index(select)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)

        # newselected = self.avaOptionScrll.draw_polys(screen, (205, 270), (370,950), mousebuttons, selectedindex, True, *[self.determineColor(option.getType()) for option in optionList[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        newselected = self.avaOptionScrll.draw_polys(screen, (205, 270), (370,950), mousebuttons, selectedindex, True, *[brightenCol(self.determineColor(option.getType()),0.25) for option in optionList[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        self.selectedOption = self.selectedOption if newselected == None else optionList[newselected]# Changes selected stock if the new selected has something
        txt = s_render(f"{ommitted[0]} - {ommitted[1]-1} out of {len(optionList)} Options",35,(0,0,0))
        screen.blit(txt,(390-txt.get_width()/2,950))
    
    def drawSavedCustomOptions(self,screen:pygame.Surface,mousebuttons:int,gametime:GameTime,stock:Stock):
        createNew = self.newOptionInfo != None
        # Coords for the latter scroll
        x,y = 1520, 770
        w,h = 365, 170
        if not createNew:
            y,h = 600, 340
            avOptiontxt = s_render('Saved Options', 45, (255, 255, 255))
            screen.blit(avOptiontxt, (1700-avOptiontxt.get_width()/2, y-50))
            

        # pygame.draw.rect(screen,(0,0,0),pygame.Rect(1515,760,375,180),5,10)
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(x-5,y-10,w+10,h+10),5,10)
        # pygame.draw.rect(screen,(20,20,20),pygame.Rect(200,235,380,715),border_radius=10)
        
        optionList = [o for o in self.savedOptions if o.getStockObj() == stock]
        if len(optionList) == 0:
            txt = s_render(f'No Saved {stock.name} Options', 40, (255, 255, 255))
            screen.blit(txt, (1700-txt.get_width()/2, y+30))
            return
        # DRAWING THE LATTER SCROLL
        
        # dateText = lambda date: f'{date.month}/{date.day}/{date.year}'# returns the date in the format mm/dd/yyyy
        daysLeft = lambda option: f'{option.daysToExpiration(gametime.time)} Day{"s" if option.daysToExpiration(gametime.time) > 1 else ""}'
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
        select = self.selectedOption if self.selectedOption in optionList else None# Ensuring that the selected stock is in the optionlist
        selectedindex = None if select == None else optionList.index(select)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)
        
        newselected = self.cucOptionScrll.draw_polys(screen, (x, y), (w, y+h), mousebuttons, selectedindex, True, *[self.determineColor(option.getType()) for option in optionList[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        
        if select == None:# if the latterscroll didn't contain the selected asset before
            self.selectedOption = self.selectedOption if newselected == None else optionList[newselected]
        else:# if the latterscroll contained the selected asset before, then it can set it to none if you select it again
            self.selectedOption = None if newselected == None else optionList[newselected]

        # self.selectedOption = self.selectedOption if newselected == None else optionList[newselected]# Changes selected stock if the new selected has something
        txt = s_render(f"{ommitted[0]} - {ommitted[1]-1} out of {len(optionList)} Options",35,(0,0,0))
        screen.blit(txt,(1700-txt.get_width()/2,950))

    def customOptionLogic(self,screen:pygame.Surface,mousebuttons:int,gametime:GameTime,stock:Stock):
        """Handles the logic for creating a custom option"""
        # pygame.draw.rect(screen,(0,0,0),pygame.Rect(1510,260,390,415),5,10)

        
        if self.newOptionInfo == None:# if there is no new option being created (display the create new option button)
            # pygame.draw.rect(screen,(0,0,0),pygame.Rect(1520,270,200,50),5,10)
            # createColor = (0,190,0)
            # if pygame.Rect(1520,270,200,50).collidepoint(pygame.mouse.get_pos()):
            #     createColor = (0,255,0)
            #     if mousebuttons == 1:
            #         # newOptionInfo is [strikePrice, expirationDate]
            #         self.newOptionInfo = [None,None,None]# changing it, the nones represent that no data is in it yet so it will display a set value box
            
            # createTxt = s_render('+ Create New', 50, createColor)
            # screen.blit(createTxt, (1700-createTxt.get_width()/2, 290))
            result = drawClickableBox(screen, (1700, 270), "+ Create New", 50, (200,200,200), (0,80,0), mousebuttons,centerX=True,fill=True)
            if result:
                self.newOptionInfo = [None,None,None]
                
        else:# if there is a new option being created
            coords = [(265,110),(380,95),(480,115),(600,85)]# stores the y and height of the boxes [Type, strike, exp date, est price]
            for i,coord in enumerate(coords):
                pygame.draw.rect(screen,(0,0,0),pygame.Rect(1510,coord[0],375,coord[1]),5,10)
                
            typeTxt = s_render('Type', 45, (200, 200, 200))
            screen.blit(typeTxt, (1700-typeTxt.get_width()/2, 275))
            
            # screen.blit(typeTxt, (1530, 325-typeTxt.get_height()/2))
            # wh = 250
            # 1575-320(127,25,255) if optionType == "put" else (50, 180, 169)
            self.oTypeSelect.draw(screen, ["Call","Put"], (1575, 315), (250, 50), colors=[(50, 180, 169),(127,25,255)],txtsize=35)

            # --------------------------------------- STRIKE PRICE ----------------------------------
            strikeTxt = s_render('Strike', 45, (180, 180, 180))
            screen.blit(strikeTxt, (1530, 427-strikeTxt.get_height()/2))
            # strikeTxt = s_render('Strike Price', 40, (200, 200, 200))
            # screen.blit(strikeTxt, (1700-strikeTxt.get_width()/2, 385))

            if self.newOptionInfo[0] == None:
                result = drawClickableBox(screen, (1875, 427), "Set Value", 45, (0,0,0), (160,160,160), mousebuttons,centerY=True,fill=True,topLeftX=True)
                # result = drawClickableBox(screen, (1700, 420), "Set Value", 45, (0,0,0), (160,160,160), mousebuttons,centerX=True,fill=True)
                if result:# if the box has been clicked to set the value (numpad displayed)
                    self.newOptionInfo[0] = True# changing it to true so that the numpad will be displayed
                    self.newOptionInfo[1] = None if self.newOptionInfo[1] == True else self.newOptionInfo[1]# if the box has been clicked for setting a value, but no value has been confirmed
            
            elif type(self.newOptionInfo[0]) == bool:# if the box has been clicked, but no value has been confirmed
                self.strikeNumPad.draw(screen,(1050,190),(450,340),"",mousebuttons,stock.price*2)# draw the numpad
                result = drawClickableBoxWH(screen, (1050, 510), (450,50),"Confirm Strike Value", 45, (160,160,160), (0,0,0), mousebuttons,fill=True)
                if result:
                    self.newOptionInfo[0] = self.strikeNumPad.getValue()# ensure that the strike price is at least 1
                numValTxt = s_render(f"${self.strikeNumPad.getNumstr(haveSes=False)}", 55, (200, 200, 200))
                # screen.blit(numValTxt, (1700-numValTxt.get_width()/2, 430))
                screen.blit(numValTxt, (1850-numValTxt.get_width(), 428-numValTxt.get_height()/2))
                if self.newOptionInfo[0] == 0: self.newOptionInfo[0] = None# if the value is 0, then it is not a valid value
            
            else:# if the value has been confirmed
                
                # result = drawClickableBox(screen, (1700, 415), f"${self.strikeNumPad.getValue()}", 55, (0,0,0), (160,160,160), mousebuttons,centerX=True,border=False)
                result = drawClickableBox(screen, (1875, 427), f"${self.strikeNumPad.getValue()}", 55, (200,200,200), (0,0,0), mousebuttons,centerY=True,border=False,topLeftX=True)
                self.newOptionInfo[0] = result if result else self.newOptionInfo[0]# Allows the user to change the value even if it has been confirmed
                

            # --------------------------------------- EXPIRATION DATE ----------------------------------
            dateTxt = s_render('Exp Date', 40, (200, 200, 200))
            # screen.blit(dateTxt, (1700-dateTxt.get_width()/2, 485))
            screen.blit(dateTxt, (1530, 537-dateTxt.get_height()/2))

            if self.newOptionInfo[1] == None:
                result = drawClickableBox(screen, (1875, 537), "Set Date", 45, (0,0,0), (170,170,170),mousebuttons,centerY=True,fill=True,topLeftX=True)
                if result:# if the box has been clicked to set the date (numpad displayed)
                    self.newOptionInfo[1] = True# changing it to true so that the numpad will be displayed
                    self.newOptionInfo[0] = None if self.newOptionInfo[0] == True else self.newOptionInfo[0]# if the box has been clicked for setting a value, but no value has been confirmed

                # if the box has been clicked for setting a date, but no value has been confirmed
            elif type(self.newOptionInfo[1]) == bool:# if the box has been clicked, but no value has been confirmed
                
                self.dateNumPad.draw(screen,(1050,190),(450,340),"Day",mousebuttons,365*3)# draw the numpad, max value of 3 years
                result = drawClickableBoxWH(screen, (1050, 510), (450,50),"Confirm Date", 45, (160,160,160), (0,0,0), mousebuttons,fill=True)
                if result:
                    self.newOptionInfo[1] = self.dateNumPad.getValue()
                daysValTxt = s_render(f"{self.dateNumPad.getNumstr('Day',upperCase=False)}", 55, (200, 200, 200))
                # screen.blit(daysValTxt, (1700-daysValTxt.get_width()/2, 520))
                screen.blit(daysValTxt, (1860-daysValTxt.get_width(), 500))
                timeOffset = gametime.time+timedelta(days=self.dateNumPad.getValue())
                dateValTxt = s_render(f"{timeOffset.strftime('%m/%d/%Y')}", 40, (175, 175, 175))
                # screen.blit(dateValTxt, (1700-dateValTxt.get_width()/2, 570))
                screen.blit(dateValTxt, (1860-dateValTxt.get_width(), 545))
                if self.newOptionInfo[1] == 0: self.newOptionInfo[1] = None
            else:# if the value has been confirmed
                # result = drawClickableBox(screen, (1700, 505), f"{self.dateNumPad.getNumstr('Day',upperCase=False)}", 55, (0,0,0), (160,160,160), mousebuttons,centerX=True,border=False)
                result = drawClickableBox(screen, (1885, 485), f"{self.dateNumPad.getNumstr('Day',upperCase=False)}", 55, (200,200,200), (0,0,0), mousebuttons,border=False,topLeftX=True)
                self.newOptionInfo[1] = result if result else self.newOptionInfo[1]
                timeOffset = gametime.time+timedelta(days=self.dateNumPad.getValue())
                dateValTxt = s_render(f"{timeOffset.strftime('%m/%d/%Y')}", 40, (120, 120, 120))
                # screen.blit(dateValTxt, (1700-dateValTxt.get_width()/2, 570))
                screen.blit(dateValTxt, (1860-dateValTxt.get_width(), 545))
                
            # --------------------------------------- ESTIMATED PRICE ----------------------------------
            priceTxt = s_render('Est Price', 40, (200, 200, 200))
            # screen.blit(priceTxt, (1700-priceTxt.get_width()/2, 615))
            screen.blit(priceTxt, (1530, 642-priceTxt.get_height()/2))
            
            saveResult = drawClickableBox(screen, (1515, 690), "Save", 45, (200,200,200), (0,225,0), mousebuttons)# draw the save button
            
            if self.newOptionInfo[0] != None and self.newOptionInfo[1] != None:
                if type(self.newOptionInfo[0]) != bool and type(self.newOptionInfo[1]) != bool and self.newOptionInfo[0] > 0:
                    timeOffset = (gametime.time+timedelta(days=self.dateNumPad.getValue()))
                    if self.newOptionObj == None:
                        self.newOptionObj = OptionAsset(self.player,stock,self.newOptionInfo[0],timeOffset,self.oTypeSelect.getSelected(),str(gametime),1)
                    else:
                        # print(f"Strike Price: {self.newOptionInfo[0]}, Expiration Date: {timeOffset}, Option Type: {self.oTypeSelect.getSelected()}")
                        self.newOptionObj.setValues(strikePrice=self.newOptionInfo[0],expirationDate=timeOffset,optionType=self.oTypeSelect.getSelected())
                    price = self.newOptionObj.getValue(bypass=True)
                    priceTxt = s_render(f"${limit_digits(price,15)}", 55, (200, 200, 200))
                    # print(self.newOptionObj.getStrike(),self.newOptionObj.getExpDate(),self.newOptionObj.getType(),self.newOptionObj.getValue())
                    screen.blit(priceTxt, (1860-priceTxt.get_width(), 620))
                    if saveResult:# if the save button has been clicked
                        self.savedOptions.append(self.newOptionObj)# save the new option
                        self.selectedOption = self.newOptionObj# select the new option
                        self.newOptionInfo,self.newOptionObj = None, None# reset the new option info
                        self.dateNumPad.reset(); self.strikeNumPad.reset()# reset the numpads
                else:# if the value has not been confirmed
                    notAppltxt = s_render(f"N/A", 55, (200, 200, 200))
                    screen.blit(notAppltxt, (1860-notAppltxt.get_width(), 620))

            cancelResult = drawClickableBox(screen, (1750, 690), "Cancel", 45, (200,200,200), (225,0,0), mousebuttons)# draw the cancel button
            if cancelResult:
                self.newOptionInfo = None
                self.newOptionObj = None

    def drawCustomOptions(self,screen:pygame.Surface,mousebuttons:int,gametime:GameTime,stock:Stock):

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1500,210,400,740),5,10)
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1500,210,400,50),5,10)

        avOptiontxt = s_render('Custom Options', 45, (255, 255, 255))
        screen.blit(avOptiontxt, (1700-avOptiontxt.get_width()/2, 220))
        self.customOptionLogic(screen,mousebuttons,gametime,stock)
        self.drawSavedCustomOptions(screen,mousebuttons,gametime,stock)

    def drawOptionInfo(self,screen:pygame.Surface, gametime, stock:Stock):
        """Draws the info underneath the stock graph for the selected option"""
        strings = ["Strike","Ex Date","Days Till Ex","Dividend","Volatility","Allocation"]
        getAllo = lambda price : (price/(self.player.getNetworth()+price))*100# gets the allocation of the option
        values = [
            f"${self.selectedOption.getStrike()}",
            f"{self.selectedOption.getExpDate()}",
            f"{self.selectedOption.daysToExpiration(gametime.time)}",
            f"{limit_digits(stock.dividend,12)}%",
            f"{limit_digits(stock.getVolatility()*100,12)}%",
            f"{limit_digits(getAllo(self.selectedOption.getValue()),12)}%"
        ]
        # info = {key:value for key,value in zip(keys,values)}
        info = [(string,value) for string,value in zip(strings,values)]
        drawLinedInfo(screen,(590,660),(435,330),info,35,TXTCOLOR)

    def drawSelectedOption(self,screen:pygame.Surface,mousebuttons:int,gametime:GameTime,stock:Stock):
        if self.selectedOption == None:
            return
        option = self.selectedOption
        stockNameTxt = s_render(f"{stock.name}", 85, stock.color)# renders the stock name
        screen.blit(stockNameTxt, (585, 565))

        optionTypeTxt = s_render(f"({option.getType().capitalize()})", 50, self.determineColor(option.getType()))# renders the option type
        screen.blit(optionTypeTxt, (595+stockNameTxt.get_width(), 565+stockNameTxt.get_height()/2-optionTypeTxt.get_height()/2))

        self.drawOptionInfo(screen,gametime,stock)# draws the info underneath the stock graph for the selected option
        maxQuant = int(self.player.cash//option.getValue(bypass=True,fullvalue=False))
        self.quantNumPad.draw(screen,(1050,190),(450,340),"Option",mousebuttons,maxQuant)# draw the numpad
        # self.selectedOption.setValues(quantity=self.quantNumPad.getValue())# set the quantity of the option

        quantTxt = s_render(f"{self.quantNumPad.getNumstr('Option')}", 65, (200, 200, 200))
        screen.blit(quantTxt, (1275-quantTxt.get_width()/2, 600))

        optionValTxt = s_render(f"x ${limit_digits(option.getValue(bypass=True,fullvalue=False),15)}", 55, (200, 200, 200))
        screen.blit(optionValTxt, (1180, 680))

        fee = 0 if self.selectedOption in self.preMadeOptions[stock] else 2
        feeTxt = s_render(f"x {fee}% fee", 55, (200, 200, 200))
        screen.blit(feeTxt, (1180, 740))

        # line inbetween 
        pygame.draw.rect(screen,(200,200,200),pygame.Rect(1130, 790, 300, 5))

        totalCost = self.selectedOption.getValue(bypass=True,fullvalue=False)*self.quantNumPad.getValue()*(1+fee/100)
        totalCostTxt = s_render(f"Total: ${limit_digits(totalCost,17)}", 65, (200, 200, 200))
        screen.blit(totalCostTxt, (1275-totalCostTxt.get_width()/2, 815))

        result = drawClickableBox(screen, (1275, 880), "Confirm Purchase", 55, (200,200,200), (0,225,0), mousebuttons,centerX=True)# draw the buy button
        if result:
            self.selectedOption.setValues(quantity=self.quantNumPad.getValue())# set the quantity of the option
            self.player.buyAsset(self.selectedOption)
            print(self.selectedOption.savingInputs())
            self.selectedOption = None
            self.quantNumPad.reset()




    def drawStockInfo(self,screen:pygame.Surface, gametime, stock:Stock):
        """Draws the info underneath the stock graph on the left"""
        if self.selectedOption != None:
            return
        if self.newOptionInfo == None or (self.newOptionInfo and type(self.newOptionInfo[0]) != bool) and (self.newOptionInfo and type(self.newOptionInfo[1]) != bool):
            strings = ["Open","High (1W)","Low (1W)","Dividend","Volatility"]
            g = gametime.time
            marketOpenTime = datetime.strptime(f"{g.month}/{g.day}/{g.year} 9:30:00 AM", "%m/%d/%Y %I:%M:%S %p")
            values = [
                f"${limit_digits(stock.getPointDate(marketOpenTime,gametime),12)}",
                f"${limit_digits(max(stock.graphs['1W']),12)}",
                f"${limit_digits(min(stock.graphs['1W']),12)}",
                f"{limit_digits(stock.dividend,12)}%",
                f"{limit_digits(stock.getVolatility()*100,12)}%"
            ]
            # info = {key:value for key,value in zip(keys,values)}
            info = [(string,value) for string,value in zip(strings,values)]
            drawLinedInfo(screen,(1055,220),(435,370),info,40,TXTCOLOR)

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player,gametime):
        
        # print(self.savedOptions,self.selectedOption)
        # screen.blit(s_render('Select a Stock', 36, (255, 255, 255)), (220, 110))
        if self.stockSelection.draw(screen, [stock.name for stock in stocklist], [200, 105], [1700, 50], colors=[stock.color for stock in stocklist],txtsize=35):
            self.newOptionInfo = None
            self.newOptionObj = None
            self.selectedOption = None

        stock = self.findStockObj(self.stockSelection.getSelected())
        self.stockGraph.setStockObj(stock)
        self.stockGraph.drawFull(screen, (585,210),(460,350),"OptionMenu Graph",True,"Normal")
        # if self.newOptionInfo == None or (self.newOptionInfo and type(self.newOptionInfo[0]) != bool) and (self.newOptionInfo and type(self.newOptionInfo[1]) != bool):
        self.drawStockInfo(screen,gametime,stock)
        self.drawAvailableOptions(screen,mousebuttons,gametime,stock)
        self.drawCustomOptions(screen,mousebuttons,gametime,stock)
        self.drawSelectedOption(screen,mousebuttons,gametime,stock)


        


        
        

