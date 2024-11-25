import pygame
from Defs import *
from Classes.BigClasses.UIControls import UIControls
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
        self.menupoints = [(185,10),(1910,10),(1910,980),(185,980)]
        self.topbarpoints = [(185,10),(1910,10),(1910,95),(185,95)]
        

    
    def draw_icon(self,screen,mousebuttons:int,stocklist:list,player,menulist,iconcoords:tuple,ui_controls,gametime):
        x,y = iconcoords
        mousex,mousey = pygame.mouse.get_pos()
        collide = pygame.Rect.collidepoint(pygame.Rect(x,y,self.icon.get_width(),self.icon.get_height()+self.icontext.get_height()),mousex,mousey)
        if collide:
            width1 = self.icon.get_width(); height1 = self.icon.get_height();height2 = self.icontext.get_height()
            ypos = y+10
            gfxdraw.filled_polygon(screen,[(25,ypos-15),(width1+35,ypos-15),(width1+35,ypos+height1+height2),(25,ypos+height1+height2)],(110,110,110))
            if mousebuttons == 1:
                self.menudrawn = not self.menudrawn
                soundEffects['menuClick'].play()
                if self.menudrawn:#if the menu is drawn, then set all the other menus to not drawn
                    for menu in menulist:
                        if menu != self: menu.menudrawn = False
        else:# if the mouse is not colliding with the icon
            fullmenu = [(self.menupoints[0][0],self.menupoints[0][1]),(self.menupoints[1][0]+300,self.menupoints[1][1]),(self.menupoints[2][0]+300,1080),(self.menupoints[3][0],1080)]
            if mousebuttons == 1 and not point_in_polygon(pygame.mouse.get_pos(),fullmenu):# if the mouse is clicked outside of the menu, then set the menu to not drawn
                self.menudrawn = False
        
        # below is the code that draws the icon and the text
        # center the self.iocntext below the icon
        screen.blit(self.icon,iconcoords)
        textx = x+(self.icon.get_width()/2)-(self.icontext.get_width()/2)
        screen.blit(self.icontext,(textx,self.icon.get_height()+y+5))
        
        if self.menudrawn:
            self.draw_menu(screen,mousebuttons,stocklist,player,ui_controls,gametime)

    def draw_menu_content(self,screen:pygame.Surface,stocklist:list,mousebuttons:int,player,gametime):
        """Mearly a placeholder for the child classes to override"""
        pass
    # def draw_menu_sidebar(self,screen,ui_controls,stocklist,gametime):
    #     # draw a polygon with points (1150,40) to (1900,975)
    #     points = ((1520,100),(1800,100),(1900,980),(1620,980))
    #     gfxdraw.filled_polygon(screen, points,(40,40,40))
    #     pygame.draw.polygon(screen, (0,0,0), points,10)

    #     ui_controls.gameplay_speed = ui_controls.bar.draw_bar(screen,[1650,630],[120,320],'vertical',shift=40)

    #     # draws the top stock bar 
    #     # ui_controls.draw_stockbar(screen,stocklist,[200,10],[1300,80])
        
    #     # draws the time in the top left corner
    #     texts = gametime.getrenders(50,50,50,105,50,50)# month,day,year,timerender,dayname,monthname
    #     month,day,year,timerender,dayname,monthname = texts

    #     screen.blit(timerender,(200,10))
    #     screen.blit(dayname,(215+timerender.get_width(),10))
    #     screen.blit(monthname,(215+timerender.get_width()+10,15+dayname.get_height()))
    #     screen.blit(day,(215+timerender.get_width()+monthname.get_width()+20,15+dayname.get_height()))
    #     screen.blit(year,(215+timerender.get_width()+monthname.get_width()+day.get_width()+30,15+dayname.get_height()))
    #     twidth = 215+timerender.get_width()+monthname.get_width()+day.get_width()+year.get_width()+30
    #     # draws the market open/closed text
    #     color = (0,150,0) if gametime.isOpen()[0] else (150,0,0)
    #     screen.blit(s_render(f"MARKET {'OPEN' if gametime.isOpen()[0] else 'CLOSED'}",110,color),(twidth+50,5))
    #     if not gametime.isOpen()[0]: 
    #         if ui_controls.autofastforward:
    #             gametime.skipToOpen = True

        # gfxdraw.filled_polygon(screen, ((1150,40),(1900,40),(1900,975),(1150,975)),(40,40,40))
        # pygame.draw.polygon(screen, (0,0,0), ((1150,40),(1900,40),(1900,975),(1150,975)),10)
    def drawbottombar(self,screen,ui_controls:UIControls,gametime):
        """Draws the bottom bar of the screen"""
        ui_controls.gameplay_speed = ui_controls.bar.draw_bar(screen,[760,990],[375,80],'horizontal',reversedscroll=True,text=gametime.skipText())

        # draws the time in the top left corner
        # texts = gametime.getrenders(50,50,50,105,50,50)
    def topbar(self,screen,gametime,player):
        """Draws the top bar of the screen"""
        screen.blit(s_render(f"Cash ${limit_digits(player.cash,150)}",50,(200,200,200)),(1150,1010))
        gametimetext = s_render(f"{str(gametime)}",50,(200,200,200))
        screen.blit(gametimetext,(750-gametimetext.get_width(),1010))
        
    def draw_menu(self,screen,mousebuttons:int,stocklist:list,player,ui_controls,gametime):
        
        self.topbar(screen,gametime,player)
        self.drawbottombar(screen,ui_controls,gametime)
        self.draw_menu_content(screen,stocklist,mousebuttons,player,gametime)#draws the content of the menu, defined in the child classes

