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
        stocknames = [stock.name for stock in stocklist]
        self.findStockObj = lambda name: stocklist[stocknames.index(name)] 
        self.avaiOptionSc = CustomColorLatter()
        self.selcOption = None
        self.newOptionInfo = None# list containing info for the new option that is being created, [strikePrice, expirationDate]
        # self.premadeOptions = {
        #     stock:OptionAsset(player,stock,self.getRandomStrike(stock,)) for stock in stocklist
        # }
        # for i in range(8):
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
        determineColor = lambda optionType: (127,25,255) if optionType == "put" else (50, 180, 169)# determines the color of the asset
        # dateText = lambda date: f'{date.month}/{date.day}/{date.year}'# returns the date in the format mm/dd/yyyy
        daysLeft = lambda option: f'{option.daysToExpiration(gametime.time)} Day{"s" if option.daysToExpiration(gametime.time) > 1 else ""}'
        get_text = lambda option : [f'${limit_digits(option.getValue(),15)} ',f'{option.getType().capitalize()}',f'{daysLeft(option)}',f'{option.getExpDate()}']# returns the text for the stock
        textlist = [get_text(option) for option in optionList]# stores 3 texts for each asset in the stocks list

        textinfo = []# stores the text info for the latter scroll [text,fontsize,color]
        coords = [[(20,15),(30,60)] for i in range(len(textlist))]

        for i,(text,option) in enumerate(zip(textlist,optionList)):# loop through the textlist and store the text info in the textinfo list
            if self.selcOption == option:
                option.getValue(bypass=True)

            polytexts = []# temporary list to store the text info for each asset
            polytexts.extend([[text[0],50,(255,255,255)],[text[1],45,determineColor(option.getType())],[text[2],50,(190,190,190)],[text[3],30,(170,170,170)]])# appends the text info for the asset            
            textinfo.append(polytexts)
            coords[i].append(((text[1],150),15))
            coords[i].append(((text[1],155),60))

        self.avaiOptionSc.storetextinfo(textinfo); self.avaiOptionSc.set_textcoords(coords)# stores the text info and the coords for the latter scroll
        ommitted = self.avaiOptionSc.store_rendercoords((205, 270), (370,950),135,0,0,updatefreq=60)
        self.selcOption = self.selcOption if self.selcOption in optionList else None# Ensuring that the selected stock is in the optionlist

        selectedindex = None if self.selcOption == None else optionList.index(self.selcOption)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)
        
        newselected = self.avaiOptionSc.draw_polys(screen, (205, 270), (370,950), mousebuttons, selectedindex, True, *[determineColor(option.getType()) for option in optionList[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        self.selcOption = self.selcOption if newselected == None else optionList[newselected]# Changes selected stock if the new selected has something
        txt = s_render(f"{ommitted[0]} - {ommitted[1]-1} out of {len(optionList)} Options",35,(0,0,0))
        screen.blit(txt,(390-txt.get_width()/2,950))
    
    def customOptionLogic(self,screen:pygame.Surface,mousebuttons:int,gametime:GameTime,stock:Stock):

        # pygame.draw.rect(screen,(0,0,0),pygame.Rect(1510,260,390,415),5,10)

        
        
        if self.newOptionInfo == None:# if there is no new option being created (display the create new option button)
            pygame.draw.rect(screen,(0,0,0),pygame.Rect(1520,270,200,50),5,10)
            createColor = (0,190,0)
            if pygame.Rect(1520,270,200,50).collidepoint(pygame.mouse.get_pos()):
                createColor = (0,255,0)
                if mousebuttons == 1:
                    # newOptionInfo is [strikePrice, expirationDate]
                    self.newOptionInfo = [None,None,None]# changing it, the nones represent that no data is in it yet so it will display a set value box
            
            createTxt = s_render('+ Create New', 45, createColor)
            screen.blit(createTxt, (1620-createTxt.get_width()/2, 280))
        else:# if there is a new option being created

            typeTxt = s_render('Option Type', 40, (200, 200, 200))
            screen.blit(typeTxt, (1700-typeTxt.get_width()/2, 275))
            # wh = 250
            # 1575-320(127,25,255) if optionType == "put" else (50, 180, 169)
            self.oTypeSelect.draw(screen, ["Call","Put"], (1575, 320), (250, 50), colors=[(50, 180, 169),(127,25,255)],txtsize=35)

            strikeTxt = s_render('Strike Price', 40, (200, 200, 200))
            screen.blit(strikeTxt, (1700-strikeTxt.get_width()/2, 385))

            if self.newOptionInfo[0] == None:
                result = drawClickableBox(screen, (1700, 420), "Set Value", 45, (0,0,0), (160,160,160), mousebuttons,centerX=True,fill=True)
                self.newOptionInfo[0] = result if result else None
            elif type(self.newOptionInfo[0]) == bool:# if the box has been clicked, but no value has been confirmed

                self.strikeNumPad.draw(screen,(1050,190),(450,400),"",mousebuttons,stock.price*2)# draw the numpad
                numValTxt = s_render(f"${self.strikeNumPad.getValue()}", 60, (200, 200, 200))
                screen.blit(numValTxt, (1700-numValTxt.get_width()/2, 420))

            dateTxt = s_render('Expiration Date', 40, (200, 200, 200))
            screen.blit(dateTxt, (1700-dateTxt.get_width()/2, 485))

            if self.newOptionInfo[1] == None:
                result = drawClickableBox(screen, (1700, 520), "Set Date", 45, (0,0,0), (170,170,170), mousebuttons, centerX=True,fill=True)
                self.newOptionInfo[1] = result if result else None

            priceTxt = s_render('Est. Price', 40, (200, 200, 200))
            screen.blit(priceTxt, (1700-priceTxt.get_width()/2, 605))



            drawClickableBox(screen, (1700, 680), "Save & Continue", 45, (0,0,0), (0,205,0), mousebuttons, centerX=True)




        

    def drawCustomOptions(self,screen:pygame.Surface,mousebuttons:int,gametime:GameTime,stock:Stock):

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1500,210,400,740),5,10)
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1500,210,400,50),5,10)

        avOptiontxt = s_render('Custom Options', 45, (255, 255, 255))
        screen.blit(avOptiontxt, (1700-avOptiontxt.get_width()/2, 220))
        self.customOptionLogic(screen,mousebuttons,gametime,stock)

        


    def drawStockInfo(self,screen:pygame.Surface, gametime, stock:Stock):
        """Draws the info underneath the stock graph on the left"""
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
        drawLinedInfo(screen,(1055,210),(435,335),info,40,TXTCOLOR)

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player,gametime):
        
        screen.blit(s_render('Select a Stock', 36, (255, 255, 255)), (220, 110))
        self.stockSelection.draw(screen, [stock.name for stock in stocklist], [200, 150], [1700, 50], colors=[stock.color for stock in stocklist],txtsize=35)

        stock = self.findStockObj(self.stockSelection.getSelected())
        self.stockGraph.setStockObj(stock)
        self.stockGraph.drawFull(screen, (585,210),(460,350),"OptionMenu Graph",True,"Normal")
        if self.newOptionInfo == None or (self.newOptionInfo and type(self.newOptionInfo[0]) != bool):
            self.drawStockInfo(screen,gametime,stock)
        self.drawAvailableOptions(screen,mousebuttons,gametime,stock)
        self.drawCustomOptions(screen,mousebuttons,gametime,stock)


        


        
        

