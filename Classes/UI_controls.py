import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.Bar import Bar

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

        super().__init__(windowoffset,maxgamespeed,pos,wh,orientation)
        # self.view = "stock"# homeview or stockview
        self.view = "home"# homeview or stockview
        self.graphscroll = 0
        self.namerenders = [[fontlist[30].render(stock.name,(200,0,0))[0],fontlist[30].render(stock.name,(0,200,0))[0]] for stock in stocklist]# [red,green]

        # get 
        get_percent = lambda stock : round(((stock.graphrangelists[stock.graphrange][-1]/stock.graphrangelists[stock.graphrange][0])-1)*100,2)
        self.get_listpercents = lambda xlist : [get_percent(stock) for stock in xlist]
        self.percentchanges = self.get_listpercents(stocklist)
        self.totalperecent = lambda xlist : sum([get_percent(stock) for stock in xlist])
    
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
        

        
    def draw_home(self,screen:pygame.Surface,stocklist:list,gametime):
        gfxdraw.filled_polygon(screen,[(200,10),(250,150),(1450,150),(1400,10)],(10,10,10))# time etc
        self.draw_time(screen,gametime)
        gfxdraw.filled_polygon(screen,[(250,800),(275,1050),(1475,1050),(1450,800)],(10,10,10))# the News bar at the bottom
        
        gfxdraw.filled_polygon(screen,[(250,710),(250,790),(1450,790),(1450,710)],(30,30,30))# stock graph bar (scrolls across screen)
        
        gfxdraw.filled_polygon(screen,[(930,160),(930,700),(1450,700),(1450,160)],(75,75,75))# Announcements bar (right of the portfolio)
        self.draw_stockbar(screen,stocklist)
        
    

    def draw_ui(self,screen,stockgraphmanager,stocklist,player,gametime,Mousebuttons):
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

