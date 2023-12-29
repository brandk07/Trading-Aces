import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.Bar import SliderBar
from Classes.imports.stockeventspos import StockEvents
from Classes.imports.Newsbar import News

# [20,60] [60,20]
# [700,1000] [1000,650]

class UI_Controls():
    def __init__(self,windowoffset:list,stocklist) -> None:
        self.gameplay_speed = 0
        self.stockevent = StockEvents()# the stock events
        self.bar = SliderBar(windowoffset,100,[(255,0,0),(110,110,110)])# the bar for the gameplay speed
        self.newsobj = News()
        for i in range(10):
            for stock in stocklist:
                self.newsobj.addStockNews(stock.name)

        # self.view = "stock"# homeview or stockview
        self.view = "stock"# homeview or stock
        self.graphscroll = 0
        self.namerenders = [[fontlist[30].render(stock.name,(200,0,0))[0],fontlist[30].render(stock.name,(0,200,0))[0]] for stock in stocklist]# [red,green]

        # get 
        self.get_percent = lambda stock : round(((stock.graphrangelists[stock.graphrange][-1]/stock.graphrangelists[stock.graphrange][0])-1)*100,2)
        self.get_listpercents = lambda xlist : [self.get_percent(stock) for stock in xlist]
        self.percentchanges = self.get_listpercents(stocklist)
        self.totalperecent = lambda xlist : sum([self.get_percent(stock) for stock in xlist])
        # for pie chart
        radius = 175; backsurface = pygame.Surface((radius * 2 + 10, radius * 2 + 10))
        backsurface.fill((50, 50, 50)); pygame.draw.circle(backsurface, (255, 255, 255), (radius, radius), radius)
        backsurface.set_colorkey((255, 255, 255))
        self.renderedpietexts = None;  self.renderedback = backsurface
        
    def drawIcon(self, screen: pygame.Surface,mousebuttons) -> bool:
        """Draws the home/stock icon in the top left corner, returns True if the icon is clicked"""
        # Draw the triangles to form a square in the top left corner
        hometri = [(25, 10), (25, 160), (175, 10)]
        stockstri = [(175, 10), (175, 160), (25, 160)]

        # Check if the mouse is clicked and hovering over the triangles
        mouse_pos = pygame.mouse.get_pos()
        home_color = (0, 120, 0) if self.view == "home" else (20,20,20)
        stocks_color = (120, 0, 0) if self.view == "stock" else (20,20,20)

        # Check if the mouse is hovering over the triangles
        if point_in_triangle(mouse_pos, hometri):
            home_color = (0, 170, 0)
            stocks_color = (80, 0, 0) if stocks_color == (120, 0, 0) else (20,20,20)
            if mousebuttons == 1:
                self.view = "home"
                soundEffects['clickbutton2'].play()
                return True

        if point_in_triangle(mouse_pos, stockstri):
            stocks_color = (170, 0, 0)
            home_color = (0, 120, 0) if home_color == (0, 170, 0) else (20,20,20)
            
            if mousebuttons == 1:
                self.view = "stock"
                soundEffects['clickbutton2'].play()
                return True

        # Draw the triangles
        pygame.draw.polygon(screen, home_color, [(x, y) for x, y in hometri])
        pygame.draw.polygon(screen, stocks_color, [(x, y) for x, y in stockstri])

        # Draw the outline for the triangles
        pygame.draw.polygon(screen, (0, 0, 0), [(x, y) for x, y in hometri], 4)
        pygame.draw.polygon(screen, (0, 0, 0), [(x, y) for x, y in stockstri], 4)

        # Draw the "Home" and "Stocks" text in the triangles
        home = fontlist[50].render('Home', (255, 255, 255))[0]
        screen.blit(home, (90 - home.get_width() / 2 - 15, 45 - home.get_height() / 2))
        stocks = fontlist[50].render('Stocks', (255, 255, 255))[0]
        screen.blit(stocks, (140 - stocks.get_width() / 2 - 15, 95 + stocks.get_height() / 2))
        return False



    def draw_stockbar(self,screen:pygame.Surface,stocklist:list):
        self.graphscroll += 1*(self.gameplay_speed/self.bar.maxvalue)+1# the speed of the stock graph 
        self.percentchanges = self.get_listpercents(stocklist)
        if self.graphscroll > len(stocklist)*190: self.graphscroll = 0
        for i,stock in enumerate(stocklist):# draws the stock graph bar
            x = int(250-self.graphscroll+(i*190))
            if x < 250-120:
                x += len(stocklist)*190
            if x < 1450+100:# if the stock is on the screen
                
                color = (0,200,0) if self.percentchanges[i] >= 0 else (200,0,0)

                stocklist[i].baredraw(screen,(x+100,710),(x,710+80),'hour')# draws the graph
                screen.blit(self.namerenders[i][0 if self.percentchanges[i] <= 0 else 1],(x-70,710+10))# draws the name of the stock
                ptext = fontlist[28].render(limit_digits(stock.price,9),color)[0]# renders the price of the stock
                screen.blit(ptext,(x-42-(ptext.get_width()/2),710+50))# draws the price of the stock

        gfxdraw.filled_polygon(screen,[(50,710),(50,790),(250,790),(250,710)],(50,50,50))# cover up the left side of the stock graph bar
        gfxdraw.filled_polygon(screen,[(1650,710),(1650,790),(1450,790),(1450,710)],(50,50,50)) # cover up the right side of the stock graph bar
        # draw an outline for the stock  bar graph
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(250,710,1200,80),5)

    def draw_time(self,screen:pygame.Surface,gametime):
        # draws the time at the top of the screen
        renders = gametime.getrenders()
        width = 0
        for i in range(3):
            screen.blit(renders[i],(275+(width),65))
            width += renders[i].get_width()*1.5
            if i != 2:
                text = fontlist[55].render('/',(255,255,255))[0]
                screen.blit(text,(275+(width),65))
                width += text.get_width()+renders[i].get_width()/2
        for i in range(3,6):
            screen.blit(renders[i],(275+(width),65))
            width += renders[i].get_width()*1.5
            if i == 3:
                text = fontlist[55].render(':',(255,255,255))[0]
                screen.blit(text,(275+(width),73))
                width += text.get_width()+renders[i].get_width()/2

        
    def drawStockEvents(self,screen:pygame.Surface,stocklist:list):
        minmove = min([stock for stock in stocklist],key=self.get_percent)
        maxmove = max([stock for stock in stocklist],key=self.get_percent)

        self.stockevent.addStockEvent(minmove.name,1600,abs(self.get_percent(minmove)),False)
        self.stockevent.addStockEvent(maxmove.name,1600,abs(self.get_percent(maxmove)))
        # self.stockevent.addStockEvent('KSTON',100)
        
        self.stockevent.draw(screen)
        
    def draw_home(self,screen:pygame.Surface,stocklist:list,gametime,player):
        gfxdraw.filled_polygon(screen,[(200,10),(250,150),(1450,150),(1400,10)],(10,10,10))# time etc
        self.draw_time(screen,gametime)
        gfxdraw.filled_polygon(screen,[(250,800),(275,1050),(1475,1050),(1450,800)],(10,10,10))# the News bar at the bottom
        
        gfxdraw.filled_polygon(screen,[(250,710),(250,790),(1450,790),(1450,710)],(30,30,30))# stock graph bar (scrolls across screen)
        
        gfxdraw.filled_polygon(screen,[(930,160),(930,700),(1450,700),(1450,160)],(75,75,75))# Announcements bar (right of the portfolio)
        self.draw_stockbar(screen,stocklist)
        self.drawStockEvents(screen,stocklist)
        self.newsobj.draw(screen)

        values = [(stock[0].price * stock[2], stock[0].name) for stock in player.stocks]
        names = set([stock[0].name for stock in player.stocks])
        values = [[sum([v[0] for v in values if v[1] == name]), name] for name in names]
        values.append([player.cash, "Cash"])
        _,self.renderedpietexts = draw_pie_chart(screen, values, 175, (1460, 160),self.renderedback,self.renderedpietexts)

    def draw_ui(self,screen,stockgraphmanager,stocklist,player,gametime,mousebuttons,menulist):
        if self.drawIcon(screen,mousebuttons):
            for i in range(len(menulist)):menulist[i].menudrawn = False
        if not any(menu.menudrawn for menu in menulist):# if any of the menus are drawn, then don't draw
            if self.view == "home":
                mousex,mousey = pygame.mouse.get_pos()
                
                self.draw_home(screen,stocklist,gametime,player)            

                player.draw(screen,player,(900,160),(250,700),stocklist,mousebuttons,True)
                self.gameplay_speed = self.bar.draw_bar(screen,[1500,650],[120,380],'vertical')


            elif self.view == "stock":
                stockgraphmanager.draw_graphs(screen,stocklist,player,mousebuttons)
                # player.draw(screen,player,(1920,0),(1600,400),stocklist,mousebuttons)
                self.gameplay_speed = self.bar.draw_bar(screen,[1620,650],[120,380],'vertical')

