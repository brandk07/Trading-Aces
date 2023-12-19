import pygame
import timeit
from Defs import fontlist,point_in_polygon,closest_point,draw_pie_chart,limit_digits
from Classes.imports.Menu import Menu
from pygame import gfxdraw
from Classes.imports.Bar import SliderBar
from Classes.Stockbook import quantityControls
import math

DX = 300
DY = 200
DH = 120
class Portfolio(Menu):
    def __init__(self):
        super().__init__(r'Assets\Portfolio\portfolio.png',(30,340))
        # self.icon = pygame.image.load(r'Assets\Portfolio\portfolio2.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon,(140,100))
        # remove all the white from the image
        self.bar = SliderBar((0,0),50,[(0,120,0),(110,110,110)])
        self.bar.value = 0
        self.icon.set_colorkey((255,255,255))
        self.portfoliotext = fontlist[65].render('Portfolio',(220,220,220))[0]
        self.menudrawn = True
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
           
            # draw a trapozid using gfxdraw.filled_polygon from 1050,565 to 1529,925
            gfxdraw.filled_polygon(screen, [(1050, 565), (1530, 565), (1565, 925), (1085, 925)], (30, 30, 30))
            pygame.draw.polygon(screen, (0, 0, 0), [(1050, 565), (1530, 565), (1565, 925), (1085, 925)], 5)
            self.quantity = quantityControls(screen,mousebuttons,player.stocks[stockindex][2],self.quantity,(1100,610))
            # draw the stock name
            if len(self.allrenders[stockindex]) < 1:
                text = fontlist[45].render(f'{stock[0]} X {limit_digits(stock[2],10,False)}', (190, 190, 190))[0]
            else:   
                text = self.allrenders[stockindex][f'{stock[0]} X {limit_digits(stock[2],10,False)}']
                
            screen.blit(text, (1060, 575))
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
        mousex, mousey = pygame.mouse.get_pos()
        xshift = 14
        yshift = 150    
        if len(self.allrenders) < len(player.stocks):
            for i in range((len(player.stocks)-len(self.allrenders))+1):
                self.allrenders.append({})
        self.bar.scroll(mousebuttons)
        self.bar.changemaxvalue(len(player.stocks) if len(player.stocks) > 0 else 1)

        barheight = 520//len(player.stocks) if len(player.stocks) > 0 else 1

        self.bar.draw_bar(screen, [225, DY], [45, DY + (yshift*4) - 80], 'vertical', barwh=[43, barheight], shift=85, reversedscroll=True, text=False)
        
        screen.blit(self.portfoliotext,(220,120))

        self.drawSelectedStock(screen, self.selected_stock, mousebuttons, player)

        for i,stock in enumerate([(stock) for i,stock in enumerate(player.stocks) if i >= self.bar.value and i < self.bar.value+5]):# draws the stock graph bar
            ioffset = i+self.bar.value

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
            for x, text in enumerate(texts):
                if text in self.allrenders[i]:
                    render = self.allrenders[i][text]  # reuse old renders if possible
                    self.allrenders[i].pop(text)  # remove the text from the recentrenders
                    self.allrenders[i][text] = render  # add the text back to the recentrenders - so it is at the end of the dict (doesn't get deleted)
                else:  # if the text is not in the recentrenders or recent renders doesn't have enough texts
                    render = fontlist[textinfo[x][1]].render(text, textinfo[x][0])[0]  # render the text
                    self.allrenders[i][text] = render  # add the text to the recentrenders
            for text in list(self.allrenders[i].keys()):
                if text not in texts:
                    self.allrenders[i].pop(text)

            twidth = self.allrenders[i][texts[0]].get_width() + 25
            twidth2 = max(self.allrenders[i][texts[1]].get_width(), self.allrenders[i][texts[2]].get_width()) + 30
            twidth3 = max(self.allrenders[i][texts[3]].get_width(), self.allrenders[i][texts[4]].get_width()) + 45
            
            # find the points for the polygons
            points,points2,points3,totalpolyon = self.getpoints(twidth, twidth2, twidth3, (i * xshift), (i * yshift))

            # check if the mouse is hovering over the polygon
            hover = False
            if point_in_polygon((mousex, mousey), totalpolyon):  # check if mouse is inside the polygon
                hover = True
                if mousebuttons == 1:
                    self.selected_stock = ioffset

            polycolor = (30, 30, 30) if not hover else (80, 80, 80)
            # polycolor = (60, 60, 60) if self.selected_stock == ioffset else polycolor


            # ----------draw the polygons----------
            gfxdraw.filled_polygon(screen, points, polycolor)  # draws the first polygon with the name of the stock
            gfxdraw.filled_polygon(screen, points2, (polycolor))  # draws the second polygon with the price of the stock
            gfxdraw.filled_polygon(screen, points3, (polycolor))  # draws the third polygon with the profit of the stock


            # ----------Draw the text----------
            screen.blit(self.allrenders[i][texts[0]], (320 + (i * xshift), 235 + (i * yshift)))  # display name of stock
            screen.blit(self.allrenders[i][texts[1]], (330 + (i * xshift) + twidth, 210 + (i * yshift)))# display bought price of stock
            screen.blit(self.allrenders[i][texts[2]], (345 + (i * xshift) + twidth, 265 + (i * yshift)))# display current price of stock
            screen.blit(self.allrenders[i][texts[3]], (330 + twidth + twidth2 + (i * xshift), 210 + (i * yshift)))# display profit of stock
            screen.blit(self.allrenders[i][texts[4]], (345 + twidth + twidth2 + (i * xshift), 265 + (i * yshift)))# display percent change of stock
            
            # top left, top right, bottom right, bottom left
            bottom_polygon = [[totalpolyon[0][0]+12, totalpolyon[0][1] + DH - 15], 
                                [totalpolyon[1][0], totalpolyon[1][1]], 
                                [totalpolyon[2][0], totalpolyon[2][1]], 
                                [totalpolyon[3][0], totalpolyon[3][1]],
                                [totalpolyon[3][0]-15, totalpolyon[3][1]],
                                [totalpolyon[3][0]-3, totalpolyon[3][1] + DH - 15],
                              ]
            if hover or self.selected_stock == ioffset:
                if percentchange > 0:bottomcolor = (0, 200, 0)
                elif percentchange == 0:bottomcolor = (200, 200, 200)
                else:bottomcolor = (200, 0, 0)
            else:
                if percentchange > 0: bottomcolor = (0, 80, 0)
                elif percentchange == 0: bottomcolor = (110, 110, 110)
                else: bottomcolor = (80, 0, 0)

            pygame.draw.polygon(screen, bottomcolor, bottom_polygon)
            outlinecolor = (0, 0, 0) if self.selected_stock != ioffset else (200, 200, 200)
            pygame.draw.polygon(screen, outlinecolor, points, 5)  # draw the outline of the polygon
            pygame.draw.polygon(screen, outlinecolor, points2, 5)  # draw the outline of the second polygon
            pygame.draw.polygon(screen, outlinecolor, points3, 5)  # draw the outline of the third polygon
        if not player.stocks:# if the player has no stocks
            text = fontlist[65].render('You have no stocks', (190, 190, 190))[0]
            screen.blit(text, (320, 235))
        values = [(stock[0].price * stock[2], stock[0].name) for stock in player.stocks]
        names = set([stock[0].name for stock in player.stocks])
        values = [[sum([v[0] for v in values if v[1] == name]), name] for name in names]

        self.renderedback,self.renderedpietexts = draw_pie_chart(screen, values, 150,(1050, 200),self.renderedback,self.renderedpietexts)
