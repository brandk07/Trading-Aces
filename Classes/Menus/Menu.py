import pygame
from Defs import *
from Classes.Menus.HomeScreen import HomeScreen
from Classes.imports.UIElements.SelectionElements import SelectionBar

class ScreenManager:
    def __init__(self,menuDict:dict,homeScreen,stockScreen) -> None:
        self.screens = {"Home":homeScreen,"Stock":stockScreen}
        for key in menuDict:
            self.screens[key] = menuDict[key]

        self.selectedScreen= "Stock"
        self.screenSelection : SelectionBar = SelectionBar(horizontal=False,rounded=5)
    def setScreen(self,screenName):
        """Sets the current screen to the screen with the name screenName"""
        assert screenName in self.screens, f"Screen {screenName} not found in screens"
        self.selectedScreen = screenName
        self.screenSelection.setSelected(screenName)

    def getCurrentScreen(self,returnName=False):
        """Returns the current screen obj, """
        return self.selectedScreen if returnName else self.screens[self.selectedScreen]
    
    def drawSelector(self,screen,mousebuttons):  

        if self.selectedScreen not in self.screens:
            self.selectedScreen = "Home"
        
        # drawBoxedImage(screen,(5,7),self.screens[self.selectedScreen].icon,(170,170),borderRadius=5)
        colors = [(86, 130, 189),(239, 131, 84),(92, 131, 116),(255, 205, 78),(191, 85, 178),(87, 167, 115),(255, 145, 164)]
        # drawCenterTxt(screen,self.selectedScreen,55,colors[list(self.screens).index(self.selectedScreen)],(90,180),centerY=False)
        drawCenterTxt(screen,self.selectedScreen,getTSizeNums(self.selectedScreen,150,80),colors[list(self.screens).index(self.selectedScreen)],(90,50))
        
        
        # self.screenSelection.draw(screen,list(self.screens.keys()),(10,225),(170,415),mousebuttons,colors=colors)
        self.screenSelection.draw(screen,list(self.screens.keys()),(10,90),(170,415),mousebuttons,colors=colors)
        self.selectedScreen = self.screenSelection.getSelected()

    def drawTime(self,screen,gametime):
        """Draws the time in the top left corner"""
        timeStrs = gametime.getTimeStrings()
        # t : datetime = gametime.time
        hour = ("0" if (timeStrs['hour']) < 10 else "")+str(timeStrs['hour'])
        # pygame.draw.rect(screen,(0,0,0),pygame.Rect(2,515,180,370),width=5)

        drawCenterTxt(screen,hour,150,(200,200,200),(92,530),centerY=False)
        drawCenterTxt(screen,f"{timeStrs['minute']}",150,(200,200,200),(92,650),centerY=False)
        drawCenterTxt(screen,f"{timeStrs['dayname'][:3]} {timeStrs['monthname'][:3]} {timeStrs['day']}",50,(200,200,200),(92,765),centerY=False)
        drawCenterTxt(screen,f"{timeStrs['year']}",80,(200,200,200),(92,820),centerY=False)
        
    def drawCurrentScreen(self,screen,mousebuttons,stocklist,player,gametime):
        
        
        
        self.drawTime(screen,gametime)
        self.drawSelector(screen,mousebuttons)
        self.screens[self.selectedScreen].draw(screen,mousebuttons,stocklist,player,gametime)
        

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

    def drawbottombar(self,screen,gametime,player):
        """Draws the bottom bar of the screen"""
        gametime.speedBar.draw_bar(screen,[760,990],[375,80],'horizontal',reversedscroll=True,text=gametime.skipText())
        screen.blit(s_render(f"Cash ${limit_digits(player.cash,150)}",50,(200,200,200)),(1150,1010))
        gametimetext = s_render(f"{str(gametime)}",50,(200,200,200))
        screen.blit(gametimetext,(750-gametimetext.get_width(),1010))
        # draws the time in the top left corner
        # texts = gametime.getrenders(50,50,50,105,50,50)
    # def topbar(self,screen,gametime,player):
    #     """Draws the top bar of the screen"""
        
        
    def draw(self,screen,mousebuttons:int,stocklist:list,player,gametime):
        
        # self.topbar(screen,gametime,player)
        self.drawbottombar(screen,gametime,player)
        self.draw_menu_content(screen,stocklist,mousebuttons,player,gametime)#draws the content of the menu, defined in the child classes

