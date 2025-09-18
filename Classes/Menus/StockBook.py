import pygame
import os
from Defs import *
from pygame import gfxdraw
from Classes.Menus.Menu import Menu
from Classes.imports.StockVisualizer import StockVisualizer
# from Classes.imports.OrderScreen import OrderScreen
from Classes.imports.UIElements.Latterscroll import PortfolioLatter,LatterScroll
from Classes.BigClasses.Stock import Stock
from Classes.imports.UIElements.BarGraph import BarGraph
from Classes.imports.UIElements.SelectionElements import SelectionBar
from Classes.imports.UIElements.Numpad import SideWaysNumPad
from Classes.imports.UIElements.OrderBox import OrderBox
import datetime

TXTCOLOR = (220,220,220)
class Stockbook(Menu):
    def __init__(self,stocklist,gametime,orderScreen,currentRun) -> None:
        super().__init__(currentRun)
        # self.quantity = 0
        
        self.stocknames = [stock.name for stock in stocklist]
        self.stocktext = {name:[] for name in self.stocknames}# a dictionary containing the stock names as keys and the stock descriptions as values
        self.createDescriptions(self.stocknames)
        self.selectedStock : Stock = stocklist[0]
        self.menudrawn = False
        self.stocklist = stocklist
        # self.purchasetext = [fontlist[65].render(text, color)[0] for text,color in zip(['PURCHASE','PURCHASE','INSUFFICIENT'],[(0,150,0),(225,225,225),(150,0,0)])]
        self.stockGraph : StockVisualizer = StockVisualizer(gametime,stocklist[0],stocklist)
        self.stockLS : PortfolioLatter = PortfolioLatter()
        self.numPad : SideWaysNumPad = SideWaysNumPad(maxDecimals=0)
        # 760,625 - 1450,950
        self.orderBox : OrderBox = OrderBox((780,430),(640,325),gametime)
        # self.futureRepLS, self.pastRepLS = LatterScroll(), LatterScroll()
        self.orderScreen = orderScreen
        # self.middleDisplays = ["Info","Reports","News"]
        self.middleDisplays = ["Purchase","Info","Reports"]
        self.currentMDisp = self.middleDisplays[0]
        self.oScreenDisp = False
        self.reportBarGraph : BarGraph = BarGraph("Report Outlook",(940,740),(450,190))
        self.barSelection : SelectionBar = SelectionBar()

        
        radius_x, radius_y = 180, 220# Used for the volatility element
        self.arcEllipseSurf = pygame.Surface(((radius_x+5)*2,radius_y), pygame.SRCALPHA)
        pygame.draw.ellipse(self.arcEllipseSurf, (0, 0, 0), (0, 0, (radius_x+5)*2, radius_y*2), 7)
        

    def createDescriptions(self,stocknames): 
        from Defs import get_asset_path
        with open(get_asset_path('GameTexts', 'StockDescriptions.txt'),'r') as descriptions:
            filecontents = descriptions.readlines()
            for i,line in enumerate(filecontents):
                for stockname in stocknames:
                    if line.replace('\n','') == stockname:
                        self.stocktext[stockname].append(filecontents[i-1].replace('\n',''))# Full stock name Ex. "Kyronix Solutions Inc. (KSTON)"
                        seperatatedstrings = separate_strings((filecontents[i+1].replace('\n','')),5)
                        for string in seperatatedstrings:# a list containing 4 strings 
                            self.stocktext[stockname].append(string)

        self.renderedstocknames = {name:get_font('reg', 90).render(name,(150,150,150))[0] for name in stocknames}
        for key,lines in self.stocktext.items():#rendering the text that displays info about the stocks
            for i,line in enumerate(lines):
                if i == 0:#if its the first line, render it with a larger font and grey color
                    self.stocktext[key][i] = get_font('reg', 40).render(line,(120, 120, 120))[0]
                else:#else render it with a smaller font and orange color
                    self.stocktext[key][i] = get_font('reg', 30).render(line,TXTCOLOR)[0]

    def changeSelectedStock(self,name=None,stockobj=None) -> bool:
        if name and isinstance(name,str):
            s = [stock for stock in self.stocklist if stock.name == name]
            if len(s) == 0 or s is None: return False# something didn't work so return false
            self.selectedStock = s[0]
            self.stockGraph.setStockObj(self.selectedStock)
            return True
        elif (stockobj and isinstance(stockobj,Stock)) or (name and isinstance(name,Stock)):
            self.selectedStock = stockobj
            self.stockGraph.setStockObj(self.selectedStock) 
            return True
        else:
            raise ValueError('You must provide either a valid name or an object')

    def drawStockLatter(self,screen:pygame.Surface,player):
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

        selectedindex = None if self.selectedStock is None else self.stocklist.index(self.selectedStock)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)
        newselected = self.stockLS.draw_polys(screen, (1470, 135), (435,975), selectedindex, True, *[sasset.getPercent() for sasset in self.stocklist[ommitted[0]-1:]])# draws the latter scroll and returns the selected asset
        self.selectedStock = self.selectedStock if newselected is None else self.stocklist[newselected]# Changes selected stock if the new selected has something

        # screen.blit(s_render(f"Displaying {ommitted[0]} - {ommitted[1]-1} out of {len(self.stocklist)}",35,(220,220,220)),(1535,105))
    
    def drawQuarterlyReports(self,screen:pygame.Surface,gametime,player):
        """Draws the quarterly reports for the stock on the right top"""

        # -----------------Drawing the future and past reports----------------
        getDate = lambda time : f"{time.month}/{time.day}/{time.year}"


        pygame.draw.rect(screen,(0,0,0),(190,690,350,275),5,10)# border for the lined info on the left (past reports)
        
        pastListl = [(f'Q{report.getQ()}',f'{getDate(report.getTime())}') for report in self.selectedStock.priceEffects.pastReports[:4]]
        pastListr =[(f'{"Beat" if report.getPerf() > 0 else "Miss"}', f'{"+" if report.getPerf() > 0 else ""}{limit_digits(report.getPerf(),15)}%') for report in self.selectedStock.priceEffects.pastReports[:4]]
        colors = [(200,0,0) if val[0] == "Miss" else (0,190,0) for val in pastListr]
       
        drawLinedInfoBigColored(screen,(200,710),(330,280),pastListl,pastListr,45,25,colors)
        screen.blit(s_render("PAST",50,(220,220,220)),(205,645))


        if self.currentRun.getCurrVal("Stock Reports"):# if the stock reports are enabled

            pygame.draw.rect(screen,(0,0,0),(555,690,350,275),5,10)# border for the lined info on the right (future reports)

            futureListl = [(f'Q{report.getQ()}',f'{getDate(report.getTime())}') for report in self.selectedStock.priceEffects.futureReports]
            futureListr = [(f'{(report.getTime()-gametime.time).days}',f'Day{"s" if (report.getTime()-gametime.time).days+1 > 1 else ""} Away') for report in self.selectedStock.priceEffects.futureReports]
            colors = [p3choice((200,0,0),(190,190,190),(190,0,0),(val.getTime()-gametime.time).days-25) for val in self.selectedStock.priceEffects.futureReports]
            drawLinedInfoBigColored(screen,(565,710),(330,280),futureListl,futureListr,45,25,colors)

            screen.blit(s_render("UPCOMING",50,(220,220,220)),(575,645))

            pastReportPer, perfReportPer = self.selectedStock.priceEffects.getLikelyHoods(gametime)
            # prediction = self.selectedStock.priceEffects.getQuarterlyLikelyhood(gametime)
    
            changeVals = lambda val : round(val,2) 
            data = [
                (changeVals(pastReportPer),(150,0,230)),
                (changeVals(perfReportPer),(255,128,0)),
                ((changeVals(pastReportPer)+changeVals(perfReportPer)),(140,140,140))
            ]

            self.reportBarGraph.updateValues([d[0] for d in data],[d[1] for d in data],["%"]*len(data))
            self.reportBarGraph.draw(screen,absoluteScale=100)

            pygame.draw.rect(screen, (150, 0, 230), pygame.Rect(945, 640, 140, 50), 0, 10)
            pygame.draw.rect(screen, (255, 128, 0), pygame.Rect(1097, 640, 140, 50), 0, 10)
            pygame.draw.rect(screen, (140, 140, 140), pygame.Rect(1250, 640, 140, 50), 0, 10)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(945, 640, 140, 50), 5, 10)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(1097, 640, 140, 50), 5, 10)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(1250, 640, 140, 50), 5, 10)

            drawCenterTxt(screen,"Past Reports",35,(230,230,230),(1013,651),centerY=False)
            drawCenterTxt(screen,"Performance",35,(230,230,230),(1165,651),centerY=False)
            drawCenterTxt(screen,"Prediction",35,(230,230,230),(1318,651),centerY=False)
        else:
            string = "To see upcoming reports and report likelihoods, go to the Mode Menu and enable 'Stock Reports'"
            for i,line in enumerate(separate_strings(string,3)):
                drawCenterTxt(screen,line,50,(220,220,220),(1007,690+(i*50)),centerY=False)

            result = drawClickableBoxWH(screen, (827, 870), (360,95), "Get Upgrade", 55, (0,0,0), (200,200,200),fill=True)
            if result:
                player.screenManager.setScreen("Mode")
                player.screenManager.screens['Mode'].career.menuSelect.setSelected(0)# sets the screen to Unlock rather than compare
                player.screenManager.screens['Mode'].career.modeSelection.setSelected("Stockbook")


        

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

    def drawCompanyInfo(self,screen:pygame.Surface,player):
        """Draws the company info for the stock on the right middle """

        
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

    def drawPurchase(self,screen:pygame.Surface,player,gametime):
        pygame.draw.rect(screen,(0,0,0),(780,770,640,190),width=5,border_radius=10)# Box for numPad
        if self.selectedStock.getValue() == 0:
            drawCenterTxt(screen,"This stock has no value",50,(220,220,220),(960,770),centerY=False)
            return
        self.numPad.draw(screen,(750,770),(700,200),"",player.cash//self.selectedStock.getValue())

        data = [("Price",f"${limit_digits(self.selectedStock.getValue(),20)}","x"),("Quantity",str(self.numPad.numstr),"x")]
        
        self.orderBox.loadData(self.numPad.numstr,f"${limit_digits(self.numPad.getValue()*self.selectedStock.getValue(),20)}",data)
        result = self.orderBox.draw(screen)
        if result:
            print('Buying',self.selectedStock.name,self.numPad.getValue())
            player.buyAsset(StockAsset(player,self.selectedStock,gametime.getTime(),self.selectedStock.price,self.numPad.getValue()))
            self.orderBox.reset()
            self.numPad.reset()

        pygame.draw.rect(screen,(0,0,0),(200,625,550,325),5,10)# border for the lined info
        
        maxQty = 0 if player.cash == 0 else int(self.selectedStock.getValue()//player.cash)
        infoList = [
            ("Price Per Share",f"${limit_digits(self.selectedStock.getValue(),12)}"),
            ("Max Quantity",f"{int(player.cash//self.selectedStock.getValue())} Share{'s' if maxQty != 1 else ''}"),
            ("Quantity Owned",f"{player.getStockQuantity(self.selectedStock)} Share{'s' if player.getStockQuantity(self.selectedStock) != 1 else ''}"),
        ]
        drawLinedInfo(screen,(205,625),(540,325),infoList,40,color=TXTCOLOR)
        
    def drawNews(self,screen:pygame.Surface,stockname:str,coords:tuple):
        """Draws the news for the stock on the right middle """
        pass

    def drawInDepthInfo(self,screen:pygame.Surface,gametime):
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

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, player,gametime):
        mousex, mousey = pygame.mouse.get_pos()

        # Draw the stock graph
        self.stockGraph.setStockObj(self.selectedStock)
        self.stockGraph.drawFull(screen, (190,100),(550,450),"StockBook Graph",True,"Normal")
       

        self.drawStockLatter(screen, player)
        # if drawClickableBox(screen,(879,420),"Create Order",95,(130,130,130),(0,170,0)):
        #     self.oScreenDisp = True 

        self.barSelection.draw(screen,self.middleDisplays,(195,560),(545,55),colors=[(19, 133, 100), (199, 114, 44), (196, 22, 62)],txtsize=35)

        self.drawInDepthInfo(screen,gametime)

        # match self.currentMDisp:
        match self.barSelection.getSelected():
            case "Info":
                self.drawCompanyInfo(screen,player)
                pass
            case "Purchase":
                self.drawPurchase(screen,player,gametime)
            case "News":
                # self.drawNews(screen,self.selectedStock.name,(190,100))
                pass
            case "Reports":
                self.drawQuarterlyReports(screen,gametime,player)
        
        if self.oScreenDisp:
            self.oScreenDisp = self.orderScreen.draw(screen,self.selectedStock,player,gametime,maxCoords=[1450,1500],minCoords=[190,-500])


