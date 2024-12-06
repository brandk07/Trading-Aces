
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from Classes.imports.Gametime import Gametime

import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.Bar import SliderBar
# from Classes.imports.stockeventspos import StockEvents
from Classes.imports.UIElements.Latterscroll import LatterScroll
from Classes.imports.Newsbar import News
from Classes.BigClasses.Stock import Stock
from Classes.imports.StockVisualizer import StockVisualizer
from Classes.imports.UIElements.PieChart import PieChart
from Classes.imports.Gametime import GameTime

class HomeScreen:
    def __init__(self,stocklist:list,gametime,tmarket,player) -> None:
        
        self.icon = pygame.image.load(r'Assets\homescreen icon.png').convert_alpha()
        self.icon = pygame.transform.smoothscale(self.icon,(140,100))
        
        self.newsobj = News(stocklist)
        self.speedBar : SliderBar = gametime.speedBar
        self.pieChart = PieChart((945,165),(520,530))
        self.totalMarketGraph = StockVisualizer(gametime,tmarket,[tmarket,player])


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
    
    def drawPieChart(self,screen,player,stocklist,mousebuttons):
        assets = player.getAssets()
        values = [[asset.getValue(),asset.name,asset.color] for asset in assets]
        values.append([player.cash, "Cash",player.color])

        self.pieChart.updateData(values)
        self.pieChart.draw(screen,"Portfolio Breakdown",mousebuttons)

    def draw_home(self,screen:pygame.Surface,stocklist:list,gametime,player,mousebuttons):
        """Draws the home screen"""
        timebarpoints = [(200,10),(250,150),(1910,150),(1860,10)]
        gfxdraw.filled_polygon(screen,timebarpoints,(10,10,10,225))# time etc
        pygame.draw.polygon(screen,(0,0,0),timebarpoints,5)# time etc
        self.draw_time(screen,gametime)


        gfxdraw.filled_polygon(screen,[(250,705),(275,1050),(1475,1050),(1450,705)],(10,10,10,175))# the News bar at the bottom
        pygame.draw.polygon(screen,(0,0,0),[(250,705),(275,1050),(1475,1050),(1450,705)],5)# the News bar at the bottom Outline
        
        pygame.draw.line(screen,(0,0,0),(270,985),(1469,985),5)# line between the news bar and the stock bar

        self.drawPieChart(screen,player,stocklist,mousebuttons)
    

    def draw(self,screen,mousebuttons,stocklist,player,gametime):                    

        self.draw_home(screen,stocklist,gametime,player,mousebuttons)            
        self.marketStatus(screen,gametime)
        self.totalMarketGraph.drawFull(screen,(250,160),(680,540),"Home Total Market",True,"hoverName")
        self.newsobj.draw(screen,gametime)
        
        screen.blit(s_render(f'GAMEPLAY SPEED',60,(247, 223, 0)),(830,20))

        self.gameplay_speed = self.speedBar.draw_bar(screen,[740,75],[450,65],'horizontal',reversedscroll=True,text=gametime.skipText())


# [20,60] [60,20]
# [700,1000] [1000,650]

# class UIControls():
#     def __init__(self,stocklist,gamespeed,gametime,tmarket,player) -> None:
#         self.gameplay_speed = 0
#         # self.stockevent = StockEvents()# the stock events
#         # self.bar = SliderBar(gamespeed,[(247, 223, 0),(110,110,110)],barcolor=[(255,255,255),(200,200,200)])# the bar for the gameplay speed
        
#         self.latterscroll = LatterScroll()
#         self.newsobj = News(stocklist)

#         # for i in range(10):
#         #     for stock in stocklist:
#         #         self.newsobj.addStockNews(stock.name)
#         self.totalMarketGraph = StockVisualizer(gametime,tmarket,[tmarket,player])

#         self.view = "home"# home or stock
#         # self.accbar_middle = "move"# move, stock, pie
#         # self.accbar_right = "topAsset"# topAsset, transactions, loans
#         self.pieChart = PieChart((945,165),(520,540))
#         self.graphscroll = 0
#         self.namerenders = [fontlist[30].render(stock.name,stock.color)[0] for stock in stocklist]# [red,green]
#         self.weeknames = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
#         self.weekdaystext = {weekday:fontlist[95].render(weekday,(255,255,255))[0] for weekday in self.weeknames}
#         # self.namerenders = [[fontlist[30].render(stock.name,(200,0,0))[0],fontlist[30].render(stock.name,(0,200,0))[0]] for stock in stocklist]# [red,green]

#         # get 
#         self.get_percent = lambda stock : round(((stock.graphs["1D"][-1]/stock.graphs["1D"][0])-1)*100,2)
#         self.get_listpercents = lambda xlist : [self.get_percent(stock) for stock in xlist]
#         self.percentchanges = self.get_listpercents(stocklist)
#         self.totalperecent = lambda xlist : sum([self.get_percent(stock) for stock in xlist])
#         # for pie chart
#         self.stockbarsurf = pygame.Surface((1200,80))
        
        
        
#     def drawIcon(self, screen: pygame.Surface,mousebuttons) -> bool:
#         """Draws the home/stock icon in the top left corner, returns True if the icon is clicked"""
#         # Draw the triangles to form a square in the top left corner
#         hometri = [(25, 10), (25, 160), (175, 10)]
#         stockstri = [(175, 10), (175, 160), (25, 160)]

#         # Check if the mouse is clicked and hovering over the triangles
#         mouse_pos = pygame.mouse.get_pos()
#         home_color = (0, 120, 0) if self.view == "home" else (20,20,20)
#         stocks_color = (120, 0, 0) if self.view == "stock" else (20,20,20)

#         # Check if the mouse is hovering over the triangles
#         if point_in_triangle(mouse_pos, hometri):
#             home_color = (0, 170, 0)
#             stocks_color = (80, 0, 0) if stocks_color == (120, 0, 0) else (20,20,20)
#             if mousebuttons == 1:
#                 self.view = "home"
#                 soundEffects['generalClick'].play()
#                 return True

#         if point_in_triangle(mouse_pos, stockstri):
#             stocks_color = (170, 0, 0)
#             home_color = (0, 120, 0) if home_color == (0, 170, 0) else (20,20,20)
            
#             if mousebuttons == 1:
#                 self.view = "stock"
#                 soundEffects['generalClick'].play()
#                 return True

#         # Draw the triangles
#         pygame.draw.polygon(screen, home_color, [(x, y) for x, y in hometri])
#         pygame.draw.polygon(screen, stocks_color, [(x, y) for x, y in stockstri])

#         # Draw the outline for the triangles
#         pygame.draw.polygon(screen, (0, 0, 0), [(x, y) for x, y in hometri], 4)
#         pygame.draw.polygon(screen, (0, 0, 0), [(x, y) for x, y in stockstri], 4)

#         # Draw the "Home" and "Stocks" text in the triangles
#         home = fontlist[50].render('Home', (255, 255, 255))[0]
#         screen.blit(home, (90 - home.get_width() / 2 - 15, 45 - home.get_height() / 2))
#         stocks = fontlist[50].render('Stocks', (255, 255, 255))[0]
#         screen.blit(stocks, (140 - stocks.get_width() / 2 - 15, 95 + stocks.get_height() / 2))
#         return False

#     def draw_stockbar(self,screen:pygame.Surface,stocklist:list,coords:list=[250,710],wh=[1200,80]):
#         """Draws a bar that scrolls across the screen, displaying the stock prices, maxwidth is 1710"""

#         dx,dy = coords
#         if wh[1] > 1710: wh[1] = 1710
#         if self.stockbarsurf.get_width() != wh[0] or self.stockbarsurf.get_height() != wh[1]:
#             self.stockbarsurf = pygame.Surface(wh).convert_alpha()
        
#         self.graphscroll += 1*(self.gameplay_speed/self.bar.maxvalue)+1# the speed of the stock graph 
#         self.percentchanges = self.get_listpercents(stocklist)
#         if self.graphscroll > len(stocklist)*190: self.graphscroll = 0
#         for i,stock in enumerate(stocklist):# draws the stock graph bar
#             x = int(0-self.graphscroll+(i*190))
#             if x < -120:
#                 x += len(stocklist)*190
#             if x < wh[0]+100:# if the stock is on the screen
                
#                 color = (0,200,0) if self.percentchanges[i] >= 0 else (200,0,0)

#                 stocklist[i].baredraw(self.stockbarsurf,(x,0),(100,wh[1]),MINRANGE)# draws the graph
#                 self.stockbarsurf.blit(self.namerenders[i],(x-70,10))# draws the name of the stock
#                 ptext = fontlist[28].render(limit_digits(stock.price,9),color)[0]# renders the price of the stock
#                 self.stockbarsurf.blit(ptext,(x-42-(ptext.get_width()/2),50))# draws the price of the stock

#         pygame.draw.rect(self.stockbarsurf,(0,0,0),pygame.Rect(0,0,wh[0],wh[1]),5)# draws the outline of the stock graph bar
#         screen.blit(self.stockbarsurf,(dx,dy))# draw the stock graph bar to the screen
#         self.stockbarsurf.fill((30,30,30))# fill the stock graph bar with a dark grey color
        
        
#     def draw_time(self,screen,gametime):
#         timeStrs = gametime.getTimeStrings()# year,month,day,minute,dayname,monthname,am/pm
        
#         timeStr = f"{timeStrs['time']+' '+timeStrs['ampm']}"
#         drawCenterTxt(screen,timeStr,105,(200,200,200),(260,20),centerX=False,centerY=False)
#         dateStr = f"{timeStrs['dayname']}, {timeStrs['monthname']} {timeStrs['day']}, {timeStrs['year']}"
#         drawCenterTxt(screen,dateStr,50,(200,200,200),(260,105),centerX=False,centerY=False)

        

#     def marketStatus(self,screen,gametime):
#         color = (0,150,0) if gametime.isOpen()[0] else (150,0,0)
#         # screen.blit(s_render(f"MARKET {'OPEN' if gametime.isOpen()[0] else 'CLOSED'}",115 if gametime.isOpen()[0] else 95,color),(725,20))
#         txt = f"MARKET {'OPEN' if gametime.isOpen()[0] else 'CLOSED'}"
#         drawCenterTxt(screen,txt,115,color,(1515,35),centerY=False)
#         # if not gametime.isOpen()[0]: 
#             # render = s_render(f"{gametime.isOpen()[1]}",65,color)
#             # screen.blit(render,(890-(render.get_width()/2),95))
#             # drawCenterTxt(screen,f"{gametime.isOpen()[1]}",65,color,(1515,35),centerY=False)
            
#     def drawPieChart(self,screen,player,stocklist,mousebuttons):
#         # values = [(stock.getValue(),stock.name) for stock in player.stocks]
#         # names = set([stock.name for stock in player.stocks])

#         # values = [[sum([v[0] for v in values if v[1] == name]), name, stocklist[[s.name for s in stocklist].index(name)].color] for name in names]
#         # values.append([player.cash, "Cash",player.color])
#         # for option in player.options:
#         #     values.append([option.getValue(),option.name,option.color])

#         # draw_pie_chart(screen, values, 190, (935, 235))
#         assets = player.getAssets()
#         values = [[asset.getValue(),asset.name,asset.color] for asset in assets]
#         values.append([player.cash, "Cash",player.color])

#         self.pieChart.updateData(values)
#         self.pieChart.draw(screen,"Portfolio Breakdown",mousebuttons)

#     def draw_home(self,screen:pygame.Surface,stocklist:list,gametime,player,mousebuttons):
#         """Draws the home screen"""
#         timebarpoints = [(200,10),(250,150),(1910,150),(1860,10)]
#         gfxdraw.filled_polygon(screen,timebarpoints,(10,10,10,225))# time etc
#         pygame.draw.polygon(screen,(0,0,0),timebarpoints,5)# time etc
#         # screen.blit(self.weekdaystext[gametime.get_day_name()],(265,20))
#         self.draw_time(screen,gametime)


#         gfxdraw.filled_polygon(screen,[(250,705),(275,1050),(1475,1050),(1450,705)],(10,10,10,175))# the News bar at the bottom
#         pygame.draw.polygon(screen,(0,0,0),[(250,705),(275,1050),(1475,1050),(1450,705)],5)# the News bar at the bottom Outline
        
#         pygame.draw.line(screen,(0,0,0),(270,985),(1469,985),5)# line between the news bar and the stock bar

#         self.drawPieChart(screen,player,stocklist,mousebuttons)

#         # self.draw_stockbar(screen,stocklist)# draws the stock graph bar
#         # self.draw_accbar_middle(screen,stocklist,mousebuttons,player)# draws the stock events (On the right of the portfolio)
#         # self.draw_accbar_right(screen,stocklist,player,mousebuttons)# draws the stock events (On the very right of the screen)
#         # self.newsobj.draw(screen)
#     # def drawBigMessage(self,screen,mousebuttons,player):
#     #     if bigMessageList:# if there is a big message
#     #         bigMessageList[0].draw(screen,self,mousebuttons,player)

#     def draw_ui(self,screen,stockgraphmanager,stocklist,player,gametime,mousebuttons,menulist,tmarket):
#         if self.drawIcon(screen,mousebuttons):
#             for i in range(len(menulist)):menulist[i].menudrawn = False
        

#         if not any(menu.menudrawn for menu in menulist):# if any of the menus are drawn, then don't draw
            
#             if self.view == "home":
#                 mousex,mousey = pygame.mouse.get_pos()
                
#                 self.draw_home(screen,stocklist,gametime,player,mousebuttons)            
#                 self.marketStatus(screen,gametime)
#                 # player.draw(screen,player,(250,160),(680,540),mousebuttons,stocklist,True)
#                 # tmarket.draw(screen,(250,160),(680,540),mousebuttons,gametime)
#                 # tmarket.drawFull(screen,(250,160),(680,540),"Home Total Market",True,"Normal")
#                 self.totalMarketGraph.drawFull(screen,(250,160),(680,540),"Home Total Market",True,"hoverName")
#                 # self.gameplay_speed = self.bar.draw_bar(screen,[1500,650],[120,380],'vertical')
#                 self.newsobj.draw(screen,gametime)
                
#                 screen.blit(s_render(f'GAMEPLAY SPEED',60,(247, 223, 0)),(830,20))

#                 self.gameplay_speed = self.bar.draw_bar(screen,[740,75],[450,65],'horizontal',reversedscroll=True,text=gametime.skipText())


#             # elif self.view == "stock":
#             #     stockgraphmanager.draw_graphs(screen,stocklist,player,mousebuttons,gametime)
#             #     # player.draw(screen,player,(1920,0),(1600,400),stocklist,mousebuttons)
#             #     self.gameplay_speed = self.bar.draw_bar(screen,[1620,575],[125,400],'vertical',text=gametime.skipText())
    
