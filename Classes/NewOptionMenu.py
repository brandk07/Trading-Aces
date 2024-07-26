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
        self.fillPreMadeOptions()
        self.stockGraph : StockVisualizer = StockVisualizer(gametime,stocklist[0],stocklist)
        self.barSelection : SelectionBar = SelectionBar()
        stocknames = [stock.name for stock in stocklist]
        self.findStockObj = lambda name: stocklist[stocknames.index(name)] 
        self.avaiOptionSc = CustomColorLatter()
        self.selcOption = None
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

    def drawAvailableOptions(self,screen:pygame.Surface,mousebuttons:int,stocklist,gametime:GameTime,stock:Stock):
        
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(200,210,380,740),5,10)
        # pygame.draw.rect(screen,(20,20,20),pygame.Rect(200,235,380,715),border_radius=10)
        avOptiontxt = s_render('Available Options', 45, (255, 255, 255))
        screen.blit(avOptiontxt, (390-avOptiontxt.get_width()/2, 215))


        # DRAWING THE LATTER SCROLL
        optionList = self.preMadeOptions[stock]
        determineColor = lambda optionType: (127,0,255) if optionType == "put" else (0,0,205)# determines the color of the asset
        # dateText = lambda date: f'{date.month}/{date.day}/{date.year}'# returns the date in the format mm/dd/yyyy
        daysLeft = lambda option: f'{option.daysToExpiration(gametime.time)} Day{"s" if option.daysToExpiration(gametime.time) > 1 else ""}'
        get_text = lambda option : [f'${option.getStrike()} ',f'{option.getType().capitalize()}',f'{daysLeft(option)}',f'{option.getExpDate()}']# returns the text for the stock
        textlist = [get_text(option) for option in optionList]# stores 3 texts for each asset in the stocks list

        textinfo = []# stores the text info for the latter scroll [text,fontsize,color]
        coords = [[(20,15),(30,60)] for i in range(len(textlist))]

        for i,(text,option) in enumerate(zip(textlist,optionList)):# loop through the textlist and store the text info in the textinfo list
            polytexts = []# temporary list to store the text info for each asset
            polytexts.extend([[text[0],50,(255,255,255)],[text[1],45,determineColor(option.getType())],[text[2],50,(190,190,190)],[text[3],30,(170,170,170)]])# appends the text info for the asset            
            textinfo.append(polytexts)
            coords[i].append(((text[1],150),15))
            coords[i].append(((text[1],155),60))

        self.avaiOptionSc.storetextinfo(textinfo); self.avaiOptionSc.set_textcoords(coords)# stores the text info and the coords for the latter scroll
        ommitted = self.avaiOptionSc.store_rendercoords((205, 270), (355,960),135,0,0,updatefreq=0)
        self.selcOption = self.selcOption if self.selcOption in optionList else None# Ensuring that the selected stock is in the optionlist

        selectedindex = None if self.selcOption == None else optionList.index(self.selcOption)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)
        
        newselected = self.avaiOptionSc.draw_polys(screen, (205, 270), (355,960), mousebuttons, selectedindex, True, *[determineColor(option.getType()) for option in optionList[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        self.selcOption = self.selcOption if newselected == None else optionList[newselected]# Changes selected stock if the new selected has something


    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player,gametime):
        
        screen.blit(s_render('Select a Stock', 36, (255, 255, 255)), (220, 110))
        self.barSelection.draw(screen, [stock.name for stock in stocklist], [200, 150], [1700, 50], colors=[stock.color for stock in stocklist],txtsize=35)

        stock = self.findStockObj(self.barSelection.getSelected())
        self.stockGraph.setStockObj(stock)
        self.stockGraph.drawFull(screen, (620,220),(400,300),"OptionMenu Graph",True,"Normal")

        self.drawAvailableOptions(screen,mousebuttons,stocklist,gametime,stock)

        


        
        

