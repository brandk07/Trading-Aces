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
        self.bar = SliderBar(windowoffset,100,[(20,50,200),(110,110,110)])# the bar for the gameplay speed
        self.newsobj = News()
        for i in range(10):
            for stock in stocklist:
                self.newsobj.addStockNews(stock.name)

        self.view = "home"# home or stock
        self.announce_state = "announce"# annouce or stock
        self.graphscroll = 0
        self.namerenders = [fontlist[30].render(stock.name,stock.color)[0] for stock in stocklist]# [red,green]
        self.weeknames = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        self.weekdaystext = {weekday:fontlist[95].render(weekday,(255,255,255))[0] for weekday in self.weeknames}
        # self.namerenders = [[fontlist[30].render(stock.name,(200,0,0))[0],fontlist[30].render(stock.name,(0,200,0))[0]] for stock in stocklist]# [red,green]

        # get 
        self.get_percent = lambda stock : round(((stock.graphrangelists[stock.graphrange][-1]/stock.graphrangelists[stock.graphrange][0])-1)*100,2)
        self.get_listpercents = lambda xlist : [self.get_percent(stock) for stock in xlist]
        self.percentchanges = self.get_listpercents(stocklist)
        self.totalperecent = lambda xlist : sum([self.get_percent(stock) for stock in xlist])
        # for pie chart
        self.stockbarsurf = pygame.Surface((1200,80))
        
        
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



    def draw_stockbar(self,screen:pygame.Surface,stocklist:list,coords:list=[250,710],wh=[1200,80]):
        """Draws a bar that scrolls across the screen, displaying the stock prices, maxwidth is 1710"""
        dx,dy = coords
        if wh[1] > 1710: wh[1] = 1710
        if self.stockbarsurf.get_width() != wh[0] or self.stockbarsurf.get_height() != wh[1]:
            self.stockbarsurf = pygame.Surface(wh)
        
        self.graphscroll += 1*(self.gameplay_speed/self.bar.maxvalue)+1# the speed of the stock graph 
        self.percentchanges = self.get_listpercents(stocklist)
        if self.graphscroll > len(stocklist)*190: self.graphscroll = 0
        for i,stock in enumerate(stocklist):# draws the stock graph bar
            x = int(0-self.graphscroll+(i*190))
            if x < -120:
                x += len(stocklist)*190
            if x < wh[0]+100:# if the stock is on the screen
                
                color = (0,200,0) if self.percentchanges[i] >= 0 else (200,0,0)

                stocklist[i].baredraw(self.stockbarsurf,(x+100,0),(x,wh[1]),'hour')# draws the graph
                self.stockbarsurf.blit(self.namerenders[i],(x-70,10))# draws the name of the stock
                ptext = fontlist[28].render(limit_digits(stock.price,9),color)[0]# renders the price of the stock
                self.stockbarsurf.blit(ptext,(x-42-(ptext.get_width()/2),50))# draws the price of the stock

        pygame.draw.rect(self.stockbarsurf,(0,0,0),pygame.Rect(0,0,wh[0],wh[1]),5)# draws the outline of the stock graph bar
        screen.blit(self.stockbarsurf,(dx,dy))# draw the stock graph bar to the screen
        self.stockbarsurf.fill((30,30,30))# fill the stock graph bar with a dark grey color
        
    def drawAnnouncements(self,screen:pygame.Surface,stocklist:list,mousebuttons):
        """Draws the stock events to the screen"""
        points1 = [(940,175),(955,215),(940+250,215),(925+250,175)]
        points2 = [(940+250,175),(955+250,215),(940+505,215),(925+505,175)]
        
        gfxdraw.filled_polygon(screen,points1,(30,30,30))
        gfxdraw.filled_polygon(screen,points2,(30,30,30))
        pygame.draw.polygon(screen,(0,0,0),points1,5)
        pygame.draw.polygon(screen,(0,0,0),points2,5)
        scolor = (255,255,255); acolor = (255,255,255)
        if point_in_polygon(pygame.mouse.get_pos(),points1):
            scolor = (0,255,0)
            if mousebuttons == 1:
                self.announce_state = "stock"
        elif point_in_polygon(pygame.mouse.get_pos(),points2):
            acolor = (0,255,0)
            if mousebuttons == 1:
                self.announce_state = "announce"

        stocktext = fontlist[30].render('Stocks', scolor)[0]
        screen.blit(stocktext,(940+125-stocktext.get_width()/2,190-stocktext.get_height()/2))
        announcetext = fontlist[30].render('Announcements', acolor)[0]
        screen.blit(announcetext,(940+375-announcetext.get_width()/2,190-announcetext.get_height()/2))

        if self.announce_state == "announce":
            minmove = min([stock for stock in stocklist],key=self.get_percent)
            maxmove = max([stock for stock in stocklist],key=self.get_percent)

            self.stockevent.addStockEvent(minmove.name,1600,abs(self.get_percent(minmove)),False)
            self.stockevent.addStockEvent(maxmove.name,1600,abs(self.get_percent(maxmove)))
            self.stockevent.draw(screen)
        elif self.announce_state == "stock":    
            pass

        
        
    def draw_time(self,screen,gametime):
        texts = gametime.getrenders(50,50,50,105,50,50)# month,day,year,timerender,dayname,monthname
        month,day,year,timerender,dayname,monthname = texts

        screen.blit(timerender,(260,20))
        screen.blit(dayname,(260,105))
        screen.blit(monthname,(260+dayname.get_width()+10,105))
        screen.blit(day,(260+dayname.get_width()+monthname.get_width()+20,105))
        screen.blit(year,(260+dayname.get_width()+monthname.get_width()+day.get_width()+30,105))


    def draw_home(self,screen:pygame.Surface,stocklist:list,gametime,player,mousebuttons):
        gfxdraw.filled_polygon(screen,[(200,10),(250,150),(1450,150),(1400,10)],(10,10,10))# time etc
        pygame.draw.polygon(screen,(0,0,0),[(200,10),(250,150),(1450,150),(1400,10)],5)# time etc
        # screen.blit(self.weekdaystext[gametime.get_day_name()],(265,20))
        self.draw_time(screen,gametime)


        gfxdraw.filled_polygon(screen,[(250,800),(275,1050),(1475,1050),(1450,800)],(10,10,10))# the News bar at the bottom
        pygame.draw.polygon(screen,(0,0,0),[(250,800),(275,1050),(1475,1050),(1450,800)],5)# the News bar at the bottom Outline
        gfxdraw.filled_polygon(screen,[(250,710),(250,790),(1450,790),(1450,710)],(30,30,30))# stock graph bar (scrolls across screen)
        
        gfxdraw.filled_polygon(screen,[(930,160),(930,700),(1450,700),(1450,160)],(75,75,75))# Announcements bar (right of the portfolio)
        pygame.draw.polygon(screen,(0,0,0),[(930,160),(930,700),(1450,700),(1450,160)],5)# Announcements bar (right of the portfolio) Outline
        
        self.draw_stockbar(screen,stocklist)# draws the stock graph bar
        self.drawAnnouncements(screen,stocklist,mousebuttons)# draws the stock events (On the right of the portfolio)
        self.newsobj.draw(screen)

        values = [(stock[0].price * stock[2], stock[0].name) for stock in player.stocks]
        names = set([stock[0].name for stock in player.stocks])

        values = [[sum([v[0] for v in values if v[1] == name]), name, stocklist[[s.name for s in stocklist].index(name)].color] for name in names]
        values.append([player.cash, "Cash",player.color])

        # add the player.options to the values
        for option in player.options:
            values.append([option.get_value(),option.name,option.color])
        _,self.renderedpietexts = draw_pie_chart(screen, values, 160, (800, 160),self.renderedback,self.renderedpietexts)

    def draw_ui(self,screen,stockgraphmanager,stocklist,player,gametime,mousebuttons,menulist):
        if self.drawIcon(screen,mousebuttons):
            for i in range(len(menulist)):menulist[i].menudrawn = False
        if not any(menu.menudrawn for menu in menulist):# if any of the menus are drawn, then don't draw
            if self.view == "home":
                mousex,mousey = pygame.mouse.get_pos()
                
                self.draw_home(screen,stocklist,gametime,player,mousebuttons)            

                player.draw(screen,player,(900,160),(250,700),stocklist,mousebuttons,True)
                self.gameplay_speed = self.bar.draw_bar(screen,[1500,650],[120,380],'vertical')


            elif self.view == "stock":
                stockgraphmanager.draw_graphs(screen,stocklist,player,mousebuttons)
                # player.draw(screen,player,(1920,0),(1600,400),stocklist,mousebuttons)
                self.gameplay_speed = self.bar.draw_bar(screen,[1620,575],[125,400],'vertical')



