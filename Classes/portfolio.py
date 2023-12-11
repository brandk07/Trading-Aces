import pygame
import timeit
from Defs import fontlist,point_in_polygon
from Classes.imports.Menu import Menu
from pygame import gfxdraw
from Classes.imports.Bar import SliderBar
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
        self.portfoliotext = fontlist[36].render('Portfolio',(255,255,255))[0]
        self.menudrawn = True

        
    def getpoints(self, w1, w2, w3, x, y):
        """returns the points for the polygon of the portfolio menu""" 
        # top left, top right, bottom right, bottom left
        p1 = ((DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + x + w1 + 25, DY + DH + y), (DX + x + w1 + 10, DY + y))
        p2 = [(DX + 10 + x + w1, DY + y), (DX + 25 + x +w1, DY + DH + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 10 + w1 + w2 + x, DY + y)]
        p3 = [(DX + 10 + w1 + w2 + x, DY + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]
        total = [(DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]

        return [p1, p2, p3, total]

    def draw_pie_chart(self, screen: pygame.Surface, stocklist: list, player):
        """Draws the pie chart for the portfolio menu."""
        # get the total value of the stocks
        totalvalue = sum([stock[0].price * stock[2] for stock in player.stocks])
        # get the percentage of each stock
        percentages = [round((stock[0].price * stock[2]) / totalvalue, 2) for stock in player.stocks]
        

    def draw_menu_content(self, screen: pygame.Surface, Mousebuttons: int, stocklist: list, player):
        mousex, mousey = pygame.mouse.get_pos()
        xshift = 14
        yshift = 150    

        self.bar.changemaxvalue(len(player.stocks))

        barheight = 520//len(player.stocks) if len(player.stocks) > 0 else 1

        self.bar.draw_bar(screen, [225, DY], [45, DY + (yshift*4) - 80], 'vertical', barwh=[42, barheight], shift=80, reversedscroll=True, text=True)
        
        self.draw_pie_chart(screen, stocklist, player)

        for i,stock in enumerate([(stock) for i,stock in enumerate(player.stocks) if i >= self.bar.value and i < self.bar.value+5]):# draws the stock graph bar
            
            percentchange = ((stock[0].price - stock[1]) / stock[1]) * 100
            if percentchange > 0:
                grcolor = (0, 200, 0)
            elif percentchange == 0:
                grcolor = (200, 200, 200)
            else:
                grcolor = (225, 0, 0)

            # Rendering all the text
            nametext = fontlist[45].render(f'{stock[0]} X {stock[2]}', (190, 190, 190))[0]
            twidth = nametext.get_width() + 25

            boughttext = fontlist[35].render(f'Paid Price: ${stock[1]*stock[2]:,.2f}', grcolor)[0]
            pricetext = fontlist[35].render(f'Price: ${stock[0].price*stock[2]:,.2f}', grcolor)[0]
            twidth2 = max(boughttext.get_width(), pricetext.get_width()) + 30

            profittext = fontlist[35].render(f'Profit/Loss: ${stock[0].price - stock[1]:,.2f}', grcolor)[0]
            percenttext = fontlist[35].render(f'Change %: {percentchange:,.2f}%', grcolor)[0]
            twidth3 = max(profittext.get_width(), percenttext.get_width()) + 45
            
            # find the points for the polygons
            points,points2,points3,totalpolyon = self.getpoints(twidth, twidth2, twidth3, (i * xshift), (i * yshift))

            # check if the mouse is hovering over the polygon
            hover = False
            if point_in_polygon((mousex, mousey), totalpolyon):  # check if mouse is inside the polygon
                hover = True

            polycolor = (30, 30, 30) if not hover else (60, 60, 60)

            # ----------draw the polygons----------
            gfxdraw.filled_polygon(screen, points, polycolor)  # draws the first polygon with the name of the stock
            gfxdraw.filled_polygon(screen, points2, (polycolor))  # draws the second polygon with the price of the stock
            gfxdraw.filled_polygon(screen, points3, (polycolor))  # draws the third polygon with the profit of the stock


            # ----------Draw the text----------
            screen.blit(nametext, (320 + (i * xshift), 235 + (i * yshift)))  # display name of stock
            screen.blit(boughttext, (330 + (i * xshift) + twidth, 210 + (i * yshift)))# display bought price of stock
            screen.blit(pricetext, (345 + (i * xshift) + twidth, 265 + (i * yshift)))# display current price of stock
            screen.blit(profittext, (330 + twidth + twidth2 + (i * xshift), 210 + (i * yshift)))# display profit of stock
            screen.blit(percenttext, (345 + twidth + twidth2 + (i * xshift), 265 + (i * yshift)))# display percent change of stock
            
            # top left, top right, bottom right, bottom left
            bottom_polygon = [[totalpolyon[0][0]+12, totalpolyon[0][1] + DH - 15], 
                                [totalpolyon[1][0], totalpolyon[1][1]], 
                                [totalpolyon[2][0], totalpolyon[2][1]], 
                                [totalpolyon[3][0], totalpolyon[3][1]],
                                [totalpolyon[3][0]-15, totalpolyon[3][1]],
                                [totalpolyon[3][0]-3, totalpolyon[3][1] + DH - 15],
                              ]
            if hover:
                if percentchange > 0:
                    bottomcolor = (0, 200, 0)
                elif percentchange == 0:
                    bottomcolor = (200, 200, 200)
                else:
                    bottomcolor = (200, 0, 0)
            else:
                if percentchange > 0:
                    bottomcolor = (0, 80, 0)
                elif percentchange == 0:
                    bottomcolor = (110, 110, 110)
                else:
                    bottomcolor = (80, 0, 0)

            pygame.draw.polygon(screen, bottomcolor, bottom_polygon)

            pygame.draw.polygon(screen, (0, 0, 0), points, 5)  # draw the outline of the polygon
            pygame.draw.polygon(screen, (0, 0, 0), points2, 5)  # draw the outline of the second polygon
            pygame.draw.polygon(screen, (0, 0, 0), points3, 5)  # draw the outline of the third polygon