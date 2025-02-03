from Classes.Menus.OptionScreens.SellScreen import *
from Classes.BigClasses.Stock import Stock
from Classes.AssetTypes.OptionAsset import OptionAsset,getCloseOpenDate

class CustomOptionCreator:
    def __init__(self,player,optionObj) -> None:
        # self.newOptionInfo = None# list containing info for the new option that is being created, [strikePrice, expirationDate]
        self.strikePrice,self.expDate = None,None
        self.creatingOption = False
        self.player = player
        self.optionObj = optionObj
        self.strikePad : Numpad = Numpad(displayText=False,nums=('DEL','0','.'))
        self.datePad : Numpad = Numpad(displayText=False,nums=('DEL','0','MAX'))
        self.oTypeSelect : SelectionBar = SelectionBar()
        self.cucOptionScrll = CustomColorLatter()
        self.numPadDisplay = None# Strike, or 
        self.selectOption = None
        self.newOptionObj = None
        self.savedOptions : list[OptionAsset] = []# stores the saved options OptionAsset objects
        self.determineColor = lambda optionType: (127,25,255) if optionType == "put" else (50, 180, 169)# determines the color of the asset
    def removeSelc(self):
        self.selectOption = None
    def stopCreating(self):
        self.creatingOption = False
    def loadSavedOptions(self,optionList:list[OptionAsset]):
        self.savedOptions = optionList
    def drawType(self,screen,):
        drawCenterTxt(screen, 'Type', 45, (200, 200, 200), (1700, 275), centerY=False)
        
        self.oTypeSelect.draw(screen, ["call","put"], (1575, 315), (250, 50), colors=[(50, 180, 169),(127,25,255)],txtsize=35)
    
    def drawStrike(self,screen,stock:Stock):
        drawCenterTxt(screen, 'Strike', 45, (180, 180, 180), (1530, 427), centerX=False)

        if self.strikePrice == None and self.numPadDisplay != "Strike":# if the strike price has not been set
            result = drawClickableBox(screen, (1875, 427), "Set Value", 45, (0,0,0), (160,160,160),centerY=True,fill=True,topLeftX=True)
            if result:# if the box has been clicked to set the value (numpad displayed)
                self.numPadDisplay = "Strike"# changing it to strike so that the numpad will be displayed
        
        elif self.numPadDisplay == "Strike" and self.strikePrice == None:# if the box has been clicked, but no value has been confirmed
            self.strikePad.draw(screen,(1050,190),(450,340),"",stock.price*2)# draw the numpad
            result = drawClickableBoxWH(screen, (1050, 510), (450,50),"Confirm Strike Value", 45, (160,160,160), (0,0,0),fill=True)

            self.strikePrice = self.strikePad.getValue() if result else self.strikePrice
            self.numPadDisplay = None if result else self.numPadDisplay
            drawCenterTxt(screen, f"${self.strikePad.getNumstr(haveSes=False)}", 55, (200, 200, 200), (1850, 428),centerX=False,fullX=True)

            if self.strikePrice == 0: self.strikePrice = None# if the value is 0, then it is not a valid value
        
        else:# if the value has been confirmed
            
            result = drawClickableBox(screen, (1862, 428), f"${self.strikePad.getValue()}", 55, (200,200,200), (0,0,0),centerY=True,border=False,topLeftX=True)
            if result: 
                self.numPadDisplay = "Strike"; self.strikePrice = None

    def drawDate(self,screen,gametime:GameTime):
        dateTxt = s_render('Exp Date', 40, (200, 200, 200))
        screen.blit(dateTxt, (1530, 537-dateTxt.get_height()/2))
        # print(self.expDate)
        if self.expDate == None and self.numPadDisplay != "Date":
            result = drawClickableBox(screen, (1875, 537), "Set Date", 45, (0,0,0), (170,170,170),centerY=True,fill=True,topLeftX=True)
            if result:# if the box has been clicked to set the date (numpad displayed)
                self.numPadDisplay = "Date"# changing it to date so that the numpad will be displayed

        elif self.numPadDisplay == "Date" and self.expDate == None:# if the box has been clicked, but no value has been confirmed
            
            self.datePad.draw(screen,(1050,190),(450,340),"Day",365*3)# draw the numpad, max value of 3 years
            result = drawClickableBoxWH(screen, (1050, 510), (450,50),"Confirm Date", 45, (160,160,160), (0,0,0),fill=True)

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
            result = drawClickableBox(screen, (1885, 485), f"{self.datePad.getNumstr('Day',upperCase=False)}", 55, (200,200,200), (0,0,0),border=False,topLeftX=True)
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

    def drawCustOptions(self,screen:pygame.Surface,gametime:GameTime,stock:Stock):
        """Handles the logic for creating a custom option"""

        
        if not self.creatingOption:# if there is no new option being created (display the create new option button)

            result = drawClickableBox(screen, (1700, 270), "+ Create New", 50, (200,200,200), (0,80,0),centerX=True,fill=True)
            if result:
                self.creatingOption = True; self.selectOption = None; self.optionObj.removeSelc()
                
        else:# if there is a new option being created
            self.selectOption = None
            coords = [(265,110),(380,95),(480,115),(600,85)]# stores the y and height of the boxes [Type, strike, exp date, est price]
            for i,coord in enumerate(coords):
                pygame.draw.rect(screen,(0,0,0),pygame.Rect(1510,coord[0],375,coord[1]),5,10)

            self.drawType(screen,)# Draws, and handles the logic for setting the option type

            self.drawStrike(screen,stock)# Draws, and handles the logic for setting the strike price
            
            self.drawDate(screen,gametime)# Draws, and handles the logic for setting the expiration date
            
            saveResult = drawClickableBox(screen, (1515, 690), "Save", 45, (200,200,200), (0,225,0))# draw the save button

            self.drawEstPrice(screen,saveResult,gametime,stock)# Draws, and handles the logic for setting the estimated price

            cancelResult = drawClickableBox(screen, (1750, 690), "Cancel", 45, (200,200,200), (225,0,0))# draw the cancel button
            if cancelResult:
                self.strikePrice,self.expDate = None,None
                self.newOptionObj = None
                self.creatingOption = False
        return self.savedOptions

    def drawSavedOptions(self,screen:pygame.Surface,gametime:GameTime,stock:Stock):
 
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
        get_text = lambda option : [f'${limit_digits(option.getValue(bypass=True),18)} ',f'{option.getType().capitalize()}',f'{daysLeft(option)}']# returns the text for the stock
        textlist = [get_text(option) for option in optionList]# stores 3 texts for each asset in the stocks list

        textinfo = []# stores the text info for the latter scroll [text,fontsize,color]
        coords = [[(20,15)] for i in range(len(textlist))]

        for i,(text,option) in enumerate(zip(textlist,optionList)):# loop through the textlist and store the text info in the textinfo list
           
            polytexts = []# temporary list to store the text info for each asset
            polytexts.extend([[text[0],43,(210,210,210)],[text[1],40,self.determineColor(option.getType())],[text[2],40,(190,190,190)]])# appends the text info for the asset            
            textinfo.append(polytexts)
            coords[i].append((160,55))
            coords[i].append((210,55))

        self.cucOptionScrll.storetextinfo(textinfo); self.cucOptionScrll.set_textcoords(coords)# stores the text info and the coords for the latter scroll

        ommitted = self.cucOptionScrll.store_rendercoords((x, y), (w,y+h),120,0,0)
        select = self.selectOption if self.selectOption in optionList else None# Ensuring that the selected stock is in the optionlist
        selectedindex = None if select == None else optionList.index(select)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)
        
        newselected = self.cucOptionScrll.draw_polys(screen, (x, y), (w, y+h),selectedindex, True, *[self.determineColor(option.getType()) for option in optionList[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        
        if newselected != None: self.creatingOption = False
        if select == None:# if the latterscroll didn't contain the selected asset before
            self.selectOption = self.selectOption if newselected == None else optionList[newselected]
        else:# if the latterscroll contained the selected asset before, then it can set it to none if you select it again
            self.selectOption = None if newselected == None else optionList[newselected]

        # self.selectOption = self.selectOption if newselected == None else optionList[newselected]# Changes selected stock if the new selected has something
        txt = s_render(f"{ommitted[0]} - {ommitted[1]-1} out of {len(optionList)} Options",35,(0,0,0))
        screen.blit(txt,(1700-txt.get_width()/2,950))
        return self.selectOption