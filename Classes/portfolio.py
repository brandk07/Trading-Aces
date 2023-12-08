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
        self.bar.gameplay_speed = 1
        self.icon.set_colorkey((255,255,255))
        self.portfoliotext = fontlist[36].render('Portfolio',(255,255,255))[0]
        self.menudrawn = True
        

    def draw_menu_content(self,screen:pygame.Surface,Mousebuttons:int,stocklist:list,player):
        mousex,mousey = pygame.mouse.get_pos()
        self.bar.draw_bar(screen,[220,145],[45,800],'vertical',barwh=[45,50],shift=95,reversedscroll=True)

        for i,stock in enumerate(player.stocks):

            polytext = fontlist[36].render(f'{stock[0]} ${round(stock[0].price,2)}',(255,255,255))[0]
            # make the polygon's x pos fit the polytext length
            # x = polytext.get_width()
            # draw a trapazoid from  (300 220) to (700 320) and include i*xshift in the x and i*65 in the y
            # top left, bottom left, bottom right, top right
            xshift =  14
            yshift = 130
            gfxdraw.filled_polygon(screen,((300+(i*xshift),200+(i*yshift)),(315+(i*xshift),300+(i*yshift)),(715+(i*xshift),300+(i*yshift)),(700+(i*xshift),200+(i*yshift))),(30,30,30))
            # draw a outline around the polygon with a witdth of 5
            pygame.draw.polygon(screen,(0,0,0),((300+(i*xshift),200+(i*yshift)),(315+(i*xshift),300+(i*yshift)),(715+(i*xshift),300+(i*yshift)),(700+(i*xshift),200+(i*yshift))),5)

            # gfxdraw.filled_polygon(screen,((365+(i*8),120+(i*65)),(375+(i*8),155+(i*65)),((x+20)+(i*8),155+(i*65)),((x+10)+(i*8),120+(i*65))),(0,80,0))
            screen.blit(polytext,(320+(i*xshift),235+(i*yshift)))
    
