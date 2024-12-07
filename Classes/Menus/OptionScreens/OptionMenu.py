from Classes.Menus.OptionScreens.SellScreen import *
from Classes.Menus.Menu import Menu
from Classes.AssetTypes.OptionAsset import OptionAsset,getCloseOpenDate
from Classes.BigClasses.Stock import Stock
from Classes.imports.UIElements.SelectionElements import SelectionBar,MenuSelection
from datetime import timedelta,datetime


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


class Optiontrade(Menu):
    def __init__(self,stocklist:list,gametime,player):
        # self.icon = pygame.image.load(r'Assets\Portfolio\portfolio2.png').convert_alpha()

        self.icon = pygame.image.load(r'Assets\Menu_Icons\noblack_option3.png').convert_alpha()
        self.icon = pygame.transform.smoothscale(self.icon, (140, 100))
        super().__init__(self.icon)
        self.player = player
        self.stocklist = stocklist
        self.gametime = gametime
        self.preMadeOptions = {}
        self.menudrawn = False
        self.fillPreMadeOptions()
        self.stockGraph : StockVisualizer = StockVisualizer(gametime,stocklist[0],stocklist)
        self.stockSelection : SelectionBar = SelectionBar()
        self.screenSelection : MenuSelection = MenuSelection((200, 105), (375, 100),["Buy","Sell"],45,colors=[(100,200,100),(200,100,100)])
        self.screenSelection.setSelected("Buy")

        self.orderBox = OrderBox((1040,570),(450,370))

        self.customOptionSc = CustomOptionCreator(player,self)    
        self.sellingScreen = SellOptionScreen(stocklist,gametime,player,self.screenSelection,self)    
        
        self.quantNumPad : Numpad = Numpad(displayText=False,nums=('DEL','0','MAX'))
        stocknames = [stock.name for stock in stocklist]
        self.findStockObj = lambda name: stocklist[stocknames.index(name)] 
        self.avaOptionScrll = CustomColorLatter()
    
        self.savedOptions = []# stores the saved options OptionAsset objects
        self.selectOption = None
        self.determineColor = lambda optionType: (127,25,255) if optionType == "put" else (50, 180, 169)# determines the color of the asset

    def removeSelc(self):
        self.selectOption = None

    def setSelectedAsset(self,option):
        """Sets the selected asset to the given option, takes to Sell screen"""

        self.customOptionSc.stopCreating()
        self.screenSelection.setSelected("Sell")
        self.sellingScreen.setSelectOption(option)

    def forceExerciseOption(self,option):
        """Sets the selected asset to the given option, takes to Sell screen"""
        self.screenSelection.setSelected("Sell")
        self.sellingScreen.setSelectOption(option)
        self.sellingScreen.exerciseMenu.setSelected(option,forced=True)
    def isForced(self):
        """Returns if the exercise menu is forced"""
        return self.sellingScreen.exerciseMenu.forced

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
        daysLeft = lambda option: f'{int(option.daysToExpiration())} Day{"s" if option.daysToExpiration() > 1 else ""}'
        get_text = lambda option : [f'{daysLeft(option)}',f'{option.getType().capitalize()}',f'${limit_digits(option.getValue(fullvalue=False),15,option.getValue(fullvalue=False)>100)} ']# returns the text for the stock
        textlist = [get_text(option) for option in optionList]# stores 3 texts for each asset in the stocks list

        textinfo = []# stores the text info for the latter scroll [text,fontsize,color]
        coords = [[(15,10),(20,62)] for i in range(len(textlist))]

        for i,(text,option) in enumerate(zip(textlist,optionList)):# loop through the textlist and store the text info in the textinfo list
            if self.selectOption == option:
                option.getValue(bypass=True)

            polytexts = []# temporary list to store the text info for each asset
            polytexts.extend([[text[1],55,self.determineColor(option.getType())],[text[0],40,(170,170,170)],[text[2],80,(190,190,190)]])# appends the text info for the asset            
            textinfo.append(polytexts)
            coords[i].append((150,22))
            # coords[i].append(((text[1],155),60))

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
            f"{limit_digits(stock.dividendYield,12)}%",
            f"{limit_digits(stock.getVolatility()*100,12)}%",
            f"{limit_digits(getAllo(self.selectOption.getValue()),12)}%"
        ]
        # info = {key:value for key,value in zip(keys,values)}
        info = [(string,value) for string,value in zip(strings,values)]
        drawLinedInfo(screen,(590,620),(435,330),info,35,TXTCOLOR)

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

        fee = 0 if self.selectOption in self.preMadeOptions[stock] else 2 


        totalCost = self.selectOption.getValue(bypass=True,fullvalue=False)*self.quantNumPad.getValue()*(1+fee/100)
        feeCost = self.selectOption.getValue(bypass=True,fullvalue=False)*self.quantNumPad.getValue()*(fee/100)
        # drawCenterTxt(screen, f"Total: ${limit_digits(totalCost,17)}", 65, (200, 200, 200), (1275, 815), centerY=False)
        data = [("Value",f"${limit_digits(option.getValue(bypass=True,fullvalue=False),15)}","x"),(f"{fee}% Fee", f"${limit_digits(feeCost,22)}","-")]
        self.orderBox.loadData(self.quantNumPad.getNumstr('Option'),f"${limit_digits(totalCost,22)}",data)
        result = self.orderBox.draw(screen,mousebuttons)

        # result = drawClickableBox(screen, (1275, 880), "Confirm Purchase", 55, (200,200,200), (0,225,0) if self.quantNumPad.getValue() > 0 else (0,0,0), mousebuttons,centerX=True)# draw the buy button
        if result and self.quantNumPad.getValue() > 0:
            self.selectOption.setValues(quantity=self.quantNumPad.getValue(),creationDate=gametime.time)# set the quantity of the option
            # print(self.quantNumPad.getValue(),"is the selected quantity")
            self.player.buyAsset(self.selectOption)
            # print(self.selectOption.savingInputs())
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
                f"{limit_digits(stock.dividendYield,12)}%",
                f"{limit_digits(stock.getVolatility()*100,12)}%"
            ]
            # info = {key:value for key,value in zip(keys,values)}
            info = [(string,value) for string,value in zip(strings,values)]
            drawLinedInfo(screen,(1055,200),(435,370),info,40,TXTCOLOR)
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
        if not (self.screenSelection.getSelected() == "Sell" and self.isForced()):# don't draw menu switcher if the exercise menu is forced
            self.screenSelection.draw(screen,mousebuttons)
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
            self.sellingScreen.drawScreen(screen,mousebuttons,gametime)


        


        
        

