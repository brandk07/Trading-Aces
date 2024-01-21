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
        # screen.blit(self.sharebackground,(1425,100))
            
        sortedstocks = sorted(player.stocks,key=lambda stock: stock[0].price*stock[2],reverse=True)

        if len(self.allrenders) < len(player.stocks):# if the player has more stocks than the renders
            for i in range((len(player.stocks)-len(self.allrenders))+1):# add the amount of renders needed
                self.allrenders.append({})

        if self.selected_stock == None and len(player.stocks) > 0:
            self.selected_stock = sortedstocks[0]
       

        player.draw(screen,player,(800,100),(200,600),stocklist,mousebuttons,True)
        
        # self.bar.draw_bar(screen, [1450, 100], [20, 880], 'vertical', barwh=[20, 65], reversedscroll=True, text=False)
        # scroll controls 
        # screen.blit(self.portfoliotext,(220,120))# display the portfolio text

        # self.drawSelectedStock(screen, self.selected_stock, mousebuttons, player)# draws the additional stock info

        # screen.blit(self.showingtext,(300,190))# display the showing text
        # shownnumtext = fontlist[45].render(f'{self.bar.value+1} - {self.bar.value+5 if self.bar.value+5 < len(player.stocks) else len(player.stocks)} of {len(player.stocks)}', (190, 190, 190))[0]
        # screen.blit(shownnumtext, (self.showingtext.get_width()+300, 190))
        

        # disamt = 6# the amount of stocks to display
        # slicedstocks = sortedstocks[self.scrollvalue:self.scrollvalue+disamt]
        # if self.selected_stock != None:
        #     if self.scrollvalue > sortedstocks.index(self.selected_stock) and self.scrollvalue < len(sortedstocks):# if the selected stock is above what is displayed
        #         self.selected_stock = sortedstocks[self.scrollvalue]# select the highest stock being displayed
        #     elif self.scrollvalue+disamt-1 < sortedstocks.index(self.selected_stock) and self.scrollvalue+disamt-1 < len(sortedstocks):# if the selected stock is below what is displayed
        #         self.selected_stock = sortedstocks[self.scrollvalue+disamt-1]# select the lowest stock being displayed
        get_text = lambda stock : [f'{stock[0]} ',
                                    f"{limit_digits(stock[2],10,False)} Share{'' if stock[2] == 1 else 's'}",
                                    f'${limit_digits(stock[0].price*stock[2],15)}',
                                ]
        
         
        textlist = [get_text(stock) for stock in sortedstocks]# stores 3 texts for each stock in the sortedstocks list

        textinfo = []
        coords = [[(20,15),(25,60)] for i in range(len(textlist))]
        # print(coords)
        for i,(text,stock) in enumerate(zip(textlist,sortedstocks)):
            polytexts = []

            polytexts.append([text[0],50,stock[0].color])
            polytexts.append([text[1],35,(190,190,190)])
            polytexts.append([text[2],45,(190,190,190)])
            textinfo.append(polytexts)
            coords[i].append(((text[1],50),30))

        self.latterscroll.storetextinfo(textinfo)
        self.latterscroll.set_textcoords(coords)

        self.latterscroll.store_rendercoords((1500, 105), 800,110,0,10,0)
        sindex = sortedstocks.index(self.selected_stock)
        self.selected_stock = sortedstocks[self.latterscroll.draw_polys(screen, (1500, 105), mousebuttons, sindex, *sortedstocks)]

        screen.blit(s_render(self.selected_stock[0].name,50,(255,255,255)),(815,110))# display the portfolio text

        # if sortedstocks:# if the player has stocks
        #     for i,stock in enumerate(sortedstocks):
        #         #all the texts to be rendered
        #         texts = [f'{stock[0]} ',
        #                     f"{limit_digits(stock[2],10,False)} Share{'' if stock[2] == 1 else 's'}",
        #                     f'${limit_digits(stock[0].price*stock[2],15)}',
        #                 ]
        #         # all the coords for the texts to be rendered
        #         coords = [(20,15),(25,60),((texts[1],50),30)]
        #         colors = [stock[0].color,(190,190,190),(190,190,190)]

        #         finaldict = {}
        #         for ind,text in enumerate(texts):
        #             finaldict[text] = (coords[ind][0],coords[ind][1],[50,35,45][ind],colors[ind])

        #         self.latterscroll.storeTextsVariable(resetlist=(i == 0),extraspace=20,**finaldict)

        #     if self.selected_stock != None:
        #         spot = sortedstocks.index(self.selected_stock)-self.scrollvalue
        #     else:
        #         spot = None
            

        #     self.selected_stock = self.latterscroll.draw_polys(screen, (1500, 105), 1505, 110, mousebuttons, spot, 0,10,True,*sortedstocks)
        #     if self.selected_stock != None:
        #         self.selected_stock = sortedstocks[self.selected_stock]

            # self.latterscroll.draw_stockgraph(screen,sortedstocks[self.bar.value:self.bar.value+7])
            

        values = [(stock[0].price * stock[2], stock[0].name) for stock in player.stocks]
        names = set([stock[0].name for stock in player.stocks])
        values = [[sum([v[0] for v in values if v[1] == name]), name, stocklist[[s.name for s in stocklist].index(name)].color] for name in names]

        draw_pie_chart(screen, values, 150,(200, 650))

# import pygame
# import timeit
# from Defs import *
# from Classes.imports.Menu import Menu
# from pygame import gfxdraw
# from Classes.imports.Bar import SliderBar
# from Classes.imports.Latterscroll import *
# from Classes.Stockbook import quantityControls
# import math

# DX = 300# default x
# DY = 230# default y
# DH = 120# default height
# class Portfolio(Menu):
#     def __init__(self):
#         self.icon = pygame.image.load(r'Assets\Menu_Icons\portfolio.png').convert_alpha()
#         self.icon = pygame.transform.scale(self.icon,(140,100))
#         self.icon.set_colorkey((255,255,255))
#         super().__init__(self.icon)
#         # remove all the white from the image
#         # self.bar = SliderBar(50,[(150,150,150),(10,10,10)],barcolor=((20,130,20),(40,200,40)))
#         # self.bar.value = 0
#         self.scrollvalue = 0
#         self.quantitybar = SliderBar(50,[(150,150,150),(10,10,10)],barcolor=((20,130,20),(40,200,40)))

#         self.sharebackground = pygame.image.load(r"Assets\backgrounds\Background (8).png").convert_alpha()
#         self.sharebackground = self.sharebackground.subsurface((0,0,485,880))
#         self.sharebackground.set_alpha(150)

#         self.portfoliotext = fontlist[65].render('Owned Shares',(220,220,220))[0]
#         self.showingtext = fontlist[45].render('Showing ',(220,220,220))[0]
#         self.menudrawn = True
#         self.allrenders = []
#         self.selected_stock = None

#         # self.latterScrollsurf = pygame.Surface((730,730))
#         self.latterscroll = PortfolioLatter()

        
#     def getpoints(self, w1, w2, w3, x, y):
#         """returns the points for the polygon of the portfolio menu""" 
#         # top left, top right, bottom right, bottom left
#         p1 = ((DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + x + w1 + 25, DY + DH + y), (DX + x + w1 + 10, DY + y))
#         p2 = [(DX + 10 + x + w1, DY + y), (DX + 25 + x +w1, DY + DH + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 10 + w1 + w2 + x, DY + y)]
#         p3 = [(DX + 10 + w1 + w2 + x, DY + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]
#         total = [(DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]

#         return [p1, p2, p3, total]
    
#     def drawSelectedStock(self, screen, stock, mousebuttons, player):
#         if stock != None:
#             mousex, mousey = pygame.mouse.get_pos()
           
#             gfxdraw.filled_polygon(screen, [(1030, 425), (1505, 425), (1565, 925), (1085, 925)], (30, 30, 30))
#             pygame.draw.polygon(screen, (0, 0, 0), [(1030, 425), (1505, 425), (1565, 925), (1085, 925)], 6)
#             # self.quantity = quantityControls(screen,mousebuttons,stock[2],self.quantity,(1100,610))
#             self.quantitybar.changemaxvalue(stock[2])
#             self.quantitybar.draw_bar(screen,[1100,700],[300,35],'horizontal',reversedscroll=True)
#             # draw the stock name

#             # text = fontlist[50].render(f'{stock[0]} X {limit_digits(stock[2],10,False)}', (190, 190, 190))[0]
#             screen.blit(s_render(f'{stock[0]} X {limit_digits(stock[2],10,False)}', 50, (190, 190, 190)), (1040, 435))# display the stock name

#             sellpoints = [(1110, 840), (1125, 910), (1465, 910), (1450, 840)]
#             # use the same system found in the stockbook class to draw the sell button and the selector for the amount of stocks to sell
#             if point_in_polygon((mousex,mousey),sellpoints):
#                 sellcolor = (150,0,0)
#                 if mousebuttons == 1:
#                     player.sell(stock[0],stock[1],int(self.quantitybar.value))
#                     self.selected_stock = None
#                     self.quantitybar.value = 0
#             else:
#                 sellcolor = (225,225,225)

#             # Draws the information about the stock on the right side of the screen 
#             info = [f'Paid Price: ${limit_digits(stock[1]*stock[2],12)}',f'Paid ${limit_digits(stock[1],12)} | Current ${limit_digits(stock[0].price,12)}',f'{"Profit" if (stock[0].price - stock[1])*stock[2] > 0 else "Loss"}: ${limit_digits((stock[0].price - stock[1])*stock[2],15)}',f'Change %: {limit_digits(((stock[0].price - stock[1]) / stock[1]) * 100,15)}%']
            
#             for i,txt in enumerate(info):
#                 screen.blit(s_render(txt,35,(130,130,130)),(1050+(i*8),490+(i*50)))

#             # total value of the stocks above the sell button
#             value = stock[0].price * self.quantitybar.value
#             valuetext = s_render(f'Value: ${limit_digits(value,15)}', 45, (190, 190, 190))
#             points = [(1100, 745), (1115, 815), (1455, 815), (1440, 745)]
#             gfxdraw.filled_polygon(screen, points, (15,15,15))
#             pygame.draw.polygon(screen, (0, 0, 0), points, 5)
#             screen.blit(valuetext, (1115, 765))

#             # sell button
#             gfxdraw.filled_polygon(screen, sellpoints, (15,15,15))
#             pygame.draw.polygon(screen, (0, 0, 0), sellpoints, 5)
#             sell_text = s_render(f'SELL', 65, sellcolor)
#             sell_text_rect = sell_text.get_rect(center=(1280, 875))
#             screen.blit(sell_text, sell_text_rect)
#     def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player):
#         """Draws all of the things in the portfolio menu"""
#         mousex, mousey = pygame.mouse.get_pos()
#         xshift = 15
#         yshift = 150 
#         # screen.blit(self.sharebackground,(1425,100))
            
#         sortedstocks = sorted(player.stocks,key=lambda stock: stock[0].price*stock[2],reverse=True)

#         if len(self.allrenders) < len(player.stocks):# if the player has more stocks than the renders
#             for i in range((len(player.stocks)-len(self.allrenders))+1):# add the amount of renders needed
#                 self.allrenders.append({})

#         if self.selected_stock == None and len(player.stocks) > 0:
#             self.selected_stock = sortedstocks[0]
       

#         player.draw(screen,player,(800,100),(200,600),stocklist,mousebuttons,True)
        
#         # self.bar.draw_bar(screen, [1450, 100], [20, 880], 'vertical', barwh=[20, 65], reversedscroll=True, text=False)
#         # scroll controls 
#         if mousebuttons == 4:
#             self.scrollvalue = max(0,self.scrollvalue-1)
#         elif mousebuttons == 5:
#             self.scrollvalue = min(len(sortedstocks)-6,self.scrollvalue+1)
#         # screen.blit(self.portfoliotext,(220,120))# display the portfolio text

#         # self.drawSelectedStock(screen, self.selected_stock, mousebuttons, player)# draws the additional stock info

#         # screen.blit(self.showingtext,(300,190))# display the showing text
#         # shownnumtext = fontlist[45].render(f'{self.bar.value+1} - {self.bar.value+5 if self.bar.value+5 < len(player.stocks) else len(player.stocks)} of {len(player.stocks)}', (190, 190, 190))[0]
#         # screen.blit(shownnumtext, (self.showingtext.get_width()+300, 190))
        

#         disamt = 6# the amount of stocks to display
#         slicedstocks = sortedstocks[self.scrollvalue:self.scrollvalue+disamt]
#         if self.selected_stock != None:
#             if self.scrollvalue > sortedstocks.index(self.selected_stock) and self.scrollvalue < len(sortedstocks):# if the selected stock is above what is displayed
#                 self.selected_stock = sortedstocks[self.scrollvalue]# select the highest stock being displayed
#             elif self.scrollvalue+disamt-1 < sortedstocks.index(self.selected_stock) and self.scrollvalue+disamt-1 < len(sortedstocks):# if the selected stock is below what is displayed
#                 self.selected_stock = sortedstocks[self.scrollvalue+disamt-1]# select the lowest stock being displayed

#         if slicedstocks:# if the player has stocks
#             for i,stock in enumerate(slicedstocks):
#                 #all the texts to be rendered
#                 texts = [f'{stock[0]} ',
#                             f"{limit_digits(stock[2],10,False)} Share{'' if stock[2] == 1 else 's'}",
#                             f'${limit_digits(stock[0].price*stock[2],15)}',
#                         ]
#                 # all the coords for the texts to be rendered
#                 coords = [(20,15),(25,60),((texts[1],50),30)]
#                 colors = [stock[0].color,(190,190,190),(190,190,190)]

#                 finaldict = {}
#                 for ind,text in enumerate(texts):
#                     finaldict[text] = (coords[ind][0],coords[ind][1],[50,35,45][ind],colors[ind])

#                 self.latterscroll.storeTextsVariable(resetlist=(i == 0),extraspace=20,**finaldict)

#             if self.selected_stock != None:
#                 spot = sortedstocks.index(self.selected_stock)-self.scrollvalue
#             else:
#                 spot = None
            

#             self.selected_stock = self.latterscroll.draw_polys(screen, (1500, 105), 1505, 110, mousebuttons, spot, 0,10,True,*slicedstocks)
#             if self.selected_stock != None:
#                 self.selected_stock = slicedstocks[self.selected_stock]

#             # self.latterscroll.draw_stockgraph(screen,sortedstocks[self.bar.value:self.bar.value+7])
            

#         values = [(stock[0].price * stock[2], stock[0].name) for stock in player.stocks]
#         names = set([stock[0].name for stock in player.stocks])
#         values = [[sum([v[0] for v in values if v[1] == name]), name, stocklist[[s.name for s in stocklist].index(name)].color] for name in names]

#         draw_pie_chart(screen, values, 150,(200, 650))
