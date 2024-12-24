import pygame
from Defs import *
from Classes.Menus.HomeScreen import HomeScreen
from Classes.imports.UIElements.SelectionElements import SelectionBar

class ScreenManager:
    def __init__(self,menuDict:dict,homeScreen,stockScreen,gametime) -> None:
        self.screens = {"Home":homeScreen,"Stock":stockScreen}
        self.gameTime = gametime
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
    
    def drawSelector(self,screen):  

        if self.selectedScreen not in self.screens:
            self.selectedScreen = "Home"
        
        # drawBoxedImage(screen,(5,7),self.screens[self.selectedScreen].icon,(170,170),borderRadius=5)
        colors = [(179, 12, 0),(255, 205, 78),(239, 131, 84),(86, 130, 189),(191, 85, 178),(87, 167, 115),(255, 145, 164)]
        
        # drawCenterTxt(screen,self.selectedScreen,55,colors[list(self.screens).index(self.selectedScreen)],(90,180),centerY=False)
        drawCenterTxt(screen,self.selectedScreen,getTSizeNums(self.selectedScreen,150,80),colors[list(self.screens).index(self.selectedScreen)],(90,50))
        
        
        # self.screenSelection.draw(screen,list(self.screens.keys()),(10,225),(170,415),colors=colors)
        result = self.screenSelection.draw(screen,list(self.screens.keys()),(10,90),(170,415),colors=colors)

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
        
    def drawCurrentScreen(self,screen,stocklist,player,gametime):
        self.drawSelector(screen)
        if self.screens['Options'].isForced():#if the options screen is forced
            self.gameTime.speedBar.frozen = True
        self.drawTime(screen,gametime)
        
        self.screens[self.selectedScreen].draw(screen,stocklist,player,gametime)
        

class Menu():
    def __init__(self) -> None:
        self.menudrawn = False
        self.menupoints = [(185,10),(1910,10),(1910,980),(185,980)]
        self.topbarpoints = [(185,10),(1910,10),(1910,95),(185,95)]        

    def draw_menu_content(self,screen:pygame.Surface,stocklist:list,player,gametime):
        """Mearly a placeholder for the child classes to override"""
        pass

    def drawbottombar(self,screen,gametime,player):
        """Draws the bottom bar of the screen"""
        gametime.speedBar.drawBar(screen,(825,990))
        
    def drawCash(self,screen,player):
        txt = limit_digits(player.cash,30)
        txt = "Cash $" + limit_digits(player.cash,30)
        drawCenterTxt(screen,txt,75,(220,220,220),(1890,15),centerX=False,fullX=True,centerY=False)
    
    def draw(self,screen,stocklist:list,player,gametime):
        
        # self.topbar(screen,gametime,player)
        self.drawCash(screen,player)
        self.drawbottombar(screen,gametime,player)
        self.draw_menu_content(screen,stocklist,player,gametime)#draws the content of the menu, defined in the child classes

