import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.Menu import Menu
import numpy as np
from Classes.imports.Bar import SliderBar
# from Classes.AssetTypes.StockAsset import StockAsset
from Classes.StockVisualizer import StockVisualizer
# from Classes.imports.OrderScreen import OrderScreen
from Classes.imports.Latterscroll import PortfolioLatter,LatterScroll
from Classes.Stock import Stock
from Classes.imports.PieChart import PieChart
from Classes.imports.BarGraph import BarGraph
from Classes.imports.SelectionBar import SelectionBar
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
        self.menudrawn = False
        self.stocklist = stocklist
        self.purchasetext = [fontlist[65].render(text, color)[0] for text,color in zip(['PURCHASE','PURCHASE','INSUFFICIENT'],[(0,150,0),(225,225,225),(150,0,0)])]
        self.quantitybar : SliderBar = SliderBar(50,[(150,150,150),(10,10,10)],barcolor=((20,130,20),(40,200,40)))
        self.stockGraph : StockVisualizer = StockVisualizer(gametime,stocklist[0],stocklist)
        self.stockLS : PortfolioLatter = PortfolioLatter()
        self.futureRepLS, self.pastRepLS = LatterScroll(), LatterScroll()
        self.orderScreen = orderScreen
        self.middleDisplays = ["Info","Reports","News"]
        self.currentMDisp = self.middleDisplays[0]
        self.oScreenDisp = False
        self.reportPieChart : PieChart = PieChart(125,(940,700))
        self.reportBarGraph : BarGraph = BarGraph("Report Likelyhood",(450,190),(940,740))
        self.barSelection : SelectionBar = SelectionBar()
        

    def createDescriptions(self,stocknames): 
        with open(r'Assets\newstockdes.txt','r') as descriptions:
            filecontents = descriptions.readlines()
            for i,line in enumerate(filecontents):
                for stockname in stocknames:
                    if line.replace('\n','') == stockname:
                        self.stocktext[stockname].append(filecontents[i+1].replace('\n',''))# Full stock name Ex. "Kyronix Solutions Inc. (KSTON)"
                        seperatatedstrings = separate_strings((filecontents[i+2].replace('\n','')),5)
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
        # screen.blit(s_render("Quarterly Reports",80,(220,220,220)),(760,160))

        # screen.blit(s_render("Chance Of Hitting Expectations",50,(220,220,220)),(760,235))

        # # -------------Drawing the things to calculate the likelyhood of the quarterly report----------------
        # perfIndicatorss = ["Past Reports","Stock Performance","News"]
        # numRanges = [18,88,0]
        # vals = [
        #     self.selectedStock.priceEffects.getReportLikelyhood(),
        #     self.selectedStock.priceEffects.getPastPerfLikelyhood(gametime),0]
        # for i in range(3):
        #     x,y = 760+(i*226),300
        #     w,h = 200,140
            
        #     if numRanges[i] == 0:
        #         color = (60,60,60)
        #     elif (p:=(vals[i])/numRanges[i]) >= 0.5:
        #         color = (0,int(225*p),0)
        #     else:# if p is realy low
        #         color = (int(-225*p)+225,0,0)

        #     pygame.draw.rect(screen,color,(x,y,w,h),border_radius=10)
        #     pygame.draw.rect(screen,(0,0,0),(x,y,w,h),5,10)
            
        #     descripttxt = s_render(perfIndicators[i],30,(0,0,0))
        #     screen.blit(descripttxt,(x+w/2-descripttxt.get_width()/2,y+h-descripttxt.get_height()-10))
        #     valTxt = s_render(f"{limit_digits(vals[i],15)}",65,(0,0,0))
        #     screen.blit(valTxt,(x+((w-valTxt.get_width())/2),y+((h-valTxt.get_height())/2)))
            
        #     if i != 2:# if its not the last one
        #         screen.blit(s_render("+",70,(220,220,220)),(x+w+5,y+h/2-15))

        # pLikelyhood = self.selectedStock.priceEffects.getQuarterlyLikelyhood(gametime)

        # if (p:=(pLikelyhood/100)) >= 0.5:
        #     color = (0,int(225*p),0)
        # else:# if p is realy low
        #     color = (int(-225*p)+225,0,0)

        # chanceTxt = s_render(f"= {limit_digits(pLikelyhood,15)} %",80,color)
        # x = 760+340-chanceTxt.get_width()/2
        # pygame.draw.rect(screen,(30,30,30),(x-25,460,chanceTxt.get_width()+50,80),border_radius=10)
        # pygame.draw.rect(screen,(0,0,0),(x-25,460,chanceTxt.get_width()+50,80),5,10)
        # screen.blit(chanceTxt,(760+340-chanceTxt.get_width()/2,475))

        # -----------------Drawing the future and past reports----------------
        getDate = lambda time : f"{time.month}/{time.day}/{time.year}"

        # futureDict = {f"Q{report[1]} {getDate(report[0])}":f'{(report[0]-gametime.time).days+1} Day{"s" if (report[0]-gametime.time).days+1 > 1 else ""} Away' for report in self.selectedStock.priceEffects.futureReports}
        # pastDict = {f'Q{report[1]} {getDate(report[0])}':f' {"Beat" if report[2] > 0 else "Miss"} {limit_digits(report[2],15)}%' for report in self.selectedStock.priceEffects.pastReports[:4]}
        
        pygame.draw.rect(screen,(0,0,0),(190,690,350,275),5,10)
        pygame.draw.rect(screen,(0,0,0),(555,690,350,275),5,10)
        
        pastListl = [(f'Q{report[1]}',f'{getDate(report[0])}') for report in self.selectedStock.priceEffects.pastReports[:4]]
        pastListr =[(f'{"Beat" if report[2] > 0 else "Miss"}', f'{"+" if report[2] > 0 else ""}{limit_digits(report[2],15)}%') for report in self.selectedStock.priceEffects.pastReports[:4]]
        colors = [(200,0,0) if val[0] == "Miss" else (0,190,0) for val in pastListr]
        # print('dicts are',pastListl,pastListr)
        drawLinedInfoBigColored(screen,(200,710),(330,280),pastListl,pastListr,45,25,colors)

        # drawLinedInfo(screen,(200,710),(330,280),pastDict,30,TXTCOLOR)
        # drawLinedInfo(screen,(760,640),(330,280),pastDict,30,TXTCOLOR)
        # drawLinedInfo(screen,(1100,640),(330,280),futureDict,30,TXTCOLOR)
        futureListl = [(f'Q{report[1]}',f'{getDate(report[0])}') for report in self.selectedStock.priceEffects.futureReports]
        futureListr = [(f'{(report[0]-gametime.time).days}',f'Day{"s" if (report[0]-gametime.time).days+1 > 1 else ""} Away') for report in self.selectedStock.priceEffects.futureReports]
        colors = [p3choice((200,0,0),(190,190,190),(190,0,0),(val[0]-gametime.time).days-25) for val in self.selectedStock.priceEffects.futureReports]
        drawLinedInfoBigColored(screen,(565,710),(330,280),futureListl,futureListr,45,25,colors)
        # drawLinedInfo(screen,(540,710),(330,280),futureDict,30,TXTCOLOR)
        screen.blit(s_render("PAST",50,(220,220,220)),(205,645))
        screen.blit(s_render("UPCOMING",50,(220,220,220)),(575,645))
        # screen.blit(s_render("EXPERT PREDICTION",50,(220,220,220)),(930,645))

        pastReportPer, perfReportPer = self.selectedStock.priceEffects.getLikelyHoods(gametime)
        prediction = self.selectedStock.priceEffects.getQuarterlyLikelyhood(gametime)
        x,y = 920,690

        # pygame.draw.rect(screen,(0,0,175,150),(920,690,350,50),border_radius=10)
        
        # pastReportTxt = s_render(f"Past Reports",40,(220,220,220))
        # perfReportTxt = s_render(f"Stock Performance",40,(220,220,220))
        # predictionTxt = s_render(f"{round(prediction/10,2)}",40,(220,220,220))
        # pastReportVal  = s_render(f"{round(pastReportPer/10,2)}",60,(220,220,220))
        # perfReportVal = s_render(f"{round(perfReportPer/10,2)}",60,(220,220,220))
        # pygame.draw.rect(screen,(0,0,0),(920,690,525,75),5,10)
        # screen.blit(pastReportTxt,(x+10,y+15))
        # screen.blit(pastReportVal,(x+515-pastReportVal.get_width(),y+15))
        # pygame.draw.rect(screen,(0,0,0),(920,780,525,75),5,10)
        # screen.blit(perfReportTxt,(x+10,y+105))
        # screen.blit(perfReportVal,(x+515-perfReportVal.get_width(),y+105))
        # pygame.draw.rect(screen,(0,0,0),(920,870,525,75),5,10)
        # screen.blit(s_render(f"Prediction",40,(220,220,220)),(930,900))
        # screen.blit(predictionTxt,(x+515-predictionTxt.get_width(),y+195))

        # strings = ["Past Reports","Stock Performance","Prediction"]
        # values = [f"{round(pastReportPer/10,2)}/1.2",f"{round(perfReportPer/10,2)}/8.8",f"{round(prediction/10,2)}/10"]
        # info = [(string,value) for string,value in zip(strings,values)]
        # pygame.draw.rect(screen,(0,0,0),(910,710,545,290),5,10)
        # drawLinedInfo(screen,(920,730),(525,250),info,50,TXTCOLOR)
        changeVals = lambda val : round(val,2) 
        data = [
            (changeVals(pastReportPer),(150,0,230)),
            (changeVals(perfReportPer),(255,128,0)),
            ((changeVals(pastReportPer)+changeVals(perfReportPer)),(140,140,140))
        ]

        self.reportBarGraph.updateValues([d[0] for d in data],[d[1] for d in data],["%"]*len(data))
        self.reportBarGraph.draw(screen,absoluteScale=100)
        # ogtext = s_render("Original", 55, (190, 190, 190))
        # screen.blit(ogtext, (885, 350))
        # pygame.draw.rect(screen, (60, 60, 60), pygame.Rect(900+ogtext.get_width(), 350, 35, 35), 0, 10)

        # screen.blit(s_render("Current", 55, asset.color), (1140, 350))
        # pygame.draw.rect(screen, asset.color, pygame.Rect(1155+ogtext.get_width(), 350, 35, 35), 0, 10)
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


        

        
        
        # self.reportPieChart.updateData(data)
        # self.reportPieChart.draw(screen)



        # screen.blit(s_render(f"Past Reports: {limit_digits(pastReportPer,15)}%",40,(220,220,220)),(930,700))


        

        # screen.blit(s_render(str(self.selectedStock.priceEffects.getQuarterlyLikelyhood(gametime)),40,(220,220,220)),(1110,100))
        
        # futureReports - [time,quarter] PastReports - [performance,time,quarter]
        # fReports,pReports = self.selectedStock.priceEffects.futureReports,self.selectedStock.priceEffects.pastReports
        # getTxtFuture = lambda report : [f"Q{report[1]}",f'{(report[0]-gametime.time).days} Days Away',"UPCOMING"]# returns the text for the stock
        
        # getTxtPast = lambda report : [f'Q{report[2]}',f'{getDate(report[1])}',f'{"Beat" if report[0] > 0 else "Miss"} {limit_digits(report[0],15)}%']
        
        # futureTxts = [getTxtFuture(report) for report in fReports]
        # pastTxts = [getTxtPast(report) for report in pReports]
        # # print(len(futureTxts),len(pastTxts))
        # ftextinfo,ptextinfo = [],[]# stores the text info for the latter scroll [text,fontsize,color]
        # fcoords,pcoords = [[(20,10),(22,60)] for i in range(len(futureTxts))],[[(20,10),(22,60)] for i in range(len(pastTxts))]

        # for i,ftext in enumerate(futureTxts):
        #     fpolytexts = []
        #     fpolytexts.extend([[ftext[0],55,(0,0,0)],[ftext[1],35,(190,190,190)],[ftext[2],50,(190,0,0) if ftext[2][:4] == "Miss" else (0,190,0)]])
        #     ftextinfo.append(fpolytexts)
        #     fcoords[i].append(((ftext[1],40),30))

        # for i,ptext in enumerate(pastTxts):
        #     ppolytexts = []
        #     ppolytexts.extend([[ptext[0],55,(0,0,0)],[ptext[1],35,(190,190,190)],[ptext[2],50,(190,0,0) if ptext[2][:4] == "Miss" else (0,190,0)]])# appends the text info for the asset
        #     ptextinfo.append(ppolytexts)
        #     pcoords[i].append(((ptext[1],40),30))

        # self.futureRepLS.storetextinfo(ftextinfo); self.futureRepLS.set_textcoords(fcoords)# stores the text info and the coords for the latter scroll
        # self.pastRepLS.storetextinfo(ptextinfo); self.pastRepLS.set_textcoords(pcoords)# stores the text info and the coords for the latter scroll
        
        # fommitted = self.futureRepLS.store_rendercoords((1100, 160), (350,425),110,0,0,updatefreq=60)
        # pommitted = self.pastRepLS.store_rendercoords((750, 160), (350,425),110,0,0,updatefreq=60)
        # # self.selectedStock = self.selectedStock if self.selectedStock in self.stocklist else None# Ensuring that the selected stock is in the stocklist
        # # print(len(self.pastRepLS.textcoords))
        # # selectedindex = None if self.selectedStock == None else self.stocklist.index(self.selectedStock)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)
        # newselected = self.futureRepLS.draw_polys(screen, (1100, 160), (350,425), mousebuttons, None, False)# draws the latter scroll and returns the selected asset
        # newselected = self.pastRepLS.draw_polys(screen, (750, 160), (350,425), mousebuttons, None, False)# draws the latter scroll and returns the selected asset
        
        # self.selectedStock = self.selectedStock if newselected == None else self.stocklist[newselected]# Changes selected stock if the new selected has something
    def drawCompanyInfo(self,screen:pygame.Surface,stockname:str,coords:tuple):
        """Draws the company info for the stock on the right middle """
        # def pil_to_pygame(image):
        #     """Convert a PIL Image to a Pygame Surface."""
        #     return pygame.image.fromstring(image.tobytes(), image.size, image.mode)
        
        
        # Draw the stock name & description
        
        pygame.draw.rect(screen,(20,20,20),(200,625,550,325),border_radius=10)
        pygame.draw.rect(screen,(0,0,0),(200,625,550,325),5,10)
        screen.blit(s_render(self.selectedStock.name,90,self.selectedStock.color),(210,635))# blits the stock name to the screen
        for i,line in enumerate(self.stocktext[self.selectedStock.name]):
            x,y = (210 if i != 0 else self.renderedstocknames[self.selectedStock.name].get_width()+215),(725+((i-1)*40) if i != 0 else 650)
            screen.blit(line,(x,y))
        # Draw stuff about CEO
        ceo = self.selectedStock.ceo
        xCeo,yCeo = 1165,620
        wCeo,hCeo = 290,330
        
        ceoInfo = s_render("CEO",50,(220,220,220))
        screen.blit(ceoInfo,(xCeo+wCeo/2-ceoInfo.get_width()/2,yCeo+10))
        # screen.blit(s_render("CEO INFO",50,(220,220,220)),(1175,630))
        pygame.draw.rect(screen,(0,0,0),(xCeo+wCeo/2-118/2,yCeo+55,128,110),5)# Box for the CEO image
        # pygame.draw.rect(screen,(0,0,0),(1175,670,128,110),5)# Box for the CEO image
        screen.blit(ceo.getImageSize(118,100),(xCeo+(wCeo/2)-(118/2)+5,yCeo+60))

        ceoName = s_render(ceo.name,50,(220,220,220))
        screen.blit(ceoName,(xCeo+wCeo/2-ceoName.get_width()/2,yCeo+170))

        ceoAge = s_render(f"{ceo.age} Years Old",40,(220,220,220))
        screen.blit(ceoAge,(xCeo+wCeo/2-ceoAge.get_width()/2,yCeo+210))
        # screen.blit(s_render(infoListR.name,50,(220,220,220)),(1175,785))
        # screen.blit(s_render(f"{infoListR.age} Years Old",40,(220,220,220)),(1200,825))
        # print(ceo.slogan.split(' '),int(len(ceo.slogan.split(' '))/4))
        # numslines = int(len(ceo.slogan.split(' '))/4)+1
        numslines = int(len(ceo.slogan)/24)+1
        # print(numslines)
        for i,line in enumerate(ceo.getSloganLines(numslines)):
            ex1 = '"' if i == 0 else ''
            ex2 = '"' if i == numslines-1 else ''
            txt = s_render(ex1+line+ex2,30,(220,220,220))
            screen.blit(txt,(xCeo+(wCeo/2)-(txt.get_width()/2),yCeo+255+(i*35)))
            # screen.blit(s_render(ex1+line+ex2,30,(220,220,220)),(1180+(i*10),875+(i*35)))
        pygame.draw.rect(screen,(0,0,0),(1165,620,290,255+35*numslines),5,10)
        
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
            f"{limit_digits(self.selectedStock.dividend,12)}%",
            f"{limit_digits(self.selectedStock.getVolatility()*100,12)}%"
        ]
        # info = {key:value for key,value in zip(keys,values)}
        info = [(string,value) for string,value in zip(strings,values)]
        drawLinedInfo(screen,(750,120),(700,300),info,40,TXTCOLOR)

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player,gametime):
        mousex, mousey = pygame.mouse.get_pos()

        # bmouse = mousebuttons# click still needs to go to the order screen
        # if self.oScreenDisp:# Can't click anything if the order screen is displayed
        #     mousebuttons = 0

        # Draw the stock graph
        self.stockGraph.setStockObj(self.selectedStock)
        self.stockGraph.drawFull(screen, (190,100),(550,450),"StockBook Graph",True,"Normal")
       

        self.drawStockLatter(screen, mousebuttons, player)
        if drawClickableBox(screen,(879,420),"Create Order",95,(130,130,130),(0,170,0),mousebuttons):
            self.oScreenDisp = True 

        self.barSelection.draw(screen,self.middleDisplays,(195,560),(545,45),txtsize=35)
        # result = checkboxOptions(screen,self.middleDisplays,self.currentMDisp,(190,550),(680,50),mousebuttons,txtSize=35)
        # self.currentMDisp = result[0] if result else self.currentMDisp

        self.drawBuySellInfo(screen,gametime)

        # match self.currentMDisp:
        match self.barSelection.getSelected():
            case "Info":
                self.drawCompanyInfo(screen,self.selectedStock.name,(190,100))
                pass
            case "News":
                # self.drawNews(screen,self.selectedStock.name,(190,100))
                pass
            case "Reports":
                self.drawQuarterlyReports(screen,gametime,mousebuttons)
        
        
        
        # print(self.selectedStock.getPointDate(datetime.datetime.strptime(f"04/19/2029 9:30:00 AM", "%m/%d/%Y %I:%M:%S %p"),gametime))
        
        if self.oScreenDisp:
            self.oScreenDisp = self.orderScreen.draw(screen,self.selectedStock,mousebuttons,player,gametime)


