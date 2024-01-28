import pygame
import timeit
from Defs import *
from Classes.imports.Menu import Menu
from pygame import gfxdraw
from Classes.imports.Bar import SliderBar
from Classes.imports.Latterscroll import *
from Classes.Stockbook import quantityControls
import math

DX = 300# default x
DY = 230# default y
DH = 120# default height
class Portfolio(Menu):
    def __init__(self):
        self.icon = pygame.image.load(r'Assets\Menu_Icons\portfolio.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon,(140,100))
        self.icon.set_colorkey((255,255,255))
        super().__init__(self.icon)
        # remove all the white from the image
        # self.bar = SliderBar(50,[(150,150,150),(10,10,10)],barcolor=((20,130,20),(40,200,40)))
        # self.bar.value = 0
        self.quantitybar = SliderBar(50,[(150,150,150),(10,10,10)],barcolor=((20,130,20),(40,200,40)))

        self.sharebackground = pygame.image.load(r"Assets\backgrounds\Background (8).png").convert_alpha()
        self.sharebackground = self.sharebackground.subsurface((0,0,485,880))
        self.sharebackground.set_alpha(150)

        self.portfoliotext = fontlist[65].render('Owned Shares',(220,220,220))[0]
        self.showingtext = fontlist[45].render('Showing ',(220,220,220))[0]
        self.menudrawn = True
        self.allrenders = []
        self.selected_stock = None

        # self.latterScrollsurf = pygame.Surface((730,730))
        self.latterscroll = PortfolioLatter()

        self.prerenders = [
                s_render('Profit',45,(190,190,190)),# text for the profit/loss
                s_render('Lost',45,(190,190,190)),# text for the profit/loss
                s_render('Bought at $',45,(190,190,190)),
                s_render('per share',45,(190,190,190)),
                s_render('Current Price $',45,(190,190,190)),
            ]

        
    def getpoints(self, w1, w2, w3, x, y):
        """returns the points for the polygon of the portfolio menu""" 
        # top left, top right, bottom right, bottom left
        p1 = ((DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + x + w1 + 25, DY + DH + y), (DX + x + w1 + 10, DY + y))
        p2 = [(DX + 10 + x + w1, DY + y), (DX + 25 + x +w1, DY + DH + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 10 + w1 + w2 + x, DY + y)]
        p3 = [(DX + 10 + w1 + w2 + x, DY + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]
        total = [(DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]

        return [p1, p2, p3, total]
    
    def drawSelectedStock(self, screen, stock, mousebuttons, player):
        if stock != None:
            mousex, mousey = pygame.mouse.get_pos()
           
            gfxdraw.filled_polygon(screen, [(1030, 425), (1505, 425), (1565, 925), (1085, 925)], (30, 30, 30))
            pygame.draw.polygon(screen, (0, 0, 0), [(1030, 425), (1505, 425), (1565, 925), (1085, 925)], 6)
            # self.quantity = quantityControls(screen,mousebuttons,stock[2],self.quantity,(1100,610))
            self.quantitybar.changemaxvalue(stock[2])
            self.quantitybar.draw_bar(screen,[1100,700],[300,35],'horizontal',reversedscroll=True)
            # draw the stock name

            # text = fontlist[50].render(f'{stock[0]} X {limit_digits(stock[2],10,False)}', (190, 190, 190))[0]
            screen.blit(s_render(f'{stock[0]} X {limit_digits(stock[2],10,False)}', 50, (190, 190, 190)), (1040, 435))# display the stock name

            sellpoints = [(1110, 840), (1125, 910), (1465, 910), (1450, 840)]
            # use the same system found in the stockbook class to draw the sell button and the selector for the amount of stocks to sell
            if point_in_polygon((mousex,mousey),sellpoints):
                sellcolor = (150,0,0)
                if mousebuttons == 1:
                    player.sell(stock[0],stock[1],int(self.quantitybar.value))
                    self.selected_stock = None
                    self.quantitybar.value = 0
            else:
                sellcolor = (225,225,225)

            # Draws the information about the stock on the right side of the screen 
            info = [f'Paid Price: ${limit_digits(stock[1]*stock[2],12)}',f'Paid ${limit_digits(stock[1],12)} | Current ${limit_digits(stock[0].price,12)}',f'{"Profit" if (stock[0].price - stock[1])*stock[2] > 0 else "Loss"}: ${limit_digits((stock[0].price - stock[1])*stock[2],15)}',f'Change %: {limit_digits(((stock[0].price - stock[1]) / stock[1]) * 100,15)}%']
            
            for i,txt in enumerate(info):
                screen.blit(s_render(txt,35,(130,130,130)),(1050+(i*8),490+(i*50)))

            # total value of the stocks above the sell button
            value = stock[0].price * self.quantitybar.value
            valuetext = s_render(f'Value: ${limit_digits(value,15)}', 45, (190, 190, 190))
            points = [(1100, 745), (1115, 815), (1455, 815), (1440, 745)]
            gfxdraw.filled_polygon(screen, points, (15,15,15))
            pygame.draw.polygon(screen, (0, 0, 0), points, 5)
            screen.blit(valuetext, (1115, 765))

            # sell button
            gfxdraw.filled_polygon(screen, sellpoints, (15,15,15))
            pygame.draw.polygon(screen, (0, 0, 0), sellpoints, 5)
            sell_text = s_render(f'SELL', 65, sellcolor)
            sell_text_rect = sell_text.get_rect(center=(1280, 875))
            screen.blit(sell_text, sell_text_rect)



    def draw_stockscroll(self,sortedstocks,screen,mousebuttons):
        # function to get the text for each stock
        get_text = lambda stock : [f'{stock[0]} ',
                                    f"{limit_digits(stock[2],10,False)} Share{'' if stock[2] == 1 else 's'}",
                                    f'${limit_digits(stock[0].price*stock[2],15)}',]
        # getting the text for each stock
        textlist = [get_text(stock) for stock in sortedstocks]# stores 3 texts for each stock in the sortedstocks list

        textinfo = []# stores the text info for the latter scroll [text,fontsize,color]
        coords = [[(20,15),(25,60)] for i in range(len(textlist))]
        # loop through the textlist and store the text info in the textinfo list
        for i,(text,stock) in enumerate(zip(textlist,sortedstocks)):
            polytexts = []# temporary list to store the text info for each stock
            polytexts.append([text[0],50,stock[0].color])
            polytexts.append([text[1],35,(190,190,190)])
            polytexts.append([text[2],50,(190,190,190)])
            textinfo.append(polytexts)
            coords[i].append(((text[1],50),30))

        self.latterscroll.storetextinfo(textinfo)# simply changes the self.texts in latterscroll
        self.latterscroll.set_textcoords(coords)# simply changes the self.textcoords in latterscroll
        # Does most of the work for the latter scroll, renders the text and finds all the coords
        self.latterscroll.store_rendercoords((1500, 105), (380,950),135,0,0,updatefreq=60)
        # drawing the latter scroll and assigning the selected stock
        self.selected_stock = sortedstocks[self.latterscroll.draw_polys(screen, (1500, 105), mousebuttons, sortedstocks.index(self.selected_stock), *sortedstocks)]
        if len(sortedstocks)/135 > 950-105:# if there is more stocks than the screen can fit
            screen.blit(s_render("Scroll to see more", 35, (190, 190, 190)), (1600, 950))

    def drawSelected(self, screen, mousebuttons, player):
        if self.selected_stock != None:
            mousex, mousey = pygame.mouse.get_pos()
            #  draw a polygon from 815,110 to 1480,960
            points = [(810, 105), (1490, 105), (1490, 960), (810, 960)]
            gfxdraw.filled_polygon(screen, points, (20, 20, 20, 190))
            pygame.draw.polygon(screen, (0, 0, 0), points, 5)


            percent = ((self.selected_stock[0].price/self.selected_stock[1])-1)

            # lostprotext = s_render('Profit' if percent >= 0 else 'Lost',45,(190,190,190))
            # screen.blit(lostprotext,(815,110))# display the portfolio text
            # percenttext = s_render(f'{limit_digits(percent,15)}%',45,(190,190,190))
            # screen.blit(percenttext,(820+lostprotext.get_width(),110))# display the portfolio text

            # pricetext = s_render(f'${limit_digits(self.selected_stock[0].price*self.selected_stock[2],15)}',45,(190,190,190))
            # screen.blit(pricetext,(1480-pricetext.get_width(),110))# display the portfolio text
            
            texts = [
                self.prerenders[0] if percent >= 0 else self.prerenders[1],# text for the profit/loss
                s_render(f'${limit_digits(percent,15)}%',45,(190,190,190)),# text for the percent
                s_render(f'${limit_digits(self.selected_stock[1]*self.selected_stock[2],15)}',45,(190,190,190)),# text for the total paid
                self.prerenders[2],# text for the "bought at" text
                s_render(str(limit_digits(self.selected_stock[1],15)),45,(190,190,190)),
                self.prerenders[3],# text for the "per share" text
                self.prerenders[4],# text for the "current price" text
                s_render(str(limit_digits(self.selected_stock[0].price,15)),45,(190,190,190)),
            ]
            coords = [
                (815,110),# coords for the profit/loss
                (820+texts[0].get_width(),110),# coords for the percent
                (1480-texts[1].get_width(),110),# coords for the total paid
                (820,465),# coords for the "bought at" text
                (820+texts[3].get_width(),465),# coords for the price text
                (830+texts[3].get_width()+texts[4].get_width(),465),# coords for the "per share" text
                (820,515),# coords for the "current price" text
                (820+texts[6].get_width(),515),# coords for the current price text
            ]
            for text,coord in zip(texts,coords):
                screen.blit(text,coord)# display all the texts


            self.selected_stock[0].baredraw(screen,(820,155),(660,295),'1M',True)

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player):
        """Draws all of the things in the portfolio menu"""
        mousex, mousey = pygame.mouse.get_pos()
            
        sortedstocks = sorted(player.stocks,key=lambda stock: stock[0].price*stock[2],reverse=True)

        if len(self.allrenders) < len(player.stocks):# if the player has more stocks than the renders
            for i in range((len(player.stocks)-len(self.allrenders))+1):# add the amount of renders needed
                self.allrenders.append({})

        if self.selected_stock == None and len(player.stocks) > 0:
            self.selected_stock = sortedstocks[0]
       
        player.draw(screen,player,(200,100),(600,500),mousebuttons,stocklist,True)
        
        if len(player.stocks) > 0:
            # draws the stocks on the right of the screen
            self.draw_stockscroll(sortedstocks,screen,mousebuttons)

            # draws the selected stock information in the middle of the screen
            self.drawSelected(screen, mousebuttons, player)

     
            

        values = [(stock[0].price * stock[2], stock[0].name) for stock in player.stocks]
        names = set([stock[0].name for stock in player.stocks])
        values = [[sum([v[0] for v in values if v[1] == name]), name, stocklist[[s.name for s in stocklist].index(name)].color] for name in names]

        draw_pie_chart(screen, values, 150,(200, 650))

