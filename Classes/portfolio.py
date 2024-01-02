import pygame
import timeit
from Defs import *
from Classes.imports.Menu import Menu
from pygame import gfxdraw
from Classes.imports.Bar import SliderBar
from Classes.Stockbook import quantityControls
import math

DX = 300# default x
DY = 200# default y
DH = 120# default height
class Portfolio(Menu):
    def __init__(self):
        
        self.icon = pygame.image.load(r'Assets\Menu_Icons\portfolio.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon,(140,100))
        self.icon.set_colorkey((255,255,255))
        super().__init__(self.icon)
        # remove all the white from the image
        self.bar = SliderBar((0,0),50,[(0,120,0),(110,110,110)])
        self.bar.value = 0
        
        self.portfoliotext = fontlist[65].render('Portfolio',(220,220,220))[0]
        self.menudrawn = False
        self.renderedpietexts = None; self.renderedback = None
        self.allrenders = []
        self.selected_stock = None; self.quantity = 0
        
    def getpoints(self, w1, w2, w3, x, y):
        """returns the points for the polygon of the portfolio menu""" 
        # top left, top right, bottom right, bottom left
        p1 = ((DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + x + w1 + 25, DY + DH + y), (DX + x + w1 + 10, DY + y))
        p2 = [(DX + 10 + x + w1, DY + y), (DX + 25 + x +w1, DY + DH + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 10 + w1 + w2 + x, DY + y)]
        p3 = [(DX + 10 + w1 + w2 + x, DY + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]
        total = [(DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]

        return [p1, p2, p3, total]
    
    def drawSelectedStock(self, screen, stockindex, mousebuttons, player):
        if stockindex != None:
            stock = player.stocks[stockindex]
            mousex, mousey = pygame.mouse.get_pos()
           
            gfxdraw.filled_polygon(screen, [(1030, 425), (1505, 425), (1565, 925), (1085, 925)], (30, 30, 30))
            pygame.draw.polygon(screen, (0, 0, 0), [(1030, 425), (1505, 425), (1565, 925), (1085, 925)], 6)
            self.quantity = quantityControls(screen,mousebuttons,player.stocks[stockindex][2],self.quantity,(1100,610))
            
            # draw the stock name
            text = fontlist[50].render(f'{stock[0]} X {limit_digits(stock[2],10,False)}', (190, 190, 190))[0]
            screen.blit(text, (1040, 435))# display the stock name

            # use the same system found in the stockbook class to draw the sell button and the selector for the amount of stocks to sell
            if point_in_polygon((mousex,mousey),[(1110,805),(1125,875),(1465,875),(1450,805)]):
                sellcolor = (150,0,0)
                if mousebuttons == 1:
                    if self.quantity >= player.stocks[stockindex][2]:
                        player.sell(player.stocks[stockindex][0],player.stocks[stockindex][1],int(self.quantity))
                        self.selected_stock = None
                    else:
                        player.sell(player.stocks[stockindex][0],player.stocks[stockindex][1],int(self.quantity))
                    self.quantity = 0
            else:
                sellcolor = (225,225,225)

            # Draws the information about the stock on the right side of the screen
            info = [f'Profit: ${limit_digits((stock[0].price - stock[1])*stock[2],15)}',f'Change %: {limit_digits(((stock[0].price - stock[1]) / stock[1]) * 100,15)}%',f'Paid Price: ${limit_digits(stock[1]*stock[2],15)}']
            for i,txt in enumerate(info):
                screen.blit(fontlist[35].render(txt,(190,190,190))[0],(1050+(i*8),490+(i*50)))

            # total value of the stocks above the sell button
            value = stock[0].price * self.quantity
            text = fontlist[45].render(f'Value: ${limit_digits(value,15)}', (190, 190, 190))[0]
            gfxdraw.filled_polygon(screen,((1110,705),(1125,775),(1465,775),(1450,705)),(15,15,15))#polygon for the total value button
            pygame.draw.polygon(screen, (0,0,0), ((1110,705),(1125,775),(1465,775),(1450,705)),5)#outline total value button polygon
            
            
            screen.blit(text, (1130, 725))
            # sell button
            gfxdraw.filled_polygon(screen,((1110,805),(1125,875),(1465,875),(1450,805)),(15,15,15))#polygon for the sell button
            pygame.draw.polygon(screen, (0,0,0), ((1110,805),(1125,875),(1465,875),(1450,805)),5)#outline sell button polygon
            sell_text, _ = fontlist[65].render(f'SELL', sellcolor)
            sell_text_rect = sell_text.get_rect(center=(1280, 840))
            screen.blit(sell_text, sell_text_rect)
            
    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player):
        """Draws all of the things in the portfolio menu"""
        mousex, mousey = pygame.mouse.get_pos()
        xshift = 15
        yshift = 150    
        if len(self.allrenders) < len(player.stocks):# if the player has more stocks than the renders
            for i in range((len(player.stocks)-len(self.allrenders))+1):# add the amount of renders needed
                self.allrenders.append({})
        if self.selected_stock == None and len(player.stocks) > 0:
            self.selected_stock = 0
        self.bar.scroll(mousebuttons)# check for the scroll of the bar
        self.bar.changemaxvalue(len(player.stocks) if len(player.stocks) > 0 else 1)# change the max value of the bar based on the amount of stocks the player has

        barheight = 520//len(player.stocks) if len(player.stocks) > 0 else 1
        
        self.bar.draw_bar(screen, [225, DY], [45, DY + (yshift*4) - 80], 'vertical', barwh=[43, barheight], shift=85, reversedscroll=True, text=False)
        
        screen.blit(self.portfoliotext,(220,120))# display the portfolio text

        self.drawSelectedStock(screen, self.selected_stock, mousebuttons, player)# draws the additional stock info
        
        percents = []; alltexts = []
        for i, stock in enumerate(player.stocks[self.bar.value:self.bar.value+5]):
            percentchange = ((stock[0].price - stock[1]) / stock[1]) * 100
            
            if percentchange > 0:
                grcolor = (0, 200, 0); profittext = "Profit"
                
            elif percentchange == 0:
                grcolor = (200, 200, 200); profittext = ""
            else:
                grcolor = (225, 0, 0); profittext = "Loss"

            textinfo = [[(190, 190, 190), 45],[(190, 190, 190), 35],[grcolor, 35],[grcolor, 35],[grcolor, 35]]

            texts = [f'{stock[0]} X {limit_digits(stock[2],10,False)}',
                        f'Paid Price: ${limit_digits(stock[1]*stock[2],15)}',
                        f'Price: ${limit_digits(stock[0].price*stock[2],15)}',
                        f'{profittext}: ${limit_digits((stock[0].price - stock[1])*stock[2],15)}',
                        f'Change %: {limit_digits(percentchange,15)}%'
                    ]
            self.allrenders = reuserenders(self.allrenders, texts, textinfo, i)
            percents.append(percentchange); alltexts.append(texts)

        self.allrenders,self.selected_stock = drawLatterScroll(screen,player.stocks,self.allrenders,self.bar.value,self.getpoints,(xshift,yshift),self.selected_stock,mousebuttons,DH,alltexts,percents)

        values = [(stock[0].price * stock[2], stock[0].name) for stock in player.stocks]
        names = set([stock[0].name for stock in player.stocks])
        values = [[sum([v[0] for v in values if v[1] == name]), name, stocklist[[s.name for s in stocklist].index(name)].color] for name in names]

        self.renderedback,self.renderedpietexts = draw_pie_chart(screen, values, 150,(1010, 115),self.renderedback,self.renderedpietexts)
