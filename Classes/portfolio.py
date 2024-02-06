import pygame
import timeit
from Defs import *
from Classes.imports.Menu import Menu
from pygame import gfxdraw
from Classes.imports.Bar import SliderBar
from Classes.imports.Latterscroll import *
from Classes.Stockbook import quantityControls
from Classes.imports.Numpad import Numpad
from Classes.Stock import Stock
from Classes.imports.StockOption import StockOption


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
        self.showingtext = fontlist[35].render('Displaying ',(220,220,220))[0]
        self.menudrawn = True
        self.allrenders = []
        self.selected_asset = None

        # for the asset type selection which sorts the latterscroll
        # self.assetoptions = ["Stocks","Options","Other"]# future, Crypto, bonds, minerals, real estate, etc
        self.assetoptions = ["Stocks","Options","Other"]
        self.displayed_asset_type = ["Stocks","Options","Other"]


        # self.latterScrollsurf = pygame.Surface((730,730))
        self.latterscroll = PortfolioLatter()
        self.numpad = Numpad()

        presize = 35
        self.prerenders = {
            'Profit': s_render('Profit',presize,(190,190,190)),# text for the profit/loss
            'Lost': s_render('Lost',presize,(190,190,190)),# text for the profit/loss
            'Bought at $': s_render('Bought at $',presize,(190,190,190)),
            'per share': s_render('per share',presize,(190,190,190)),
            'Current Price $': s_render('Current Price $',presize,(190,190,190)),
            'Price': s_render('Price',presize,(190,190,190)),
            '(Per Share)': s_render('(Per Share)',presize,(190,190,190)),
            'Shares': s_render('Shares',presize,(190,190,190)),
            'Paid': s_render('Paid',presize,(190,190,190)),
            'Net Gain': s_render('Net Gain',presize,(190,190,190)),
            'Net Loss': s_render('Net Loss',presize,(190,190,190)),
        }
 
        
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
                    self.selected_asset = None
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


        # screen.blit(s_render("Scroll to see more", 35, (190, 190, 190)), (1600, 950))
    
    # def drawSelected(self, screen, mousebuttons, player):
    #     if self.selected_asset != None:
    #         mousex, mousey = pygame.mouse.get_pos()
    #         #  draw a polygon from 815,110 to 1480,960
    #         points = [(810, 105), (1490, 105), (1490, 960), (810, 960)]
    #         # gfxdraw.filled_polygon(screen, points, (20, 20, 20, 190))
    #         pygame.draw.polygon(screen, (0, 0, 0), points, 5)


    #         percent = ((self.selected_asset[0].price/self.selected_asset[1])-1)

    #         # lostprotext = s_render('Profit' if percent >= 0 else 'Lost',45,(190,190,190))
    #         # screen.blit(lostprotext,(815,110))# display the portfolio text
    #         # percenttext = s_render(f'{limit_digits(percent,15)}%',45,(190,190,190))
    #         # screen.blit(percenttext,(820+lostprotext.get_width(),110))# display the portfolio text

    #         # pricetext = s_render(f'${limit_digits(self.selected_asset[0].price*self.selected_asset[2],15)}',45,(190,190,190))
    #         # screen.blit(pricetext,(1480-pricetext.get_width(),110))# display the portfolio text
            
    #         texts = [
    #             self.prerenders['Profit'] if percent >= 0 else self.prerenders['Lost'],# text for the profit/loss
    #             s_render(f'${limit_digits(percent,15)}%',35,(190,190,190)),# text for the percent
    #             s_render(f'${limit_digits(self.selected_asset[1]*self.selected_asset[2],15)}',45,(190,190,190)),# text for the total paid
    #             self.prerenders["Bought at $"],# text for the "bought at" text
    #             s_render(str(limit_digits(self.selected_asset[1],15)),35,(190,190,190)),
    #             self.prerenders["per share"],# text for the "per share" text
    #             self.prerenders["Current Price $"],# text for the "current price" text
    #             s_render(str(limit_digits(self.selected_asset[0].price,15)),35,(190,190,190)),
    #         ]
    #         coords = [
    #             (815,110),# coords for the profit/loss
    #             (820+texts[0].get_width(),110),# coords for the percent
    #             (1480-texts[1].get_width(),110),# coords for the total paid
    #             (820,465),# coords for the "bought at" text
    #             (820+texts[3].get_width(),465),# coords for the price text
    #             (830+texts[3].get_width()+texts[4].get_width(),465),# coords for the "per share" text
    #             (820,515),# coords for the "current price" text
    #             (820+texts[6].get_width(),515),# coords for the current price text
    #         ]
    #         for text,coord in zip(texts,coords):
    #             screen.blit(text,coord)# display all the texts


    #         self.selected_asset[0].baredraw(screen,(820,155),(660,295),'1M',True)

    #         self.numpad.draw(screen,(820,675),(300,275),'SHARE' if self.numpad.value == 1 else 'SHARES',mousebuttons,self.selected_asset[2])
    #         self.draw_selectedpriceInfo(screen,player)

    # def draw_selectedpriceInfo(self,screen,player):
    #     """All the price info next to the numpad for the selected stock"""
    #     # (820,675),(300,275)
    #     # draw the stock name

    #     # screen.blit(s_render(f'{stock[0]} X {limit_digits(stock[2],10,False)}', 50, (190, 190, 190)), (1040, 435))
    #     h1 = self.prerenders["Price"].get_height()
    #     h2 = self.prerenders["(Per Share)"].get_height()
    #     coords = [
    #         (1130, 680),# coords for the Price text
    #         (1145, 690+h1),# coords for the "(per share)" text
    #         (1130, 705+h1+h2)# coords for the "Shares x" text
    #         # (1130, 860)# coords for the "Paid" text
    #     ]

    #     totalheight = h1+h2+self.prerenders["Shares"].get_height()+15
    #     # paidvalue = s_render(f'${limit_digits(self.selected_asset[1]*self.numpad.get_value(),15)}', 45, (190, 190, 190))
    #     value = s_render(f'${limit_digits(self.selected_asset[0].price*self.numpad.get_value(),15)}', 45, (190, 190, 190))

    #     points = [(1125, 675), (1125, 715+totalheight+value.get_height()), (1480, 715+totalheight+value.get_height()), (1480, 675)]
    #     # gfxdraw.filled_polygon(screen, points, (80,80,80,120))# background for the value info
    #     pygame.draw.polygon(screen, (0, 0, 0), points, 3)

    #     for i,text in enumerate(["Price","(Per Share)","Shares"]):
    #         screen.blit(self.prerenders[text],coords[i])
        
    #     gfxdraw.line(screen, 1130, 705+totalheight, 1475, 705+totalheight, (190,190,190))

    #     # draw the price of the stock
    #     price = s_render(f'${limit_digits(self.selected_asset[0].price,15)}', 45, (190, 190, 190)) 
    #     screen.blit(price, (1475-price.get_width(),680))

    #     # draw the amount of shares
    #     shares = s_render(f'{self.numpad.get_value():,.0f}', 45, (190, 190, 190))
    #     screen.blit(shares, (1475-shares.get_width(),695+h1+h2))

    #     # draw the total value
    #     screen.blit(value, (1475-value.get_width(),715+totalheight))

    #     strtext = "Net Gain" if self.selected_asset[0].price > self.selected_asset[1] else "Net Loss"
    #     screen.blit(self.prerenders[strtext],(1130, 860))
    #     color = ((0,200,0) if self.selected_asset[0].price > self.selected_asset[1] else (200,0,0)) if self.selected_asset[0].price != self.selected_asset[1] else (190,190,190)
    #     netchange = s_render(f'${limit_digits((self.selected_asset[0].price - self.selected_asset[1])*self.numpad.get_value(),15)}', 45, color)
    #     screen.blit(netchange, (1475-netchange.get_width(),860))
    def draw_assetscroll(self,sortedassets,screen,mousebuttons):
        # asset is the class name (the class should have a str method that returns the name of the asset)

        # asset is [class, ogvalue:float, secondary text:str, value:float, percent:float]
        # function to get the text for each asset
        get_text = lambda classobj,secondtext,value : [f'{classobj} ',
                                    # f"{limit_digits(asset[2],10,False)} Share{'' if asset[2] == 1 else 's'}",
                                    secondtext,
                                    f'${limit_digits(value,15)}',]
        # getting the text for each asset
        textlist = [get_text(classobj,secondtext,value) for [classobj,ogvalue,secondtext,value,percent] in sortedassets]# stores 3 texts for each asset in the sortedassets list

        textinfo = []# stores the text info for the latter scroll [text,fontsize,color]
        coords = [[(20,15),(25,60)] for i in range(len(textlist))]
        # loop through the textlist and store the text info in the textinfo list
        for i,(text,[classobj,ogvalue,secondtext,value,percent]) in enumerate(zip(textlist,sortedassets)):
            polytexts = []# temporary list to store the text info for each asset
            polytexts.append([text[0],50,classobj.color])
            polytexts.append([text[1],35,(190,190,190)])
            polytexts.append([text[2],60,(190,190,190)])
            textinfo.append(polytexts)
            coords[i].append(((text[1],100),30))

        self.latterscroll.storetextinfo(textinfo)# simply changes the self.texts in latterscroll
        self.latterscroll.set_textcoords(coords)# simply changes the self.textcoords in latterscroll
        # Does most of the work for the latter scroll, renders the text and finds all the coords
        scrollmaxcoords = (500,960)
        ommitted = self.latterscroll.store_rendercoords((875, 200), scrollmaxcoords,135,0,0,updatefreq=60)

        # drawing the latter scroll and assigning the selected asset
        selectedindex = None if self.selected_asset == None else [asset[:2] for asset in sortedassets].index(self.selected_asset)# gets the index of the selected asset only uses the first 2 elements of the asset (the class and the ogvalue)
        newselected = self.latterscroll.draw_polys(screen, (875, 200), mousebuttons, selectedindex, *[asset[3] for asset in sortedassets])# draws the latter scroll and returns the selected asset
        if newselected == None:
            self.selected_asset = None
        else:# if the selected asset is not None
            self.selected_asset = sortedassets[newselected][:2]

        # make a text saying showing # out of # assets
        screen.blit(self.showingtext,(980,950))
        currenttext = s_render(f'{ommitted[0]} - {ommitted[1]-1}',35,(220,220,220))
        outoftext = s_render(f' out of {len(sortedassets)}',35,(220,220,220))

        screen.blit(currenttext,(980+self.showingtext.get_width(),950))

        screen.blit(outoftext,(980+self.showingtext.get_width()+currenttext.get_width(),950))

    def assetscroll_controls(self,screen,mousebuttons):
        """Controls for the asset scroll"""
        screen.blit(s_render("My Assets", 45, (210, 210, 210)), (880, 100))
        
        width = 500//len(self.assetoptions)
        for i,option in enumerate(self.assetoptions):
            x,y = 880+(i*width),160
            rect = pygame.Rect(x,y,width-5,35)
            color = (120,120,120)
            if rect.collidepoint(pygame.mouse.get_pos()):
                color = (160,160,160)
                if mousebuttons == 1:
                    if option in self.displayed_asset_type:
                        self.displayed_asset_type.remove(option)
                    else:
                        self.displayed_asset_type.append(option)

            pygame.draw.rect(screen, color, rect, width=3,border_radius=10)
            pygame.draw.rect(screen, (0,0,0), [x+10,y+10,15,15], 3)
            # rectangle inside the one above
            if option in self.displayed_asset_type:
                pygame.draw.rect(screen, (200,200,200), [x+13,y+13,9,9])
            screen.blit(s_render(option, 30, (210, 210, 210)), (x+34,y+8))

    def get_allassets(self,player) -> list:
        """returns a sorted list of the currently displayed assets of the player"""
        def get_second(asset):
            if isinstance(asset,list) and isinstance(asset[0],Stock):
                return f"{limit_digits(asset[1],10,False)} Share{'' if asset[1] == 1 else 's'}"
            elif isinstance(asset,StockOption):
                return f"{asset} Option"
        def get_percent(asset):
            if isinstance(asset,list) and isinstance(asset[0],Stock):
                return ((asset[0].price - asset[1]) / asset[1]) * 100
            elif isinstance(asset,StockOption):
                return ((asset.get_value() - asset.ogvalue) / asset.ogvalue) * 100
            
        # asset is [class, ogvalue:float, secondary text:str, value:float, percent:float]
        stockassets,optionassets = [],[]
        if "Stocks" in self.displayed_asset_type:
            stockassets = [[stock[0],stock[1] ,get_second(stock),stock[0].price*stock[2],get_percent(stock)] for stock in player.stocks]
        if "Options" in self.displayed_asset_type:
            optionassets = [[option, option.ogvalue, get_second(option),option.get_value(),get_percent(option)] for option in player.options]
        allassets = stockassets + optionassets 
        # sortedstocks = sorted(player.stocks,key=lambda stock: stock[0].price*stock[2],reverse=True)
        return sorted(allassets,key=lambda asset: asset[3],reverse=True)

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player):
        """Draws all of the things in the portfolio menu"""
        mousex, mousey = pygame.mouse.get_pos()
        
        sortedassets = self.get_allassets(player)
        if self.selected_asset != None and self.selected_asset not in [asset[:2] for asset in sortedassets]:
            if len(sortedassets) > 0:
                self.selected_asset = sortedassets[0][:2]
            else:
                self.selected_asset = None

        if len(self.allrenders) < len(player.stocks):# if the player has more stocks than the renders
            for i in range((len(player.stocks)-len(self.allrenders))+1):# add the amount of renders needed
                self.allrenders.append({})
       
        player.draw(screen,player,(200,100),(650,500),mousebuttons,stocklist,True)
        
        if len(sortedassets) > 0:
            # draws the stocks on the right of the screen
            self.draw_assetscroll(sortedassets,screen,mousebuttons)
        self.assetscroll_controls(screen,mousebuttons)

            # draws the selected stock information in the middle of the screen
            # self.drawSelected(screen, mousebuttons, player)

        values = [(stock[0].price * stock[2], stock[0].name) for stock in player.stocks]
        names = set([stock[0].name for stock in player.stocks])
        values = [[sum([v[0] for v in values if v[1] == name]), name, stocklist[[s.name for s in stocklist].index(name)].color] for name in names]

        draw_pie_chart(screen, values, 150,(200, 650))

