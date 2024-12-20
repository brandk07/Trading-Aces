from Classes.Menus.OptionScreens.ExerciseScreen import *
from Classes.imports.UIElements.Latterscroll import CustomColorLatter
from Classes.imports.Gametime import GameTime

class SellOptionScreen:
    def __init__(self,stocklist,gametime,player,screenSelection,optionTrade) -> None:
        self.player = player
        self.stocklist:list = stocklist
        self.gametime = gametime
        self.ownedScroll = CustomColorLatter()
        self.selectedGraph : StockVisualizer = StockVisualizer(gametime,stocklist[0],stocklist)
        self.netWorthGraph : StockVisualizer = StockVisualizer(gametime,player,stocklist)
        self.selectOption = None
        self.optionTrade = optionTrade# stores the Parent option trade object
        self.sortby = "Expiration"
        self.numpad = Numpad(displayText=False)
        self.screenSelection : SelectionBar = screenSelection# stores the screen selection object from the main game screen
        self.exerciseMenu : ExerciseOptionScreen = ExerciseOptionScreen(stocklist,gametime,player)
        self.orderBox = OrderBox((1030,615),(385,345),gametime)
        
        self.determineColor = lambda optionType: (127,25,255) if optionType == "put" else (50, 180, 169)# determines the color of the asset
    def setSelectOption(self,option:OptionAsset):
        self.selectOption = option

    def drawOptionInfo(self,screen:pygame.Surface, gametime):
        option = self.selectOption

        drawCenterTxt(screen, option.stockObj.name, 120, option.stockObj.color, (895, 110),centerX=False, centerY=False,fullX=True)
        drawCenterTxt(screen, option.getType().capitalize(), 120, self.determineColor(option.getType()), (910, 110),centerX=False, centerY=False)
        
        
        # EXPIRATION INFO
        drawCenterTxt(screen, 'Expiration Info', 50, (0, 0, 0), (1340, 220), centerY=False)
        # line under the title
        pygame.draw.line(screen, (0, 0, 0), (1165, 270), (1165+350, 270), 5)

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
        drawLinedInfo(screen,(1155,270),(370,360),info,37,TXTCOLOR)
        

        # Other Info
        drawCenterTxt(screen, 'Other Info', 50, (0, 0, 0), (1720, 220), centerY=False)

        pygame.draw.line(screen, (0, 0, 0), (1545, 270), (1545+350, 270), 5)

        strings = ["Strike","Type","Dividend","Volatility"]
        values = [
            f"${option.getStrike()}",
            f"{option.optionType}",
            f"{limit_digits(option.stockObj.dividendYield,12)}%",
            f"{limit_digits(option.stockObj.getVolatility()*100,12)}%"
        ]
        info = [(string,value) for string,value in zip(strings,values)]
        drawLinedInfo(screen,(1535,270),(370,360),info,37,TXTCOLOR)

    def drawOwnedOptions(self,screen:pygame.Surface):

        strike = drawClickableBoxWH(screen, (210, 910), (220,50), "Value", 45, (0,0,0), (200,200,200),fill=True)
        exp = drawClickableBoxWH(screen, (455, 910), (220,50),"Expiration", 45, (0,0,0), (200,200,200),fill=True)
        self.sortby = "Value" if strike else self.sortby
        self.sortby = "Expiration" if exp else self.sortby

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(200,210,465,665),5,10)# draws the box around the latter scroll
        drawCenterTxt(screen, 'Owned Options', 45, (180, 180, 180), (432, 220), centerY=False)


        # DRAWING THE LATTER SCROLL
        optionList = self.player.getOptions()
        if len(optionList) == 0:
            drawCenterTxt(screen, 'No Owned Options', 45, (200, 200, 200), (432, 390), centerY=False)
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

        # newselected = self.ownedScroll.draw_polys(screen, (205, 270), (370,950), selectedindex, True, *[self.determineColor(option.getType()) for option in optionList[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        newselected = self.ownedScroll.draw_polys(screen, (205, 270), (455,875), selectedindex, True, *[brightenCol(self.determineColor(option.getType()),0.25) for option in optionList[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset

        if select == None:# if the latterscroll didn't contain the selected asset before
            self.selectOption = self.selectOption if newselected == None else optionList[newselected]# Changes selected stock if the new selected has something
        else:# if the latterscroll contained the selected asset before, then it can set it to none if you select it again
            self.selectOption = None if newselected == None else optionList[newselected]

        drawCenterTxt(screen, f"{ommitted[0]} - {ommitted[1]-1} out of {len(optionList)} Options", 35, (0, 0, 0), (432, 875), centerY=False)
    
    def drawExerciseAndOther(self,screen,gametime):
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(670, 620, 1230, 270),5,10)# box around the entire bottom

        drawCenterTxt(screen, 'Go to Exercise Screen', 55, (0, 0, 0), (865, 770), centerY=False, fullY=True)
        result = drawClickableBoxWH(screen, (685, 780), (360,95), "Exercise Screen", 55, (0,0,0), (200,200,200),fill=True)
        if result:
            self.exerciseMenu.setSelected(self.selectOption)

        drawCenterTxt(screen, 'See in Portfolio', 55, (0, 0, 0), (1235, 770), centerY=False, fullY=True)
        result = drawClickableBoxWH(screen, (1055, 780), (360,95), "Portfolio", 55, (0,0,0), (200,200,200),fill=True)
        if result:
            self.player.screenManager.setScreen("Portfolio")
            self.player.screenManager.screens["Portfolio"].setSelectedAsset(self.selectOption)
            # self.optionTrade.menudrawn = False
            # portfolio = self.player.menuList[1]
            # portfolio.menudrawn = True
            # portfolio.setSelectedAsset(self.selectOption)

        stock = self.selectOption.stockObj
        
        # drawCenterTxt(screen, stock.name, 90, stock.color, (210, 635), centerY=False)# blits the stock name to the screen
        drawCenterTxt(screen, stock.name, 90, stock.color, (680, 630), centerX=False, centerY=False)# blits the stock name to the screen
        
        drawCenterTxt(screen, FSTOCKNAMEDICT[stock.name], 45, (180, 180, 180), (812, 660), centerX=False)

        drawCenterTxt(screen, 'Report Info', 65, (0, 0, 0), (1657, 695), centerY=False, fullY=True)

        daysTillNextR = stock.priceEffects.daysTillNextReport(gametime)
        data = [("Quarterly Report In",f"{daysTillNextR} Day{'s' if daysTillNextR != 1 else ''}"),(f"Report Outlook",f"{round(stock.priceEffects.getQuarterlyLikelyhood(gametime),2)}%")]
        drawLinedInfo(screen,(1425,705),(460,170),data,37,TXTCOLOR)
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1425,705,465,170),5,10)

        

    def drawScreen(self,screen,gametime:GameTime):
        
        if self.exerciseMenu.drawn():# if the exercise menu is drawn
            self.exerciseMenu.drawScreen(screen)
        else:# if the exercise menu is not drawn
            if self.selectOption != None and self.selectOption not in self.player.getOptions():
                self.selectOption = None


            if self.selectOption == None:
                pygame.draw.rect(screen,(0,0,0),pygame.Rect(670, 210, 675, 550),5,10)# box around the select an option
                drawCenterTxt(screen, 'Select An Option', 80, (180, 180, 180), (1005, 225), centerY=False)
                self.netWorthGraph.drawFull(screen, (1350,210),(550,550),"SellNetWorth",True,"Normal")

            self.drawOwnedOptions(screen)
            
            if self.selectOption != None:
                self.drawOptionInfo(screen,self.gametime)
                self.drawExerciseAndOther(screen,gametime)
                self.selectedGraph.setStockObj(self.selectOption.stockObj)
                self.selectedGraph.drawFull(screen, (670,210),(465,405),"SellSelected",True,"Normal")