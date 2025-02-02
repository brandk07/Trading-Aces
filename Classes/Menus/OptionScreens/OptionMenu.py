from Classes.Menus.OptionScreens.CustomOptionCreator import *
from Classes.Menus.Menu import Menu
from Classes.imports.UIElements.SelectionElements import SelectionBar,MenuSelection
from datetime import timedelta,datetime

class Optiontrade(Menu):
    def __init__(self,stocklist:list,gametime,player,currentRun):
        super().__init__(currentRun)
        self.player = player
        self.stocklist = stocklist
        self.gametime = gametime
        self.preMadeOptions = {}
        self.menudrawn = False
        
        self.stockGraph : StockVisualizer = StockVisualizer(gametime,stocklist[0],stocklist)
        self.stockSelection : SelectionBar = SelectionBar()
        self.screenSelection : MenuSelection = MenuSelection((200, 105), (375, 100),["Buy","Owned"],45,colors=[(100,200,100),(200,100,100)])
        self.screenSelection.setSelected("Buy")

        self.orderBox = OrderBox((1040,570),(450,370),gametime)

        self.customOptionSc = CustomOptionCreator(player,self)    
        self.sellingScreen = SellOptionScreen(stocklist,gametime,player,self.screenSelection,self)    
        
        self.quantNumPad : Numpad = Numpad(displayText=False,nums=('DEL','0','MAX'))
        stocknames = [stock.name for stock in stocklist]
        self.findStockObj = lambda name: stocklist[stocknames.index(name)] 
        self.avaOptionScrll = CustomColorLatter()
    
        self.savedOptions = []# stores the saved options OptionAsset objects
        self.selectOption = None
        self.determineColor = lambda optionType: (127,25,255) if optionType == "put" else (50, 180, 169)# determines the color of the asset
        # if self.preMadeOptions == {}:
        self.fillPreMadeOptions()
    def removeSelc(self):
        self.selectOption = None

    def setSelectedAsset(self,option):
        """Sets the selected asset to the given option, takes to Owned screen"""

        self.customOptionSc.stopCreating()
        self.screenSelection.setSelected("Owned")
        self.sellingScreen.setSelectOption(option)

    def forceExerciseOption(self,option):
        """Sets the selected asset to the given option, takes to Owned screen"""
        self.screenSelection.setSelected("Owned")
        self.sellingScreen.setSelectOption(option)
        self.sellingScreen.exerciseMenu.setSelected(option,forced=True)
    def isForced(self):
        """Returns if the exercise menu is forced"""
        return self.sellingScreen.exerciseMenu.forced
    
    def savingData(self):
        """Saves the inputs for the option menu"""
        allData = [{},[]]# premade, saved
        for stock,options in self.preMadeOptions.items():
            allData[0][stock.name] = []
            for option in options:
                allData[0][stock.name].append(option.savingInputs())
        for option in self.savedOptions:
            allData[1].append(option.savingInputs())
        return allData
    def loadingData(self,data,stockdict):
        """Loads the inputs for the option menu"""

        for stock in stockdict.values():
            self.preMadeOptions[stock] = [OptionAsset(self.player,stockdict[optData[0]],optData[1],optData[2],optData[3],optData[4],optData[5],porfolioPercent=optData[6],ogValue=optData[7],color=tuple(optData[8])) for optData in data[0][stock.name]]
            
        for optData in data[1]:
            self.savedOptions.append(OptionAsset(self.player,stockdict[optData[0]],optData[1],optData[2],optData[3],optData[4],optData[5],porfolioPercent=optData[6],ogValue=optData[7],color=tuple(optData[8])))
        self.customOptionSc.loadSavedOptions(self.savedOptions)

    def createRandomOption(self,stock:Stock):
        def getRandomDate(gametime):
            extime = str(gametime.time+timedelta(days=random.randint(3,400)))
            while gametime.isOpen(datetime.strptime(extime, "%Y-%m-%d %H:%M:%S")) == False:#  Makes sure the expiration date is a trading day
                extime = str(gametime.time+timedelta(days=random.randint(3,400)))
            return extime
        optionType = random.choice(['call','put'])
        strikeprice = random.randint(max(1,math.floor(stock.price-30)*100),min(math.ceil(stock.price*1.05)*100,math.ceil(stock.price+30)*100))/100
        extime = getRandomDate(self.gametime)
        oObj = OptionAsset(self.player,stock,strikeprice,extime,optionType,str(self.gametime),1)
        return oObj

    def fillPreMadeOptions(self):        
        for stock in self.stocklist:
            self.preMadeOptions[stock] = []
            for _ in range(8):
                self.preMadeOptions[stock].append(self.createRandomOption(stock))

    def drawAvailableOptions(self,screen:pygame.Surface,gametime:GameTime,stock:Stock):
        
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
            polytexts.extend([[text[1],55,self.determineColor(option.getType())],[text[0],40,(170,170,170)],[text[2],70,(190,190,190)]])# appends the text info for the asset            
            textinfo.append(polytexts)
            coords[i].append((140,25))
            # coords[i].append(((text[1],155),60))

        self.avaOptionScrll.storetextinfo(textinfo); self.avaOptionScrll.set_textcoords(coords)# stores the text info and the coords for the latter scroll
        ommitted = self.avaOptionScrll.store_rendercoords((205, 270), (370,950),135,0,0,updatefreq=60)
    
        select = self.selectOption if self.selectOption in optionList else None# Ensuring that the selected stock is in the optionlist
        selectedindex = None if select == None else optionList.index(select)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)

        # newselected = self.avaOptionScrll.draw_polys(screen, (205, 270), (370,950), , selectedindex, True, *[self.determineColor(option.getType()) for option in optionList[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        newselected = self.avaOptionScrll.draw_polys(screen, (205, 270), (370,950),selectedindex, True, *[brightenCol(self.determineColor(option.getType()),0.25) for option in optionList[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        if newselected != None: self.customOptionSc.stopCreating()

        if select == None:# if the latterscroll didn't contain the selected asset before
            self.selectOption = self.selectOption if newselected == None else optionList[newselected]# Changes selected stock if the new selected has something
        else:# if the latterscroll contained the selected asset before, then it can set it to none if you select it again
            self.selectOption = None if newselected == None else optionList[newselected]

        if self.selectOption != None and self.selectOption not in self.savedOptions:
            self.customOptionSc.removeSelc()
        txt = s_render(f"{ommitted[0]} - {ommitted[1]-1} out of {len(optionList)} Options",35,(0,0,0))
        screen.blit(txt,(390-txt.get_width()/2,950))


    def drawCustomOptions(self,screen:pygame.Surface,gametime:GameTime,stock:Stock):

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1500,210,400,740),5,10)
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1500,210,400,50),5,10)

        drawCenterTxt(screen, 'Custom Options', 45, (200, 200, 200), (1700, 220), centerY=False)

        self.savedOptions = self.customOptionSc.drawCustOptions(screen,gametime,stock)

        changeIt = False# only should be changed if the result is not none
        if self.selectOption != None and self.selectOption in self.savedOptions: 
            changeIt = True# if the selectOption is in this list then it should be changed
        result = self.customOptionSc.drawSavedOptions(screen,gametime,stock)
        if changeIt:
            self.selectOption = result
        else: 
            self.selectOption = self.selectOption if result == None else result


    def drawOptionInfo(self,screen:pygame.Surface, gametime, stock:Stock):
        """Draws the info underneath the stock graph for the selected option"""
        strings = ["Strike","Ex Date","Days Till Ex","Dividend","Volatility","Allocation"]
        getAllo = lambda price : (price/(self.player.getNetworth()+price))*100# gets the allocation of the option
        values = [
            f"${limit_digits(self.selectOption.getStrike(),24)}",
            f"{self.selectOption.getExpDate()}",
            f"{self.selectOption.daysToExpiration()}",
            f"{limit_digits(stock.dividendYield,12)}%",
            f"{limit_digits(stock.getVolatility()*100,12)}%",
            f"{limit_digits(getAllo(self.selectOption.getValue()),17)}%"
        ]
        # info = {key:value for key,value in zip(keys,values)}
        info = [(string,value) for string,value in zip(strings,values)]
        drawLinedInfo(screen,(590,620),(435,330),info,35,TXTCOLOR)

    def drawselectOption(self,screen:pygame.Surface,gametime:GameTime,stock:Stock):
        if self.selectOption == None:
            return
        option = self.selectOption
        stockNameTxt = s_render(f"{stock.name}", 85, stock.color)# renders the stock name
        screen.blit(stockNameTxt, (585, 565))

        optionTypeTxt = s_render(f"({option.getType().capitalize()})", 50, self.determineColor(option.getType()))# renders the option type
        screen.blit(optionTypeTxt, (595+stockNameTxt.get_width(), 565+stockNameTxt.get_height()/2-optionTypeTxt.get_height()/2))

        self.drawOptionInfo(screen,gametime,stock)# draws the info underneath the stock graph for the selected option
        # print(self.player.cash,option.getValue(bypass=True,fullvalue=False))
        if option.getValue(bypass=True,fullvalue=False) > 0.1:
            maxQuant = int(self.player.cash//option.getValue(bypass=True,fullvalue=False))
            self.quantNumPad.draw(screen,(1050,190),(450,340),"Option",maxQuant)# draw the numpad
        else:
            drawCenterTxt(screen, "Option Value Too Low", 50, (210, 50, 50), (1275, 280), centerY=False)
        

        fee = 0 if self.selectOption in self.preMadeOptions[stock] else 2 


        totalCost = self.selectOption.getValue(bypass=True,fullvalue=False)*self.quantNumPad.getValue()*(1+fee/100)
        feeCost = self.selectOption.getValue(bypass=True,fullvalue=False)*self.quantNumPad.getValue()*(fee/100)
        # drawCenterTxt(screen, f"Total: ${limit_digits(totalCost,17)}", 65, (200, 200, 200), (1275, 815), centerY=False)
        data = [("Value",f"${limit_digits(option.getValue(bypass=True,fullvalue=False),15)}","x"),(f"{fee}% Fee", f"${limit_digits(feeCost,22)}","-")]
        self.orderBox.loadData(self.quantNumPad.getNumstr('Option'),f"${limit_digits(totalCost,22)}",data)
        result = self.orderBox.draw(screen)

        # result = drawClickableBox(screen, (1275, 880), "Confirm Purchase", 55, (200,200,200), (0,225,0) if self.quantNumPad.getValue() > 0 else (0,0,0), ,centerX=True)# draw the buy button
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
            if not option.optionLive() or option.getValue() < 0.1:# if the option is not live or the value is too low
                self.savedOptions.remove(option)
        for key,options in self.preMadeOptions.items():
            for i in range(len(options)):
                if not options[i].optionLive() or options[i].getValue() < 0.1:# if the option is not live or the value is too low
                    self.preMadeOptions[key][i] = self.createRandomOption(key)# create a new random option
        if self.selectOption != None and not self.selectOption.optionLive():
            self.selectOption = None
            
    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, player,gametime):
        
        # if not (self.screenSelection.getSelected() == "Owned" and self.isForced()):# don't draw menu switcher if the exercise menu is forced
        self.screenSelection.draw(screen,)
        if self.screenSelection.getSelected() == "Buy":
            self.checkOptionDates()# Ensures that the options are still live

            if self.stockSelection.draw(screen, [stock.name for stock in stocklist], [585, 105], [1325, 65], colors=[stock.color for stock in stocklist],txtsize=35):
                self.newOptionInfo = None
                self.newOptionObj = None
                self.selectOption = None

            stock = self.findStockObj(self.stockSelection.getSelected())
            self.stockGraph.setStockObj(stock)
            self.stockGraph.drawFull(screen, (585,210),(460,350),"OptionMenu Graph",True,"Normal",)
            # if self.newOptionInfo == None or (self.newOptionInfo and type(self.strikePrice) != bool) and (self.newOptionInfo and type(self.newOptionInfo[1]) != bool):
            self.drawStockInfo(screen,gametime,stock)
            self.drawAvailableOptions(screen,gametime,stock)
            self.drawCustomOptions(screen,gametime,stock)
            self.drawselectOption(screen,gametime,stock)
        elif self.screenSelection.getSelected() == "Owned":
            self.sellingScreen.drawScreen(screen,gametime)


        


        
        

