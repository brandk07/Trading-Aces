import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.Bar import TimeBar
# from Classes.imports.stockeventspos import StockEvents
from Classes.imports.UIElements.Latterscroll import LatterScroll
from Classes.imports.Newsbar import News
from Classes.BigClasses.Stock import Stock
from Classes.imports.StockVisualizer import StockVisualizer
from Classes.imports.UIElements.PieChart import PieChart
from Classes.imports.Gametime import GameTime

class HomeScreen:
    def __init__(self,stocklist:list,gametime,tmarket,player) -> None:
                
        self.newsobj = News(stocklist)
        self.speedBar : TimeBar = gametime.speedBar
        self.pieChart = PieChart((945,165),(520,530))
        self.totalMarketGraph = StockVisualizer(gametime,tmarket,[tmarket,player]+stocklist)


    def draw_time(self,screen,gametime):
        timeStrs = gametime.getTimeStrings()# year,month,day,minute,dayname,monthname,am/pm
        
        timeStr = f"{timeStrs['time']+' '+timeStrs['ampm']}"
        drawCenterTxt(screen,timeStr,105,(200,200,200),(260,20),centerX=False,centerY=False)
        dateStr = f"{timeStrs['dayname']}, {timeStrs['monthname']} {timeStrs['day']}, {timeStrs['year']}"
        drawCenterTxt(screen,dateStr,50,(200,200,200),(260,105),centerX=False,centerY=False)
        
    def marketStatus(self,screen,gametime):
        color = (0,150,0) if gametime.isOpen()[0] else (150,0,0)
        # screen.blit(s_render(f"MARKET {'OPEN' if gametime.isOpen()[0] else 'CLOSED'}",115 if gametime.isOpen()[0] else 95,color),(725,20))
        txt = f"MARKET {'OPEN' if gametime.isOpen()[0] else 'CLOSED'}"
        drawCenterTxt(screen,txt,115,color,(1515,35),centerY=False)
    
    def drawPieChart(self,screen,player,stocklist):
        assets = player.getAssets()
        values = [[asset.getValue(),asset.name,asset.color] for asset in assets]
        values.append([player.cash, "Cash",player.color])

        self.pieChart.updateData(values)
        self.pieChart.draw(screen,"Portfolio Breakdown")

    def draw_home(self,screen:pygame.Surface,stocklist:list,gametime,player):
        """Draws the home screen"""
        timebarpoints = [(200,10),(250,150),(1910,150),(1860,10)]
        gfxdraw.filled_polygon(screen,timebarpoints,(10,10,10,225))# time etc
        pygame.draw.polygon(screen,(0,0,0),timebarpoints,5)# time etc
        self.draw_time(screen,gametime)


        gfxdraw.filled_polygon(screen,[(250,705),(270,983),(1470,983),(1450,705)],(25,25,25,175))# the News bar at the bottom
        pygame.draw.polygon(screen,(0,0,0),[(250,705),(270,983),(1470,983),(1450,705)],5)# the News bar at the bottom Outline

        gfxdraw.filled_polygon(screen,[(270,983),(1470,983),(1475,1050),(275,1050)],(40,40,40,175))# the News bar at the botto
        pygame.draw.polygon(screen,(0,0,0),[(270,983),(1470,983),(1475,1050),(275,1050)],5)# the News bar at the bottom Outline
        
        # pygame.draw.line(screen,(0,0,0),(270,985),(1469,985),5)# line between the news bar and the stock bar

        self.drawPieChart(screen,player,stocklist)
    

    def draw(self,screen,stocklist,player,gametime):                    

        self.draw_home(screen,stocklist,gametime,player)            
        self.marketStatus(screen,gametime)
        self.totalMarketGraph.drawFull(screen,(250,160),(680,540),"Home Total Market",True,"hoverName")
        self.newsobj.draw(screen,gametime)
        
        screen.blit(s_render(f'GAMEPLAY SPEED',60,(247, 223, 0)),(830,20))

        # result = self.speedBar.draw_bar(screen,[740,75],[450,65],'horizontal',reversedscroll=True,text=gametime.skipText())
        self.speedBar.drawBar(screen,(747,65))

        self.gameplay_speed = self.speedBar.getValue()
    
