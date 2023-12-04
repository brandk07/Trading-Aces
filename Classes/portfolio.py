import pygame
import timeit
from Defs import *
from Classes.imports.Menu import Menu
import pygame.gfxdraw
from Classes.imports.Bar import SliderBar

class Portfolio(Menu):
    def __init__(self):
        super().__init__(r'Assets\Portfolio\portfolio.png',(30,340))
        # self.icon = pygame.image.load(r'Assets\Portfolio\portfolio2.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon,(140,100))
        # remove all the white from the image
        self.bar = SliderBar((0,0),50,[(0,120,0),(110,110,110)])
        self.bar2 = SliderBar((0,0),50,[(0,120,0),(110,110,110)])
        self.bar3 = SliderBar((0,0),50,[(0,120,0),(110,110,110)])
        self.icon.set_colorkey((255,255,255))
        self.portfoliotext = fontlist[36].render('Portfolio',(255,255,255))[0]

    def draw_menu_content(self,screen:pygame.Surface,Mousebuttons:int,stocklist:list,player):
        mousex,mousey = pygame.mouse.get_pos()
        self.bar.draw_bar(screen,[220,145],[45,800],'vertical',barwh=[42,50],shift=95)
        self.bar2.draw_bar(screen,[440,145],[45,800],'vertical',barwh=[42,50],shift=200)
        self.bar3.draw_bar(screen,[800,145],[45,800],'vertical',barwh=[42,50],shift=600)
        # for i,stock in enumerate(player.stocks):

        #     polytext = fontlist[36].render(f'{stock[0]} ${round(stock[0].price,2)}',(255,255,255))[0]
        #     # make the polygon's x pos fit the polytext length
        #     x = polytext.get_width()
        #     gfxdraw.filled_polygon(screen,((215+(i*8),120+(i*65)),(225+(i*8),155+(i*65)),((x+20)+(i*8),155+(i*65)),((x+10)+(i*8),120+(i*65))),(0,80,0))
        #     screen.blit(polytext,(225+(i*8),125+(i*65)))
    
