import pygame
import timeit
from Defs import *
from Classes.imports.Menu import Menu
from pygame import gfxdraw
from Classes.imports.Bar import SliderBar
from Classes.Stockbook import quantityControls
from Classes.imports.Option import Option
import math

DX = 300
DY = 200
DH = 120
class Optiontrade(Menu):
    def __init__(self):
        
        # self.icon = pygame.image.load(r'Assets\Portfolio\portfolio2.png').convert_alpha()

        self.icon = pygame.image.load(r'Assets\Menu_Icons\bulloption2.png').convert_alpha()
        width = 140
        height = int(width / self.icon.get_width() * self.icon.get_height())
        self.icon = pygame.transform.scale(self.icon, (width, height))
        
        super().__init__(self.icon)
        
        
        self.bar = SliderBar((0,0),50,[(0,120,0),(110,110,110)])
        self.bar.value = 0
        # self.icon.set_colorkey((255,255,255))
        self.optiontext = fontlist[65].render('Options',(220,220,220))[0]
        self.ownedtext = [fontlist[50].render('Owned',(220,220,220))[0],fontlist[50].render('Owned',(0,200,0))[0]]
        self.availabletext = [fontlist[50].render('Available',(220,220,220))[0],fontlist[50].render('Available',(0,200,0))[0]]
        self.putoptions = []
        self.calloptions = []
        self.menudrawn = True
        self.renderedpietexts = None; self.renderedback = None
        self.allrenders = []
        self.selected_option = None; self.quantity = 0
        self.view = "Owned"# Owned or Available
    
        
    def getpoints(self, w1, w2, w3, x, y):
        """returns the points for the polygon of the portfolio menu""" 
        # top left, top right, bottom right, bottom left
        p1 = ((DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + x + w1 + 25, DY + DH + y), (DX + x + w1 + 10, DY + y))
        p2 = [(DX + 10 + x + w1, DY + y), (DX + 25 + x +w1, DY + DH + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 10 + w1 + w2 + x, DY + y)]
        p3 = [(DX + 10 + w1 + w2 + x, DY + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]
        total = [(DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]

        return [p1, p2, p3, total]
    
    def drawSelectedStock(self, screen, optionindex, mousebuttons, player):
        if optionindex != None:
            option = player.options[optionindex]
            mousex, mousey = pygame.mouse.get_pos()
           
            # draw a trapozid using gfxdraw.filled_polygon from 1050,565 to 1529,925
            gfxdraw.filled_polygon(screen, [(1000, 200), (1480, 200), (1565, 925), (1100, 925)], (30, 30, 30))
            pygame.draw.polygon(screen, (0, 0, 0), [(1000, 200), (1480, 200), (1565, 925), (1100, 925)], 5)

            # draw the stock name
            text = fontlist[45].render(f'{option.stockobj.name} Option', (190, 190, 190))[0]
                
            screen.blit(text, (1060, 575))
            # use the same system found in the stockbook class to draw the sell button and the selector for the amount of stocks to sell
            if point_in_polygon((mousex,mousey),[(1110,805),(1125,875),(1465,875),(1450,805)]):
                sellcolor = (150,0,0)
                if mousebuttons == 1:
                    if player.cash > option.price:
                        player.buyOption(option)
            else:
                sellcolor = (225,225,225)

            xshift = 15
            yshift = 100
            text = []   


            # total value of the stocks above the sell button
            # strike_price = option.strike_price
            # text = fontlist[45].render(f'Value: ${limit_digits(value,15)}', (190, 190, 190))[0]
            # gfxdraw.filled_polygon(screen,((1100,705),(1115,775),(1455,775),(1440,705)),(15,15,15))#polygon for the total value button
            # pygame.draw.polygon(screen, (0,0,0), ((1110,705),(1125,775),(1465,775),(1450,705)),5)#outline total value button polygon

            value = option.get_value()
            text = fontlist[45].render(f'Value: ${limit_digits(value,15)}', (190, 190, 190))[0]
            gfxdraw.filled_polygon(screen,((1100,705),(1115,775),(1455,775),(1440,705)),(15,15,15))#polygon for the total value button
            pygame.draw.polygon(screen, (0,0,0), ((1110,705),(1125,775),(1465,775),(1450,705)),5)#outline total value button polygon
            
            screen.blit(text, (1130, 725))
            # sell button
            gfxdraw.filled_polygon(screen,((1110,805),(1125,875),(1465,875),(1450,805)),(15,15,15))#polygon for the sell button
            pygame.draw.polygon(screen, (0,0,0), ((1110,805),(1125,875),(1465,875),(1450,805)),5)#outline sell button polygon
            sell_text, _ = fontlist[65].render(f'SELL', sellcolor)
            sell_text_rect = sell_text.get_rect(center=(1280, 840))
            screen.blit(sell_text, sell_text_rect)

    def draw_Owned(self,screen,mousebuttons,player):
        mousex, mousey = pygame.mouse.get_pos()
        xshift = 15
        yshift = 150    
        if len(self.allrenders) < len(player.options):# if the player has more stocks than the renders
            for i in range((len(player.options)-len(self.allrenders))+1):# add the amount of renders needed
                self.allrenders.append({})
        if self.selected_option == None and len(player.options) > 0:
            self.selected_option = 0
        self.bar.scroll(mousebuttons)# check for the scroll of the bar
        self.bar.changemaxvalue(len(player.options) if len(player.options) > 0 else 1)# change the max value of the bar based on the amount of stocks the player has

        barheight = 520//len(player.options) if len(player.options) > 0 else 1

        self.bar.draw_bar(screen, [225, DY], [45, DY + (yshift*4) - 80], 'vertical', barwh=[43, barheight], shift=85, reversedscroll=True, text=False)

        self.drawSelectedStock(screen, self.selected_option, mousebuttons, player)# draws the additional stock info

        percents = []; alltexts = []
        for i, option in enumerate(player.options[self.bar.value:self.bar.value+5]):
            percentchange = ((option.get_value() - option.ogvalue) / option.ogvalue) * 100
            
            if percentchange > 0:
                grcolor = (0, 200, 0); profittext = "Profit"
                
            elif percentchange == 0:
                grcolor = (200, 200, 200); profittext = ""
            else:
                grcolor = (225, 0, 0); profittext = "Loss"

            textinfo = [[(190, 190, 190), 45],[(190, 190, 190), 35],[grcolor, 35],[grcolor, 35],[grcolor, 35]]

            texts = [f'{option.stockobj.name} {option.option_type}',
                     f'Original Value: ${limit_digits(option.ogvalue,15)}',
                     f'Value: ${limit_digits(option.get_value(),15)}',
                     f'{profittext}: ${limit_digits((option.get_value() - option.ogvalue),15)}',
                     f'Change %: {limit_digits(percentchange,15)}%'
                    ]
            self.allrenders = reuserenders(self.allrenders, texts, textinfo, i)
            percents.append(percentchange); alltexts.append(texts)

        self.allrenders,self.selected_option = drawLatterScroll(screen,player.options,self.allrenders,self.bar.value,self.getpoints,(xshift,yshift),self.selected_option,mousebuttons,DH,alltexts,percents)
        # for i,option in enumerate([(option) for i,option in enumerate(player.options) if i >= self.bar.value and i < self.bar.value+5]):# draws the stock graph bar
            # ioffset = i+self.bar.value

            # percentchange = ((option.get_value() - option.ogvalue) / option.ogvalue) * 100
            
            # if percentchange > 0:
            #     grcolor = (0, 200, 0); profittext = "Profit"
                
            # elif percentchange == 0:
            #     grcolor = (200, 200, 200); profittext = ""
            # else:
            #     grcolor = (225, 0, 0); profittext = "Loss"

            # textinfo = [[(190, 190, 190), 45],[(190, 190, 190), 35],[grcolor, 35],[grcolor, 35],[grcolor, 35]]

            # texts = [f'{option.stockobj.name} {option.option_type}',
            #          f'Original Value: ${limit_digits(option.ogvalue,15)}',
            #          f'Value: ${limit_digits(option.get_value(),15)}',
            #          f'{profittext}: ${limit_digits((option.get_value() - option.ogvalue),15)}',
            #          f'Change %: {limit_digits(percentchange,15)}%'
            #         ]
        #     self.allrenders = reuserenders(self.allrenders, texts, textinfo, i)

        #     twidth = self.allrenders[i][texts[0]].get_width() + 25
        #     twidth2 = max(self.allrenders[i][texts[1]].get_width(), self.allrenders[i][texts[2]].get_width()) + 30
        #     twidth3 = max(self.allrenders[i][texts[3]].get_width(), self.allrenders[i][texts[4]].get_width()) + 45
            
        #     # find the points for the polygons
        #     points,points2,points3,totalpolyon = self.getpoints(twidth, twidth2, twidth3, (i * xshift), (i * yshift))

        #     # check if the mouse is hovering over the polygon
        #     hover = False
        #     if point_in_polygon((mousex, mousey), totalpolyon):  # check if mouse is inside the polygon
        #         hover = True
        #         if mousebuttons == 1:
        #             self.selected_option = ioffset

        #     polycolor = (30, 30, 30) if not hover else (80, 80, 80)
        #     # polycolor = (60, 60, 60) if self.selected_option == ioffset else polycolor

        #     # ----------draw the polygons----------
        #     gfxdraw.filled_polygon(screen, points, polycolor)  # draws the first polygon with the name of the stock
        #     gfxdraw.filled_polygon(screen, points2, (polycolor))  # draws the second polygon with the price of the stock
        #     gfxdraw.filled_polygon(screen, points3, (polycolor))  # draws the third polygon with the profit of the stock

        #     # ----------Draw the text----------
        #     screen.blit(self.allrenders[i][texts[0]], (320 + (i * xshift), 235 + (i * yshift)))  # display name of stock
        #     screen.blit(self.allrenders[i][texts[1]], (330 + (i * xshift) + twidth, 210 + (i * yshift)))# display bought price of stock
        #     screen.blit(self.allrenders[i][texts[2]], (345 + (i * xshift) + twidth, 265 + (i * yshift)))# display current price of stock
        #     screen.blit(self.allrenders[i][texts[3]], (330 + twidth + twidth2 + (i * xshift), 210 + (i * yshift)))# display profit of stock
        #     screen.blit(self.allrenders[i][texts[4]], (345 + twidth + twidth2 + (i * xshift), 265 + (i * yshift)))# display percent change of stock
            
        #     # top left, top right, bottom right, bottom left
        #     bottom_polygon = [[totalpolyon[0][0]+12, totalpolyon[0][1] + DH - 15], 
        #                         [totalpolyon[1][0], totalpolyon[1][1]], 
        #                         [totalpolyon[2][0], totalpolyon[2][1]], 
        #                         [totalpolyon[3][0], totalpolyon[3][1]],
        #                         [totalpolyon[3][0]-15, totalpolyon[3][1]],
        #                         [totalpolyon[3][0]-3, totalpolyon[3][1] + DH - 15],
        #                       ]
        #     if hover or self.selected_option == ioffset:
        #         if percentchange > 0:bottomcolor = (0, 200, 0)
        #         elif percentchange == 0:bottomcolor = (120, 120, 120)
        #         else:bottomcolor = (200, 0, 0)
        #     else:
        #         if percentchange > 0: bottomcolor = (0, 80, 0)
        #         elif percentchange == 0: bottomcolor = (110, 110, 110)
        #         else: bottomcolor = (80, 0, 0)

        #     pygame.draw.polygon(screen, bottomcolor, bottom_polygon)
        #     outlinecolor = (0, 0, 0) if self.selected_option != ioffset else (180, 180, 180)
        #     pygame.draw.polygon(screen, outlinecolor, points, 5)  # draw the outline of the polygon
        #     pygame.draw.polygon(screen, outlinecolor, points2, 5)  # draw the outline of the second polygon
        #     pygame.draw.polygon(screen, outlinecolor, points3, 5)  # draw the outline of the third polygon
            
        # emptyboxnum = 5-len([(stock) for i,stock in enumerate(player.options) if i >= self.bar.value and i < self.bar.value+5])
        # for i in range(emptyboxnum):
        #     ioffset = i+(5-emptyboxnum)
        #     points,points2,points3,totalpolyon = self.getpoints(150,200,200,(ioffset*xshift),(ioffset*yshift))
            
        #     gfxdraw.filled_polygon(screen, points, (30,30,30))
        #     gfxdraw.filled_polygon(screen, points2, (30,30,30))
        #     gfxdraw.filled_polygon(screen, points3, (30,30,30))
        #     pygame.draw.polygon(screen, (0,0,0), points, 5)
        #     pygame.draw.polygon(screen, (0,0,0), points2, 5)
        #     pygame.draw.polygon(screen, (0,0,0), points3, 5)
        #     screen.blit(self.emptytext, (320 + (ioffset * xshift), 235 + (ioffset * yshift)))  # display name of stock

        # values = [option.get_value() for option in player.options]
        # names = set([option.stockobj.name for option in player.options])
        # values = [[sum([v[0] for v in values if v[1] == name]), name] for name in names]

        # self.renderedback,self.renderedpietexts = draw_pie_chart(screen, values, 150,(1050, 200),self.renderedback,self.renderedpietexts)
    def draw_Available(self):
        pass

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player):
        """Draws all of the things in the option menu"""
        screen.blit(self.optiontext,(220,120))# display the option text
        # draw a polygon from 400,120 to 750,160
        ownedPoints = [(400, 110), (555, 110), (565, 170), (415, 170)]
        availablePoints = [(555, 110), (735, 110), (750, 170), (565, 170)]

        gfxdraw.filled_polygon(screen, ownedPoints, (50, 50, 50))
        pygame.draw.polygon(screen, (0, 0, 0), ownedPoints, 5)
        gfxdraw.filled_polygon(screen, availablePoints, (50, 50, 50))
        pygame.draw.polygon(screen, (0, 0, 0), availablePoints, 5)
        # drwa teh ownded and available text
        screen.blit(self.ownedtext[0] if self.view == 'Available' else self.ownedtext[1],(435,120))
        screen.blit(self.availabletext[0] if self.view == 'Owned' else self.availabletext[1],(585,120))
        # draw a line in between the owned and available text
        pygame.draw.line(screen,(0,0,0),(555,110),(565,170),5)
        if point_in_polygon(pygame.mouse.get_pos(),ownedPoints):
            if mousebuttons == 1:
                soundEffects['clickbutton2'].play()
                self.view = "Owned"
        elif point_in_polygon(pygame.mouse.get_pos(),availablePoints):
            if mousebuttons == 1:
                soundEffects['clickbutton2'].play()
                self.view = "Available"

        if self.view == "Owned":
            self.draw_Owned(screen,mousebuttons,player)
        elif self.view == "Available ":
            self.draw_Available()