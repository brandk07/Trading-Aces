import pygame
from Defs import *
from pygame import gfxdraw
from Classes.Menus.Menu import Menu
import numpy as np
from Classes.imports.StockVisualizer import StockVisualizer
# from Classes.imports.OrderScreen import OrderScreen
from Classes.imports.UIElements.Latterscroll import PortfolioLatter,LatterScroll
from Classes.BigClasses.Stock import Stock
from Classes.imports.UIElements.BarGraph import BarGraph
from Classes.imports.UIElements.SelectionElements import SelectionBar
import datetime

TXTCOLOR = (220,220,220)
class Stockbook(Menu):
    def __init__(self,stocklist,gametime,orderScreen) -> None:
        self.icon = pygame.image.load(r'Assets\Menu_Icons\stockbook.png').convert_alpha()
        self.icon = pygame.transform.smoothscale(self.icon,(140,100))
        super().__init__(self.icon)
        # self.quantity = 0
        stocknames = [stock.name for stock in stocklist]
        self.stocktext = {name:[] for name in stocknames}# a dictionary containing the stock names as keys and the stock descriptions as values
        self.createDescriptions(stocknames)
        self.selectedStock : Stock = stocklist[0]
        self.menudrawn = False
        self.stocklist = stocklist
        # self.purchasetext = [fontlist[65].render(text, color)[0] for text,color in zip(['PURCHASE','PURCHASE','INSUFFICIENT'],[(0,150,0),(225,225,225),(150,0,0)])]
        self.stockGraph : StockVisualizer = StockVisualizer(gametime,stocklist[0],stocklist)
        self.stockLS : PortfolioLatter = PortfolioLatter()
        # self.futureRepLS, self.pastRepLS = LatterScroll(), LatterScroll()
        self.orderScreen = orderScreen
        # self.middleDisplays = ["Info","Reports","News"]
        self.middleDisplays = ["Info","Reports"]
        self.currentMDisp = self.middleDisplays[0]
        self.oScreenDisp = False
        self.reportBarGraph : BarGraph = BarGraph("Report Outlook",(450,190),(940,740))
        self.barSelection : SelectionBar = SelectionBar()

        
        radius_x, radius_y = 180, 220# Used for the volatility element
        self.arcEllipseSurf = pygame.Surface(((radius_x+5)*2,radius_y), pygame.SRCALPHA)
        pygame.draw.ellipse(self.arcEllipseSurf, (0, 0, 0), (0, 0, (radius_x+5)*2, radius_y*2), 7)
        

    def createDescriptions(self,stocknames): 
        with open(r'Assets\stockdes3.txt','r') as descriptions:
            filecontents = descriptions.readlines()
            for i,line in enumerate(filecontents):
                for stockname in stocknames:
                    if line.replace('\n','') == stockname:
                        self.stocktext[stockname].append(filecontents[i-1].replace('\n',''))# Full stock name Ex. "Kyronix Solutions Inc. (KSTON)"
                        seperatatedstrings = separate_strings((filecontents[i+1].replace('\n','')),5)
                        for string in seperatatedstrings:# a list containing 4 strings 
                            self.stocktext[stockname].append(string)

        self.renderedstocknames = {name:fontlist[90].render(name,(150,150,150))[0] for name in stocknames}
        for key,lines in self.stocktext.items():#rendering the text that displays info about the stocks
            for i,line in enumerate(lines):
                if i == 0:#if its the first line, render it with a larger font and grey color
                    self.stocktext[key][i] = fontlist[40].render(line,(120, 120, 120))[0]
                else:#else render it with a smaller font and orange color
                    self.stocktext[key][i] = fontlist[30].render(line,TXTCOLOR)[0]

    def changeSelectedStock(self,name=None,stockobj=None):
        if name and isinstance(name,str):
            self.selectedStock = [stock for stock in self.stocklist if stock.name == name][0]
            
            self.stockGraph.setStockObj(self.selectedStock)
        elif (stockobj and isinstance(stockobj,Stock)) or (name and isinstance(name,Stock)):
            self.selectedStock = stockobj
            self.stockGraph.setStockObj(self.selectedStock) 
        else:
            raise ValueError('You must provide either a valid name or an object')

    def drawStockLatter(self,screen:pygame.Surface,mousebuttons:int,player):
        """Draws the Latterscroll with all the stocks in the middle"""

        get_text = lambda stock : [f'{stock} ',f'{"+" if stock.getPercent() > 0 else ""}{limit_digits(stock.getPercent(),15)}%',f'${limit_digits(stock.getValue(),15)}']# returns the text for the stock
        textlist = [get_text(stock) for stock in self.stocklist]# stores 3 texts for each asset in the stocks list

        textinfo = []# stores the text info for the latter scroll [text,fontsize,color]
        coords = [[(20,15),(25,60)] for i in range(len(textlist))]

        for i,(text,stock) in enumerate(zip(textlist,self.stocklist)):# loop through the textlist and store the text info in the textinfo list
            polytexts = []# temporary list to store the text info for each asset
            polytexts.extend([[text[0],50,stock.color],[text[1],35,(190,190,190)],[text[2],70,(190,190,190)]])# appends the text info for the asset            
            textinfo.append(polytexts)
            coords[i].append(((text[1],100),30))

        self.stockLS.storetextinfo(textinfo); self.stockLS.set_textcoords(coords)# stores the text info and the coords for the latter scroll
        ommitted = self.stockLS.store_rendercoords((1470, 135), (435,975),135,0,0,updatefreq=0)
        self.selectedStock = self.selectedStock if self.selectedStock in self.stocklist else None# Ensuring that the selected stock is in the stocklist

        selectedindex = None if self.selectedStock == None else self.stocklist.index(self.selectedStock)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)
        newselected = self.stockLS.draw_polys(screen, (1470, 135), (435,975), mousebuttons, selectedindex, True, *[sasset.getPercent() for sasset in self.stocklist[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        self.selectedStock = self.selectedStock if newselected == None else self.stocklist[newselected]# Changes selected stock if the new selected has something

        # screen.blit(s_render(f"Displaying {ommitted[0]} - {ommitted[1]-1} out of {len(self.stocklist)}",35,(220,220,220)),(1535,105))
    
    def drawQuarterlyReports(self,screen:pygame.Surface,gametime,mousebuttons):
        """Draws the quarterly reports for the stock on the right top"""

        # -----------------Drawing the future and past reports----------------
        getDate = lambda time : f"{time.month}/{time.day}/{time.year}"

        # futureDict = {f"Q{report[1]} {getDate(report[0])}":f'{(report[0]-gametime.time).days+1} Day{"s" if (report[0]-gametime.time).days+1 > 1 else ""} Away' for report in self.selectedStock.priceEffects.futureReports}
        # pastDict = {f'Q{report[1]} {getDate(report[0])}':f' {"Beat" if report[2] > 0 else "Miss"} {limit_digits(report[2],15)}%' for report in self.selectedStock.priceEffects.pastReports[:4]}
        
        pygame.draw.rect(screen,(0,0,0),(190,690,350,275),5,10)
        pygame.draw.rect(screen,(0,0,0),(555,690,350,275),5,10)
        
        pastListl = [(f'Q{report.getQ()}',f'{getDate(report.getTime())}') for report in self.selectedStock.priceEffects.pastReports[:4]]
        pastListr =[(f'{"Beat" if report.getPerf() > 0 else "Miss"}', f'{"+" if report.getPerf() > 0 else ""}{limit_digits(report.getPerf(),15)}%') for report in self.selectedStock.priceEffects.pastReports[:4]]
        colors = [(200,0,0) if val[0] == "Miss" else (0,190,0) for val in pastListr]
        # print('dicts are',pastListl,pastListr)
        drawLinedInfoBigColored(screen,(200,710),(330,280),pastListl,pastListr,45,25,colors)

        futureListl = [(f'Q{report.getQ()}',f'{getDate(report.getTime())}') for report in self.selectedStock.priceEffects.futureReports]
        futureListr = [(f'{(report.getTime()-gametime.time).days}',f'Day{"s" if (report.getTime()-gametime.time).days+1 > 1 else ""} Away') for report in self.selectedStock.priceEffects.futureReports]
        colors = [p3choice((200,0,0),(190,190,190),(190,0,0),(val.getTime()-gametime.time).days-25) for val in self.selectedStock.priceEffects.futureReports]
        drawLinedInfoBigColored(screen,(565,710),(330,280),futureListl,futureListr,45,25,colors)
        # drawLinedInfo(screen,(540,710),(330,280),futureDict,30,TXTCOLOR)
        screen.blit(s_render("PAST",50,(220,220,220)),(205,645))
        screen.blit(s_render("UPCOMING",50,(220,220,220)),(575,645))
        # screen.blit(s_render("EXPERT PREDICTION",50,(220,220,220)),(930,645))

        pastReportPer, perfReportPer = self.selectedStock.priceEffects.getLikelyHoods(gametime)
        prediction = self.selectedStock.priceEffects.getQuarterlyLikelyhood(gametime)
 
        changeVals = lambda val : round(val,2) 
        data = [
            (changeVals(pastReportPer),(150,0,230)),
            (changeVals(perfReportPer),(255,128,0)),
            ((changeVals(pastReportPer)+changeVals(perfReportPer)),(140,140,140))
        ]

        self.reportBarGraph.updateValues([d[0] for d in data],[d[1] for d in data],["%"]*len(data))
        self.reportBarGraph.draw(screen,absoluteScale=100)

        # The Text and the boxes indicating which color is which on the bar graph
        pastRtxt = s_render("Past Reports", 40, (220, 220, 220))
        perfRtxt = s_render("Performance", 40, (220, 220, 220))
        predtxt = s_render("Prediction", 40, (220, 220, 220))
        screen.blit(pastRtxt, (930, 640))
        screen.blit(perfRtxt, (1090, 640))
        screen.blit(predtxt, (1275, 640))
        # The boxes indicating which color is which on the bar graph
        pygame.draw.rect(screen, (150, 0, 230), pygame.Rect(930, 680, 35, 35), 0, 10)
        pygame.draw.rect(screen, (255, 128, 0), pygame.Rect(1090, 680, 35, 35), 0, 10)
        pygame.draw.rect(screen, (140, 140, 140), pygame.Rect(1275, 680, 35, 35), 0, 10)

    def drawVolatilityElement(self,screen:pygame.Surface):
        def colorShifter(degree):
            """Returns a color based on the degree
            0 should be green, as you go closer to 180 it should turn yellow, then red"""
            
            # Ensure degree is within the range [0, 180]
            degree = max(0, min(180, degree))
            
            max_value = 180
            
            if degree <= 90:
                # Interpolate between green (0, 200, 0) and yellow (200, 200, 0)
                red = int((degree / 90) * max_value)
                green = max_value
                blue = 0
            else:
                # Interpolate between yellow (200, 200, 0) and red (200, 0, 0)
                red = max_value
                green = int((1 - (degree - 90) / 90) * max_value)
                blue = 0
            
            return (red, green, blue)
        
        pygame.draw.rect(screen,(0,0,0),(760,625,400,325),5,10)


        center_x, center_y = 960, 910
        radius_x, radius_y = 180, 220

        for degree in range(180, 360):
            x = center_x + int(radius_x * math.cos(math.radians(degree)))
            y = center_y + int(radius_y * math.sin(math.radians(degree)))
            pygame.draw.line(screen, colorShifter(degree - 180), (center_x, center_y), (x, y), 7)
        
        screen.blit(self.arcEllipseSurf, (center_x - radius_x-4, center_y - radius_y-1))
        pygame.draw.line(screen, (0, 0, 0), (center_x - radius_x, center_y), (center_x + radius_x, center_y), 7)

        
        currentAngle = (((self.selectedStock.givenVolatility-700)/15)/25)*180+180
        x = 960+int(180*math.cos(math.radians(currentAngle)))
        y = 910+int(220*math.sin(math.radians(currentAngle)))
        pygame.draw.line(screen,(0,0,0),(960,910),(x,y),8)
        # screen.blit(s_render(f"Volatility {self.selectedStock.ceo.getVolatility()}",50,(220,220,220)),(760,630))
        drawCenterTxt(screen,f"Volatility {self.selectedStock.givenVolatility}",50,(220,220,220),(960,635),centerY=False)

    def drawCompanyInfo(self,screen:pygame.Surface,stockname:str,coords:tuple,player):
        """Draws the company info for the stock on the right middle """
        # def pil_to_pygame(image):
        #     """Convert a PIL Image to a Pygame Surface."""
        #     return pygame.image.fromstring(image.tobytes(), image.size, image.mode)
        
        self.drawVolatilityElement(screen)
        # Draw the stock name & description
        
        pygame.draw.rect(screen,(20,20,20),(200,625,550,325),border_radius=10)
        pygame.draw.rect(screen,(0,0,0),(200,625,550,325),5,10)
        screen.blit(s_render(self.selectedStock.name,90,self.selectedStock.color),(210,635))# blits the stock name to the screen
        
        for i,line in enumerate(self.stocktext[self.selectedStock.name]):
            x,y = (210 if i != 0 else self.renderedstocknames[self.selectedStock.name].get_width()+215),(725+((i-1)*40) if i != 0 else 650)
            screen.blit(line,(x,y))

        # Draw Company Volaatility Info

        # # Draw stuff about CEO
        # ceo = self.selectedStock.ceo
        # xCeo,yCeo = 1165,630
        # wCeo,hCeo = 290,325
        
        # drawCenterTxt(screen,"CEO",50,(220,220,220),(xCeo+wCeo/2,yCeo+5),centerY=False)
        # pygame.draw.rect(screen,(0,0,0),(xCeo+wCeo/2-118/2,yCeo+45,128,110),5)# Box for the CEO image
        # screen.blit(ceo.getImageSize(118,100),(xCeo+(wCeo/2)-(118/2)+5,yCeo+50))


        # drawCenterTxt(screen,ceo.name,45,(220,220,220),(xCeo+wCeo/2,yCeo+170),centerY=False)
        # drawCenterTxt(screen,f"{ceo.age} Years Old",35,(180,180,180),(xCeo+wCeo/2,yCeo+210),centerY=False)

        # numslines = int(len(ceo.slogan)/24)+1

        # for i,line in enumerate(ceo.getSloganLines(numslines)):
        #     ex1 = '"' if i == 0 else ''
        #     ex2 = '"' if i == numslines-1 else ''
        #     txt = s_render(ex1+line+ex2,30,(220,220,220))
        #     screen.blit(txt,(xCeo+(wCeo/2)-(txt.get_width()/2),yCeo+240+(i*35)))
        #     # screen.blit(s_render(ex1+line+ex2,30,(220,220,220)),(1180+(i*10),875+(i*35)))
        # pygame.draw.rect(screen,(0,0,0),(1165,625,290,240+35*numslines),5,10)
        
    def drawNews(self,screen:pygame.Surface,stockname:str,coords:tuple):
        """Draws the news for the stock on the right middle """
        pass

    def drawBuySellInfo(self,screen:pygame.Surface,gametime):
        """Draws the info underneath the stock graph on the left"""
        strings = ["Open","High (1M)","Low (1M)","Dividend","Volatility"]
        g = gametime.time
        marketOpenTime = datetime.datetime.strptime(f"{g.month}/{g.day}/{g.year} 9:30:00 AM", "%m/%d/%Y %I:%M:%S %p")
        values = [
            f"${limit_digits(self.selectedStock.getPointDate(marketOpenTime,gametime),12)}",
            f"${limit_digits(max(self.selectedStock.graphs['1M']),12)}",
            f"${limit_digits(min(self.selectedStock.graphs['1M']),12)}",
            f"{limit_digits(self.selectedStock.dividendYield,12)}%",
            f"{limit_digits(self.selectedStock.getVolatility()*100,12)}%"
        ]
        # info = {key:value for key,value in zip(keys,values)}
        info = [(string,value) for string,value in zip(strings,values)]
        drawLinedInfo(screen,(750,100),(700,300),info,40,TXTCOLOR)

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player,gametime):
        mousex, mousey = pygame.mouse.get_pos()

        # Draw the stock graph
        self.stockGraph.setStockObj(self.selectedStock)
        self.stockGraph.drawFull(screen, (190,100),(550,450),"StockBook Graph",True,"Normal")
       

        self.drawStockLatter(screen, mousebuttons, player)
        if drawClickableBox(screen,(879,420),"Create Order",95,(130,130,130),(0,170,0),mousebuttons):
            self.oScreenDisp = True 

        self.barSelection.draw(screen,self.middleDisplays,(195,560),(545,45),mousebuttons,txtsize=35)

        self.drawBuySellInfo(screen,gametime)

        # match self.currentMDisp:
        match self.barSelection.getSelected():
            case "Info":
                self.drawCompanyInfo(screen,self.selectedStock.name,(190,100),player)
                pass
            case "News":
                # self.drawNews(screen,self.selectedStock.name,(190,100))
                pass
            case "Reports":
                self.drawQuarterlyReports(screen,gametime,mousebuttons)
        
        if self.oScreenDisp:
            self.oScreenDisp = self.orderScreen.draw(screen,self.selectedStock,mousebuttons,player,gametime,maxCoords=[1450,1500],minCoords=[190,-500])


