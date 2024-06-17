import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.Menu import Menu
import numpy as np
from Classes.imports.Bar import SliderBar
from Classes.AssetTypes.StockAsset import StockAsset
from Classes.StockVisualizer import StockVisualizer
from Classes.imports.OrderScreen import OrderScreen
from Classes.imports.Latterscroll import PortfolioLatter
from Classes.Stock import Stock
import datetime

TXTCOLOR = (220,220,220)
class Stockbook2(Menu):
    def __init__(self,stocklist,gametime,orderScreen) -> None:
        self.icon = pygame.image.load(r'Assets\Menu_Icons\stockbook.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon,(140,100))
        super().__init__(self.icon)
        # self.quantity = 0
        stocknames = [stock.name for stock in stocklist]
        self.stocktext = {name:[] for name in stocknames}# a dictionary containing the stock names as keys and the stock descriptions as values
        self.createDescriptions(stocknames)
        self.selectedStock : Stock = stocklist[0]
        self.menudrawn = True
        self.stocklist = stocklist
        self.purchasetext = [fontlist[65].render(text, color)[0] for text,color in zip(['PURCHASE','PURCHASE','INSUFFICIENT'],[(0,150,0),(225,225,225),(150,0,0)])]
        self.quantitybar = SliderBar(50,[(150,150,150),(10,10,10)],barcolor=((20,130,20),(40,200,40)))
        self.stockGraph = StockVisualizer(gametime,stocklist[0],stocklist)
        self.latterScroll = PortfolioLatter()
        self.orderScreen = orderScreen
        self.oScreenDisp = True
        

    def createDescriptions(self,stocknames):
        with open(r'Assets\newstockdes.txt','r') as descriptions:
            filecontents = descriptions.readlines()
            for i,line in enumerate(filecontents):
                for stockname in stocknames:
                    if line.replace('\n','') == stockname:
                        self.stocktext[stockname].append(filecontents[i+1].replace('\n',''))# Full stock name Ex. "Kyronix Solutions Inc. (KSTON)"
                        seperatatedstrings = separate_strings((filecontents[i+2].replace('\n','')),4)
                        for string in seperatatedstrings:# a list containing 4 strings 
                            self.stocktext[stockname].append(string)

        self.renderedstocknames = {name:fontlist[90].render(name,(150,150,150))[0] for name in stocknames}
        for key,lines in self.stocktext.items():#rendering the text that displays info about the stocks
            for i,line in enumerate(lines):
                if i == 0:#if its the first line, render it with a larger font and grey color
                    self.stocktext[key][i] = fontlist[40].render(line,(120, 120, 120))[0]
                else:#else render it with a smaller font and orange color
                    self.stocktext[key][i] = fontlist[30].render(line,(225, 130, 0))[0]
    
    def changeselectedStock(self,name=None,stockobj=None):
        if name:
            self.selectedStock = [stock for stock in self.stocklist if stock.name == name]
            self.stockGraph.setStockObj(self.stocklist[self.selectedStock])
        elif stockobj:
            self.selectedStock = stockobj
            self.stockGraph.setStockObj(self.stocklist[self.selectedStock])
        else:
            raise ValueError('You must provide either a name or an object')

    def drawStockLatter(self,screen:pygame.Surface,mousebuttons:int,player):
        """Draws the Latterscroll with all the stocks in the middle"""

        get_text = lambda stock : [f'{stock} ',f'{"+" if stock.getPercent() > 0 else ""}{limit_digits(stock.getPercent(),15)}%',f'${limit_digits(stock.getValue(),15)}']# returns the text for the stock
        # getting the text for each asset
        textlist = [get_text(stock) for stock in self.stocklist]# stores 3 texts for each asset in the stocks list

        textinfo = []# stores the text info for the latter scroll [text,fontsize,color]
        coords = [[(20,15),(25,60)] for i in range(len(textlist))]
        # loop through the textlist and store the text info in the textinfo list
        for i,(text,stock) in enumerate(zip(textlist,self.stocklist)):
            polytexts = []# temporary list to store the text info for each asset
            polytexts.append([text[0],50,stock.color])
            polytexts.append([text[1],35,(190,190,190)])
            polytexts.append([text[2],70,(190,190,190)])
            textinfo.append(polytexts)
            coords[i].append(((text[1],100),30))

        self.latterScroll.storetextinfo(textinfo)# simply changes the s.texts in latterscroll
        self.latterScroll.set_textcoords(coords)# simply changes the s.textcoords in latterscroll
        # Does most of the work for the latter scroll, renders the text and finds all the coords
        scrollmaxcoords = (435,975)
        ommitted = self.latterScroll.store_rendercoords((745, 135), scrollmaxcoords,135,0,0,updatefreq=60)

        # drawing the latter scroll and assigning the selected asset
        if self.selectedStock not in self.stocklist:
            self.selectedStock = None
        selectedindex = None if self.selectedStock == None else self.stocklist.index(self.selectedStock)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)
        newselected = self.latterScroll.draw_polys(screen, (745, 135), scrollmaxcoords, mousebuttons, selectedindex, True, *[sasset.getPercent() for sasset in self.stocklist[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        if newselected != None:
            self.selectedStock = self.stocklist[newselected]

        # make a text saying displaying # out of # assets
        dispText = s_render(f"Displaying {ommitted[0]} - {ommitted[1]-1} out of {len(self.stocklist)}",35,(220,220,220))
        screen.blit(dispText,(800,105))
    
    def drawQuarterlyReports(self,screen:pygame.Surface,stockname:str,coords:tuple):
        """Draws the quarterly reports for the stock on the right top"""
        pass

    def drawNews(self,screen:pygame.Surface,stockname:str,coords:tuple):
        """Draws the news for the stock on the right middle """
        pass

    def drawBuySellInfo(self,screen:pygame.Surface,gametime):
        """Draws the info underneath the stock graph on the left"""
        keys = ["Open","High (1W)","Low (1W)","Dividend","Volatility"]
        g = gametime.time
        marketOpenTime = datetime.datetime.strptime(f"{g.month}/{g.day}/{g.year} 9:30:00 AM", "%m/%d/%Y %I:%M:%S %p")
        values = [
            f"${limit_digits(self.selectedStock.getPointDate(marketOpenTime,gametime.time),12)}",
            f"${limit_digits(max(self.selectedStock.graphs['1W']),12)}",
            f"${limit_digits(min(self.selectedStock.graphs['1W']),12)}",
            f"{limit_digits(self.selectedStock.dividend,12)}%",
            f"{limit_digits(self.selectedStock.getVolatility()*100,12)}%"
        ]
        info = {key:value for key,value in zip(keys,values)}
        drawLinedInfo(screen,(190,570),(550,300),info,40,TXTCOLOR)

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player,gametime):
        mousex, mousey = pygame.mouse.get_pos()

        bmouse = mousebuttons# click still needs to go to the order screen
        if self.oScreenDisp:# Can't click anything if the order screen is displayed
            mousebuttons = 0
        # Draw the stock graph
        self.stockGraph.drawFull(screen, (190,100),(550,450),"StockBook Graph",True,"Normal")

        # Draw the stock name & description
        screen.blit(s_render(self.selectedStock.name,90,self.selectedStock.color),(1250,710))# blits the stock name to the screen
        for i,line in enumerate(self.stocktext[self.selectedStock.name]):
            x,y = (1250+((i-1)*8) if i != 0 else self.renderedstocknames[self.selectedStock.name].get_width()+1255),(800+((i-1)*40) if i != 0 else 725)
            screen.blit(line,(x,y))

        self.drawStockLatter(screen, mousebuttons, player)
        # self.drawQuarterlyReports(screen,self.selectedStock.name,(190,100))
        # self.drawNews(screen,self.selectedStock.name,(190,100))
        self.drawBuySellInfo(screen,gametime)

        if self.oScreenDisp:
            self.oScreenDisp = self.orderScreen.draw(screen,self.selectedStock,bmouse,player)


