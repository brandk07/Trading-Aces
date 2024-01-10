import pygame
import timeit
from Defs import *
from Classes.imports.Menu import Menu
from pygame import gfxdraw
from Classes.imports.Bar import SliderBar
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
        self.bar = SliderBar((0,0),50,[(150,150,150),(10,10,10)],barcolor=((20,130,20),(40,200,40)))
        self.bar.value = 0
        self.quantitybar = SliderBar((0,0),50,[(150,150,150),(10,10,10)],barcolor=((20,130,20),(40,200,40)))

        
        self.portfoliotext = fontlist[65].render('Owned Shares',(220,220,220))[0]
        self.showingtext = fontlist[45].render('Showing ',(220,220,220))[0]
        self.menudrawn = False
        self.renderedpietexts = None; self.renderedback = None
        self.allrenders = []
        self.selected_stock = None

        self.latterScrollsurf = pygame.Surface((730,730))
        
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
            
    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player):
        """Draws all of the things in the portfolio menu"""
        mousex, mousey = pygame.mouse.get_pos()
        xshift = 15
        yshift = 150 
        sortedstocks = sorted(player.stocks,key=lambda stock: stock[0].price*stock[2],reverse=True)

        if len(self.allrenders) < len(player.stocks):# if the player has more stocks than the renders
            for i in range((len(player.stocks)-len(self.allrenders))+1):# add the amount of renders needed
                self.allrenders.append({})

        if self.selected_stock == None and len(player.stocks) > 0:
            self.selected_stock = sortedstocks[0]
        self.bar.scroll(mousebuttons)# check for the scroll of the bar
        self.bar.changemaxvalue(len(player.stocks)-5 if len(player.stocks) > 5 else 1)# change the max value of the bar based on the amount of stocks the player has

        
        self.bar.draw_bar(screen, [225, DY], [35, int(DY + (yshift*3.25) - 50)], 'vertical', barwh=[33, 65], shift=85, reversedscroll=True, text=False)
        
        screen.blit(self.portfoliotext,(220,120))# display the portfolio text

        self.drawSelectedStock(screen, self.selected_stock, mousebuttons, player)# draws the additional stock info

        screen.blit(self.showingtext,(300,190))# display the showing text
        shownnumtext = fontlist[45].render(f'{self.bar.value+1} - {self.bar.value+5 if self.bar.value+5 < len(player.stocks) else len(player.stocks)} of {len(player.stocks)}', (190, 190, 190))[0]
        screen.blit(shownnumtext, (self.showingtext.get_width()+300, 190))
        
        x,y = DX,DY
        drawnstocks = 0

        if self.selected_stock != None:
            if self.bar.value > sortedstocks.index(self.selected_stock) and self.bar.value < len(sortedstocks):# if the selected stock is above what is displayed
                self.selected_stock = sortedstocks[self.bar.value]# select the highest stock being displayed
            elif self.bar.value+4 < sortedstocks.index(self.selected_stock) and self.bar.value+4 < len(sortedstocks):# if the selected stock is below what is displayed
                self.selected_stock = sortedstocks[self.bar.value+4]# select the lowest stock being displayed

        while y < 830 and self.bar.value+drawnstocks < len(player.stocks):
            stock = sortedstocks[self.bar.value+drawnstocks]

            percentchange = ((stock[0].price - stock[1]) / stock[1]) * 100

            height = DH if self.selected_stock == stock else DH*.85
            nametext = s_render(f'{stock[0]} ', 50, stock[0].color)
            # nametext = fontlist[50].render(f'{stock[0]} ', stock[0].color)[0]
            sharetext = s_render(f"{limit_digits(stock[2],10,False)} Share{'' if stock[2] == 1 else 's'}", 35, (190, 190, 190))
            # sharetext = fontlist[35].render(f"{limit_digits(stock[2],10,False)} Share{'' if stock[2] == 1 else 's'}", (190, 190, 190))[0]
            pricetext = s_render(f'${limit_digits(stock[0].price*stock[2],15)}', 45, (190, 190, 190))
            # pricetext = fontlist[45].render(f'${limit_digits(stock[0].price*stock[2],15)}', (190, 190, 190))[0]
            addedx = 0 if sharetext.get_width() < 85 else round(sharetext.get_width()-85,-1)
            width = nametext.get_width() + pricetext.get_width() + 180 + addedx 

            points = [(x, y), (x + 15, y + height), (x + 25 + width, y + height), (x + 10 + width, y)]
            gfxdraw.filled_polygon(screen, points, (15, 15, 15))
            pygame.draw.polygon(screen, (0, 0, 0), points, 5)
            
            screen.blit(nametext, (x+20, y+15))
            screen.blit(sharetext, (x+25, y+60))
            
            stock[0].baredraw(screen, (x+230+addedx, y), (x+120+addedx, y+height-7), 'hour')
            
            screen.blit(pricetext, (x+250+addedx, y+30))

            if (hover:=point_in_polygon((mousex,mousey),points)):
                if mousebuttons == 1:
                    self.selected_stock = stock
                    soundEffects['clickbutton2'].play()
            
            bottom_polygon = [[points[0][0]+18, points[0][1] + height - 7], 
                            [points[1][0]+5, points[1][1]], 
                            [points[2][0], points[2][1]], 
                            [points[3][0], points[3][1]],
                            [points[3][0]-7, points[3][1]],
                            [points[3][0]+5, points[3][1] + height - 7],
                            ]
            if hover or self.selected_stock == stock:
                if percentchange > 0:bottomcolor = (0, 200, 0)
                elif percentchange == 0:bottomcolor = (200, 200, 200)
                else:bottomcolor = (200, 0, 0)
            else:
                if percentchange > 0: bottomcolor = (0, 80, 0)
                elif percentchange == 0: bottomcolor = (80, 80, 80)
                else: bottomcolor = (80, 0, 0)
            gfxdraw.filled_polygon(screen,bottom_polygon,bottomcolor)

            if self.selected_stock == stock:
                y += yshift; x += xshift; drawnstocks += 1
            else:
                y += yshift*.85; x += xshift*.85; drawnstocks += 1
            
        # percents = []; alltexts = []
        # for i, stock in enumerate(player.stocks[self.bar.value:self.bar.value+5]):
        #     percentchange = ((stock[0].price - stock[1]) / stock[1]) * 100
            
        #     if percentchange > 0:
        #         grcolor = (0, 200, 0); profittext = "Profit"
                
        #     elif percentchange == 0:
        #         grcolor = (200, 200, 200); profittext = ""
        #     else:
        #         grcolor = (225, 0, 0); profittext = "Loss"

        #     textinfo = [[(190, 190, 190), 45],[(190, 190, 190), 35],[grcolor, 35],[grcolor, 35],[grcolor, 35]]

        #     texts = [f'{stock[0]} X {limit_digits(stock[2],10,False)}',
        #                 f'Paid Price: ${limit_digits(stock[1]*stock[2],15)}',
        #                 f'Price: ${limit_digits(stock[0].price*stock[2],15)}',
        #                 f'{profittext}: ${limit_digits((stock[0].price - stock[1])*stock[2],15)}',
        #                 f'Change %: {limit_digits(percentchange,15)}%'
        #             ]
        #     self.allrenders = reuserenders(self.allrenders, texts, textinfo, i)
        #     percents.append(percentchange); alltexts.append(texts)

        # self.allrenders,self.selected_stock = drawLatterScroll(screen,player.stocks,self.allrenders,self.bar.value,self.getpoints,(xshift,yshift),self.selected_stock,mousebuttons,DH,alltexts,percents)

        values = [(stock[0].price * stock[2], stock[0].name) for stock in player.stocks]
        names = set([stock[0].name for stock in player.stocks])
        values = [[sum([v[0] for v in values if v[1] == name]), name, stocklist[[s.name for s in stocklist].index(name)].color] for name in names]

        self.renderedback,self.renderedpietexts = draw_pie_chart(screen, values, 150,(1010, 115),self.renderedback,self.renderedpietexts)
