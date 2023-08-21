import pygame
from Defs import *
class Menu():
    def __init__(self,icondir,iconcoords:tuple,stocknames:list=None) -> None:
        surface = pygame.Surface((140,115))
        self.icon = pygame.image.load(icondir).convert_alpha()
        self.icon = pygame.transform.scale(self.icon,(140,100))
        surface.fill((60,60,60))
        surface.blit(self.icon,(0,5))
        pygame.draw.rect(surface,(0,0,0),pygame.Rect(0,0,140,115),5)
        self.icon = surface.copy()
        # Set the icontext to be the name of the child class that inherits this class
        self.icontext = fontlist[36].render(self.__class__.__name__,(255,255,255))[0]
        self.menudrawn = False
        self.iconcoords = iconcoords
    
    def draw_icon(self,screen,Mousebuttons:int,stocklist:list,play_pause:bool,player,menulist):
        
        mousex,mousey = pygame.mouse.get_pos()
        collide = pygame.Rect.collidepoint(pygame.Rect(self.iconcoords[0],self.iconcoords[1],self.icon.get_width(),self.icon.get_height()+self.icontext.get_height()),mousex,mousey)
        if collide:
            width1 = self.icon.get_width(); height1 = self.icon.get_height();height2 = self.icontext.get_height()
            ypos = self.iconcoords[1]+10
            gfxdraw.filled_polygon(screen,[(25,ypos-15),(width1+35,ypos-15),(width1+35,ypos+height1+height2),(25,ypos+height1+height2)],(110,110,110))
            if Mousebuttons == 1:
                self.menudrawn = not self.menudrawn
                if self.menudrawn:#if the menu is drawn, then set all the other menus to not drawn
                    for menu in menulist:
                        if menu != self: menu.menudrawn = False
        # below is the code that draws the icon and the text
        # center the self.iocntext below the icon
        screen.blit(self.icon,self.iconcoords)
        textx = self.iconcoords[0]+(self.icon.get_width()/2)-(self.icontext.get_width()/2)
        screen.blit(self.icontext,(textx,self.icon.get_height()+self.iconcoords[1]+5))
        
        if self.menudrawn:
            self.draw_menu(screen,Mousebuttons,stocklist,play_pause,player)

    def draw_menu_content(self,screen:pygame.Surface,stocklist:list,Mousebuttons:int,play_pause,player):
        """Mearly a placeholder for the child classes to override"""
        pass

    def draw_menu(self,screen,Mousebuttons:int,stocklist:list,play_pause:bool,player):
        gfxdraw.filled_polygon(screen, ((200,100),(1500,100),(1600,980),(300,980)),(40,40,40))
        pygame.draw.polygon(screen, (0,0,0), ((200,100),(1500,100),(1600,980),(300,980)),10)
        self.draw_menu_content(screen,stocklist,Mousebuttons,play_pause,player)#draws the content of the menu, defined in the child classes
