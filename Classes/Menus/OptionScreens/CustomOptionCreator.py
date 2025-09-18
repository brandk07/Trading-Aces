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
        self.oTypeSelect : SelectionBar = SelectionBar()
        self.cucOptionScrll = CustomColorLatter()
        self.selectOption = None
        self.newOptionObj = None
        self.savedOptions : list[OptionAsset] = []# stores the saved options OptionAsset objects
        self.determineColor = lambda optionType: (127,25,255) if optionType == "put" else (50, 180, 169)# determines the color of the asset
        
        # Initialize simple keyboard input state
        self.strike_input_text = ""
        self.date_input_text = ""
        self.last_key_time = 0
        self.key_repeat_delay = 0.5  # Initial delay
        self.key_repeat_interval = 0.05  # Repeat interval
        self.inputMode = None  # "strike_keyboard", "date_keyboard", or None
    def removeSelc(self):
        self.selectOption = None
    def stopCreating(self):
        self.creatingOption = False
        self.inputMode = None
        self.strike_input_text = ""
        self.date_input_text = ""
    def loadSavedOptions(self,optionList:list[OptionAsset]):
        self.savedOptions = optionList
    def drawType(self,screen,):
        drawCenterTxt(screen, 'Type', 45, (200, 200, 200), (1700, 275), centerY=False)
        
        self.oTypeSelect.draw(screen, ["call","put"], (1575, 315), (250, 50), colors=[(50, 180, 169),(127,25,255)],txtsize=35)
    
    def drawStrike(self,screen,stock:Stock):
        drawCenterTxt(screen, 'Strike', 45, (180, 180, 180), (1530, 427), centerX=False)

        if self.strikePrice is None and self.inputMode != "strike_keyboard":# if the strike price has not been set
            result = drawClickableBox(screen, (1875, 427), "Set Value", 45, (0,0,0), (160,160,160),centerY=True,fill=True,topLeftX=True)
            
            if result:# if the set value box has been clicked
                self.inputMode = "strike_keyboard"# enable keyboard input
        
        elif self.inputMode == "strike_keyboard" and self.strikePrice is None:# if keyboard input is being used
            # Draw the keyboard input interface below the stock graph
            self.drawKeyboardInput(screen, "strike")
        
        else:# if the value has been confirmed
            result = drawClickableBox(screen, (1862, 428), f"${limit_digits(self.strikePrice, 10)}", 55, (200,200,200), (0,0,0),centerY=True,border=False,topLeftX=True)
            if result: 
                self.strikePrice = None; self.inputMode = None
                self.strike_input_text = ""

    def drawDate(self,screen,gametime:GameTime):
        dateTxt = s_render('Exp Date', 40, (200, 200, 200))
        screen.blit(dateTxt, (1530, 537-dateTxt.get_height()/2))
        
        if self.expDate is None and self.inputMode != "date_keyboard":
            result = drawClickableBox(screen, (1875, 537), "Set Date", 45, (0,0,0), (170,170,170),centerY=True,fill=True,topLeftX=True)
            
            if result:# if the set date box has been clicked
                self.inputMode = "date_keyboard"# enable keyboard input

        elif self.inputMode == "date_keyboard" and self.expDate is None:# if keyboard input is being used
            # Draw the keyboard input interface below the stock graph
            self.drawKeyboardInput(screen, "date", gametime)
        
        else:# if the value has been confirmed
            days_text = f"{self.expDate} Day{'s' if self.expDate != 1 else ''}"
            result = drawClickableBox(screen, (1885, 485), days_text, 55, (200,200,200), (0,0,0),border=False,topLeftX=True)
            if result: 
                self.expDate = None; self.inputMode = None
                self.date_input_text = ""
            else:

                timeOffset = gametime.time+timedelta(days=self.expDate)
                drawCenterTxt(screen, f"{timeOffset.strftime('%m/%d/%Y')}", 40, (120, 120, 120), (1860, 545),centerX=False,centerY=False,fullX=True)
    
    def drawEstPrice(self,screen,saveResult:bool,gametime:GameTime,stock:Stock):
        drawCenterTxt(screen, 'Est Price', 40, (200, 200, 200), (1530, 642), centerX=False)
            
        if self.strikePrice != None and self.expDate != None:# if the strike price and expiration date have been set
            if self.inputMode is None:# if no input method is active
                timeOffset = (gametime.time+timedelta(days=self.expDate))
                
                if self.newOptionObj is None:# if the new option object has not been created
                    self.newOptionObj = OptionAsset(self.player,stock,self.strikePrice,timeOffset,self.oTypeSelect.getSelected(),str(gametime),1)
                else:# if the new option object has been created
                    self.newOptionObj.setValues(strikePrice=self.strikePrice,expDate=timeOffset,optionType=self.oTypeSelect.getSelected())
                
                price = self.newOptionObj.getValue(bypass=True)
                drawCenterTxt(screen, f"${limit_digits(price,15)}", 55, (200, 200, 200), (1860, 620), centerX=False, centerY=False,fullX=True)
                
                if saveResult:# if the save button has been clicked
                    self.savedOptions.append(self.newOptionObj)# save the new option
                    self.selectOption = self.newOptionObj# select the new option
                    self.strikePrice,self.newOptionObj,self.expDate = None, None, None# reset the new option info
                    self.inputMode = None
                    self.strike_input_text = ""
                    self.date_input_text = ""
                    self.creatingOption = False# stop creating the option

        if self.strikePrice is None or self.expDate is None or self.inputMode is not None:# if the strike price or expiration date have not been set or input is active
            drawCenterTxt(screen, f"N/A", 55, (200, 200, 200), (1860, 620), centerX=False, centerY=False,fullX=True)

    def handleKeyboardInput(self, input_type):
        """Handle keyboard input for strike price or date input"""
        import time
        
        keys = pygame.key.get_pressed()
        current_time = time.time()
        
        # Handle backspace
        if keys[pygame.K_BACKSPACE] and current_time - self.last_key_time > 0.1:
            if input_type == "strike" and self.strike_input_text:
                self.strike_input_text = self.strike_input_text[:-1]
                self.last_key_time = current_time
            elif input_type == "date" and self.date_input_text:
                self.date_input_text = self.date_input_text[:-1]
                self.last_key_time = current_time
        
        # Handle Enter key (same as confirm)
        if keys[pygame.K_RETURN] and current_time - self.last_key_time > 0.2:
            self.last_key_time = current_time
            if input_type == "strike":
                try:
                    value = float(self.strike_input_text) if self.strike_input_text else 0
                    if value > 0:
                        self.strikePrice = value
                        self.inputMode = None
                        self.strike_input_text = ""
                except ValueError:
                    pass
            elif input_type == "date":
                try:
                    days = int(self.date_input_text) if self.date_input_text else 0
                    if 0 < days <= 365*3:
                        from Classes.AssetTypes.OptionAsset import getCloseOpenDate
                        from datetime import timedelta
                        # Calculate actual trading days
                        newNumDays = (getCloseOpenDate(self.player.gametime.time+timedelta(days=days))-self.player.gametime.time).days
                        self.expDate = newNumDays
                        self.inputMode = None
                        self.date_input_text = ""
                except ValueError:
                    pass
        
        # Handle Escape key (same as cancel)
        if keys[pygame.K_ESCAPE] and current_time - self.last_key_time > 0.2:
            self.last_key_time = current_time
            self.inputMode = None
            if input_type == "strike":
                self.strike_input_text = ""
            else:
                self.date_input_text = ""
        
        # Handle number input
        number_keys = {
            pygame.K_0: "0", pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3", pygame.K_4: "4",
            pygame.K_5: "5", pygame.K_6: "6", pygame.K_7: "7", pygame.K_8: "8", pygame.K_9: "9",
            pygame.K_KP0: "0", pygame.K_KP1: "1", pygame.K_KP2: "2", pygame.K_KP3: "3", pygame.K_KP4: "4",
            pygame.K_KP5: "5", pygame.K_KP6: "6", pygame.K_KP7: "7", pygame.K_KP8: "8", pygame.K_KP9: "9"
        }
        
        for key, char in number_keys.items():
            if keys[key] and current_time - self.last_key_time > 0.1:
                if input_type == "strike" and len(self.strike_input_text) < 10:
                    self.strike_input_text += char
                    self.last_key_time = current_time
                elif input_type == "date" and len(self.date_input_text) < 4:
                    self.date_input_text += char
                    self.last_key_time = current_time
        
        # Handle decimal point for strike price
        if input_type == "strike" and (keys[pygame.K_PERIOD] or keys[pygame.K_KP_PERIOD]) and current_time - self.last_key_time > 0.1:
            if "." not in self.strike_input_text and len(self.strike_input_text) < 9:
                self.strike_input_text += "."
                self.last_key_time = current_time

    def updateTextInputs(self):
        """Update text inputs by handling current keys if they are focused"""
        if self.inputMode == "strike_keyboard":
            self.handleKeyboardInput("strike")
        elif self.inputMode == "date_keyboard":
            self.handleKeyboardInput("date")

    def drawKeyboardInput(self, screen, input_type, gametime=None):
        """Draw keyboard input interface in the area below the stock graph"""
        # Main container area: between 585,565 and 1485,945
        container_x, container_y = 600, 580
        container_w, container_h = 870, 280
        
        # Draw border only (no dark background for performance)
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(container_x, container_y, container_w, container_h), 3, border_radius=10)
        
        # Draw title
        title = "Enter Strike Price" if input_type == "strike" else "Enter Expiration Date"
        drawCenterTxt(screen, title, 55, (200, 200, 200), (container_x + container_w//2, container_y + 30), centerX=True, centerY=False)
        
        # Draw input box
        input_rect = pygame.Rect(container_x + 50, container_y + 80, container_w - 100, 80)
        pygame.draw.rect(screen, (40, 40, 40), input_rect, border_radius=5)
        pygame.draw.rect(screen, (150, 150, 150), input_rect, 3, border_radius=5)
        
        # Get current text and format it
        if input_type == "strike":
            current_text = self.strike_input_text
            display_text = f"${limit_digits(float(current_text))}" if current_text else "$0.00"
        else:
            current_text = self.date_input_text
            display_text = f"{limit_digits(float(current_text),truncate=True)} days" if current_text else "0 days"
        
        # Draw text or placeholder
        # if current_text:
        #     text_surface = s_render(display_text, 50, (200, 200, 200))
        # else:
        #     text_surface = s_render(placeholder, 45, (120, 120, 120))
        
        # text_x = input_rect.x + 20
        # text_y = input_rect.y + (input_rect.height - text_surface.get_height()) // 2
        # screen.blit(text_surface, (text_x, text_y))
        displayTextRender = s_render(display_text, 50, (200, 200, 200))
        drawCenterRendered(screen, displayTextRender, (input_rect.x + 20, input_rect.y + input_rect.height//2), centerX=False, centerY=True)

        # Draw blinking cursor
        import time
        if int(time.time() * 2) % 2:  # Blink every 0.5 seconds
            # if input_type == "strike":
            #     cursor_x = text_x + (displayTextRender.get_width() if current_text else s_render("$", 50, (200, 200, 200)).get_width())
            # else:
            #     cursor_x = text_x + (displayTextRender.get_width() if current_text else 0)
            if input_type == "date":
                modified_text = f"{limit_digits(float(current_text),truncate=True)}" if current_text else "0"
                displayTextRender = s_render(modified_text, 50, (200, 200, 200))

            cursor_x = input_rect.x + 20 + displayTextRender.get_width()
            pygame.draw.line(screen, (200, 200, 200), (cursor_x, input_rect.y + 15), (cursor_x, input_rect.y + input_rect.height - 15), 3)
        
        # Draw preview/validation info
        info_y = container_y + 175
        if input_type == "strike" and current_text:
            try:
                value = float(current_text)
                if value > 0:
                    drawCenterTxt(screen, f"Strike Price: ${limit_digits(value, 10)}", 40, (100, 200, 100), (container_x + container_w//2, info_y), centerX=True, centerY=False)
                else:
                    drawCenterTxt(screen, "Strike price must be greater than 0", 35, (200, 100, 100), (container_x + container_w//2, info_y), centerX=True, centerY=False)
            except ValueError:
                drawCenterTxt(screen, "Invalid number format", 35, (200, 100, 100), (container_x + container_w//2, info_y), centerX=True, centerY=False)
        elif input_type == "date" and current_text and gametime:
            try:
                days = int(current_text)
                if 0 < days <= 365*3:
                    timeOffset = gametime.time + timedelta(days=days)
                    drawCenterTxt(screen, f"Expires in {limit_digits(days, 10)} day{'s' if days > 1 else ''}", 40, (100, 200, 100), (container_x + container_w//2, info_y), centerX=True, centerY=False)
                    drawCenterTxt(screen, f"Date: {timeOffset.strftime('%m/%d/%Y')}", 35, (150, 150, 150), (container_x + container_w//2, info_y + 35), centerX=True, centerY=False)
                else:
                    drawCenterTxt(screen, "Must be between 1 and 1095 days (3 years)", 35, (200, 100, 100), (container_x + container_w//2, info_y), centerX=True, centerY=False)
            except ValueError:
                drawCenterTxt(screen, "Invalid number format", 35, (200, 100, 100), (container_x + container_w//2, info_y), centerX=True, centerY=False)
        
        # Draw buttons (moved up)
        button_y = container_y + 210
        confirm_result = drawClickableBoxWH(screen, (container_x + 50, button_y), (200, 50), "Confirm (Enter)", 40, (0, 0, 0), (0, 180, 0), fill=True)
        cancel_result = drawClickableBoxWH(screen, (container_x + container_w - 250, button_y), (200, 50), "Cancel (Esc)", 40, (0, 0, 0), (180, 0, 0), fill=True)
        
        # Handle button results
        if confirm_result:
            if input_type == "strike":
                try:
                    value = float(current_text) if current_text else 0
                    if value > 0:
                        self.strikePrice = value
                        self.inputMode = None
                        self.strike_input_text = ""
                except ValueError:
                    pass
            else:  # date
                try:
                    days = int(current_text) if current_text else 0
                    if 0 < days <= 365*3:
                        newNumDays = (getCloseOpenDate(gametime.time+timedelta(days=days))-gametime.time).days
                        self.expDate = newNumDays
                        self.inputMode = None
                        self.date_input_text = ""
                except ValueError:
                    pass
        elif cancel_result:
            self.inputMode = None
            if input_type == "strike":
                self.strike_input_text = ""
            else:
                self.date_input_text = ""

    def drawCustOptions(self,screen:pygame.Surface,gametime:GameTime,stock:Stock):
        """Handles the logic for creating a custom option"""
        
        # Update text inputs
        self.updateTextInputs()
        
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
                self.inputMode = None
                self.strike_input_text = ""
                self.date_input_text = ""
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
        selectedindex = None if select is None else optionList.index(select)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)
        
        newselected = self.cucOptionScrll.draw_polys(screen, (x, y), (w, y+h),selectedindex, True, *[self.determineColor(option.getType()) for option in optionList[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        
        if newselected != None: self.creatingOption = False
        if select is None:# if the latterscroll didn't contain the selected asset before
            self.selectOption = self.selectOption if newselected is None else optionList[newselected]
        else:# if the latterscroll contained the selected asset before, then it can set it to none if you select it again
            self.selectOption = None if newselected is None else optionList[newselected]

        # self.selectOption = self.selectOption if newselected is None else optionList[newselected]# Changes selected stock if the new selected has something
        txt = s_render(f"{ommitted[0]} - {ommitted[1]-1} out of {len(optionList)} Options",35,(0,0,0))
        screen.blit(txt,(1700-txt.get_width()/2,950))
        return self.selectOption