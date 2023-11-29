import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.Bar import Bar
from Classes.imports.stockeventspos import StockEvents
from Classes.imports.Newsbar import News

# [20,60] [60,20]
# [700,1000] [1000,650]
def limit_digits(num, max_digits):
    if len("{:.2f}".format(num)) > max_digits:
        return "{:.2e}".format(num)
    else:
        return "{:.2f}".format(num)
class UI_Controls(Bar):
    def __init__(self,windowoffset:list,stocklist) -> None:
        maxgamespeed = 50
        pos = [1500,650]
        wh = [120,380]
        orientation = 'vertical'
        self.stockevent = StockEvents()
        self.newsobj = News()
        self.newsobj.addStockNews('MAGLO')

        super().__init__(windowoffset,maxgamespeed,pos,wh,orientation)
        # self.view = "stock"# homeview or stockview
        self.view = "home"# homeview or stockview
        self.graphscroll = 0
        self.namerenders = [[fontlist[30].render(stock.name,(200,0,0))[0],fontlist[30].render(stock.name,(0,200,0))[0]] for stock in stocklist]# [red,green]

        # get 
        self.get_percent = lambda stock : round(((stock.graphrangelists[stock.graphrange][-1]/stock.graphrangelists[stock.graphrange][0])-1)*100,2)
        self.get_listpercents = lambda xlist : [self.get_percent(stock) for stock in xlist]
        self.percentchanges = self.get_listpercents(stocklist)
        self.totalperecent = lambda xlist : sum([self.get_percent(stock) for stock in xlist])
        
    def drawIcon(self, screen: pygame.Surface):
        # Draw the triangles to form a square in the top left corner
        
        def point_in_triangle(point, triangle):
            x, y = point
            x1, y1 = triangle[0]
            x2, y2 = triangle[1]
            x3, y3 = triangle[2]
            denominator = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
            a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denominator
            b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denominator
            c = 1 - a - b
            return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1
        
        hometri = [(40, 10), (40, 160), (190, 10)]
        stockstri = [(190, 10), (190, 160), (40, 160)]

        # Check if the mouse is clicked and hovering over the triangles
        mouse_pos = pygame.mouse.get_pos()
        home_color = (0, 120, 0) if self.view == "home" else (20,20,20)
        stocks_color = (120, 0, 0) if self.view == "stock" else (20,20,20)

        # Check if the mouse is hovering over the triangles
        if point_in_triangle(mouse_pos, hometri):
            home_color = (0, 170, 0)
            stocks_color = (80, 0, 0) if stocks_color == (120, 0, 0) else (20,20,20)
            if pygame.mouse.get_pressed()[0]:
                self.view = "home"

        if point_in_triangle(mouse_pos, stockstri):
            stocks_color = (170, 0, 0)
            home_color = (0, 120, 0) if home_color == (0, 170, 0) else (20,20,20)
            
            if pygame.mouse.get_pressed()[0]:
                self.view = "stock"

        # Draw the triangles
        pygame.draw.polygon(screen, home_color, [(x-15, y) for x, y in hometri])
        pygame.draw.polygon(screen, stocks_color, [(x-15, y) for x, y in stockstri])

        # Draw the outline for the triangles
        pygame.draw.polygon(screen, (0, 0, 0), [(x-15, y) for x, y in hometri], 4)
        pygame.draw.polygon(screen, (0, 0, 0), [(x-15, y) for x, y in stockstri], 4)

        # Draw the "Home" and "Stocks" text in the triangles
        home = fontlist[50].render('Home', (255, 255, 255))[0]
        screen.blit(home, (90 - home.get_width() / 2 - 15, 45 - home.get_height() / 2))
        stocks = fontlist[50].render('Stocks', (255, 255, 255))[0]
        screen.blit(stocks, (140 - stocks.get_width() / 2 - 15, 95 + stocks.get_height() / 2))



    def draw_stockbar(self,screen:pygame.Surface,stocklist:list):
        self.graphscroll += 1*(self.gameplay_speed/self.maxvalue)+1# the speed of the stock graph 
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
                ptext = fontlist[30].render(limit_digits(stock.price,8),color)[0]# renders the price of the stock
                screen.blit(ptext,(x-40-(ptext.get_width()/2),710+50))# draws the price of the stock

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
        
    def draw_home(self,screen:pygame.Surface,stocklist:list,gametime):
        gfxdraw.filled_polygon(screen,[(200,10),(250,150),(1450,150),(1400,10)],(10,10,10))# time etc
        self.draw_time(screen,gametime)
        gfxdraw.filled_polygon(screen,[(250,800),(275,1050),(1475,1050),(1450,800)],(10,10,10))# the News bar at the bottom
        
        gfxdraw.filled_polygon(screen,[(250,710),(250,790),(1450,790),(1450,710)],(30,30,30))# stock graph bar (scrolls across screen)
        
        gfxdraw.filled_polygon(screen,[(930,160),(930,700),(1450,700),(1450,160)],(75,75,75))# Announcements bar (right of the portfolio)
        self.draw_stockbar(screen,stocklist)
        self.drawStockEvents(screen,stocklist)
        self.newsobj.draw(screen)
        
    

    def draw_ui(self,screen,stockgraphmanager,stocklist,player,gametime,Mousebuttons):
        self.drawIcon(screen)
        if self.view == "home":
            mousex,mousey = pygame.mouse.get_pos()
            if Mousebuttons == 1:
                print(mousex,mousey)
                Mousebuttons = 0
            
            self.draw_home(screen,stocklist,gametime)            

            player.draw(screen,player,(900,160),(250,700),stocklist,Mousebuttons)
            self.draw_bar(screen)


        elif self.view == "stock":
            stockgraphmanager.draw_graphs(screen,stocklist,player,Mousebuttons)
            player.draw(screen,player,(1920,0),(1600,400),stocklist,Mousebuttons)
            self.draw_bar(screen)

