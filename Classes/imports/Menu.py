import pygame
from Defs import *

class Menu():
    def __init__(self,iconimage) -> None:
        surface = pygame.Surface((140,115))
        # self.icon = pygame.image.load(icondir).convert_alpha()
        # self.icon = pygame.transform.scale(self.icon,(140,100))
        self.icon = iconimage
        surface.fill((60,60,60))
        surface.blit(self.icon,(0,5))
        pygame.draw.rect(surface,(0,0,0),pygame.Rect(0,0,140,115),5)
        self.icon = surface.copy()
        # Set the icontext to be the name of the child class that inherits this class
        self.icontext = fontlist[36].render(self.__class__.__name__,(255,255,255))[0]
        self.menudrawn = False

    
    def draw_icon(self,screen,mousebuttons:int,stocklist:list,player,menulist,iconcoords:tuple):
        x,y = iconcoords
        mousex,mousey = pygame.mouse.get_pos()
        collide = pygame.Rect.collidepoint(pygame.Rect(x,y,self.icon.get_width(),self.icon.get_height()+self.icontext.get_height()),mousex,mousey)
        if collide:
            width1 = self.icon.get_width(); height1 = self.icon.get_height();height2 = self.icontext.get_height()
            ypos = y+10
            gfxdraw.filled_polygon(screen,[(25,ypos-15),(width1+35,ypos-15),(width1+35,ypos+height1+height2),(25,ypos+height1+height2)],(110,110,110))
            if mousebuttons == 1:
                
                self.menudrawn = not self.menudrawn
                soundEffects['clickbutton'].play()
                if self.menudrawn:#if the menu is drawn, then set all the other menus to not drawn
                    for menu in menulist:
                        if menu != self: menu.menudrawn = False
        # below is the code that draws the icon and the text
        # center the self.iocntext below the icon
        screen.blit(self.icon,iconcoords)
        textx = x+(self.icon.get_width()/2)-(self.icontext.get_width()/2)
        screen.blit(self.icontext,(textx,self.icon.get_height()+y+5))
        
        if self.menudrawn:
            self.draw_menu(screen,mousebuttons,stocklist,player)

    def draw_menu_content(self,screen:pygame.Surface,stocklist:list,Mousebuttons:int,player):
        """Mearly a placeholder for the child classes to override"""
        pass

    def draw_menu(self,screen,Mousebuttons:int,stocklist:list,player):
        gfxdraw.filled_polygon(screen, ((200,100),(1500,100),(1600,980),(300,980)),(40,40,40))
        pygame.draw.polygon(screen, (0,0,0), ((200,100),(1500,100),(1600,980),(300,980)),10)
        self.draw_menu_content(screen,stocklist,Mousebuttons,player)#draws the content of the menu, defined in the child classes
