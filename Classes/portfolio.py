import pygame
import timeit
from Defs import *
import pygame.gfxdraw

class Portfolio():
    def __init__(self):
        self.icon = pygame.image.load(r'Assets\Portfolio\portfolio.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon,(140,100))
        self.portfoliotext = fontlist[36].render('Portfolio',(0,0,0))[0]
    def draw(self,screen):
        pass

    def draw_icon(self,screen):
        screen.blit(self.icon,(30,150))
        screen.blit(self.portfoliotext,(50,self.icon.get_height()+105))
