import pygame
import timeit
from Defs import *
from Classes.menu import Menu
import pygame.gfxdraw

class Portfolio(Menu):
    def __init__(self):
        super().__init__(r'Assets\Portfolio\portfolio.png',(30,340))
        # self.icon = pygame.image.load(r'Assets\Portfolio\portfolio2.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon,(140,100))
        # remove all the white from the image
        self.icon.set_colorkey((255,255,255))
        self.portfoliotext = fontlist[36].render('Portfolio',(255,255,255))[0]

    def draw_menu_content(self,screen:pygame.Surface,stocklist:list,Mousebuttons:int,play_pause,player):
        mousex,mousey = pygame.mouse.get_pos()
        for i,stock in enumerate(player.stocks):
            # [name, price, obj, Stock object]

            # if pygame.Rect.collidepoint(pygame.Rect(215+(i*8),120+(i*65),175,35),mousex,mousey) and Mousebuttons == 1:#if the mouse is hovering over the stock
            #     self.selectedstock = i
            # if stock.price > stock.graphrangelists[stock.graphrange][0]:# if the price is greater than the first point in the current graph
            #     color = (0,120,0) if self.selectedstock == i else (0,80,0)
            # else:
            #     color = (120,0,0) if self.selectedstock == i else (80,0,0)
            # the polygons and text for each of the stocks with the names and prices on the left side of the screen
            polytext = fontlist[36].render(f'{stock[0]} ${round(stock[3].price,2)}',(255,255,255))[0]
            # make the polygon's x pos fit the polytext length
            x = polytext.get_width()
            gfxdraw.filled_polygon(screen,((215+(i*8),120+(i*65)),(225+(i*8),155+(i*65)),((x+20)+(i*8),155+(i*65)),((x+10)+(i*8),120+(i*65))),(0,80,0))
            screen.blit(polytext,(225+(i*8),125+(i*65)))
            # if self.selectedstock == i:
            #     pygame.draw.polygon(screen, (0,0,0), ((215+(i*8),120+(i*65)),(225+(i*8),155+(i*65)),(400+(i*8),155+(i*65)),(390+(i*8),120+(i*65))),5)
            #     self.selected_stock(screen,stocklist,play_pause,player,Mousebuttons)
        
    # def draw(self,screen):
    #     pass

    # def draw_icon(self,screen):
    #     mousex,mousey = pygame.mouse.get_pos()
    #     collide = pygame.Rect.collidepoint(pygame.Rect(30,100,self.icon.get_width(),self.icon.get_height()+self.buyselltext.get_height()),mousex,mousey)
    #     if self.icon_sensing(screen,Mousebuttons,stocklist,play_pause,player):
    #         width1 = self.icon.get_width(); height1 = self.icon.get_height();height2 = self.buyselltext.get_height()
    #         gfxdraw.filled_polygon(screen,[(25,95),(width1+35,95),(width1+35,110+height1+height2),(25,110+height1+height2)],(110,110,110))
    #     screen.blit(self.icon,(30,250))
    #     screen.blit(self.portfoliotext,(50,self.icon.get_height()+255))
