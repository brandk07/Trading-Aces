from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes.Menus.startMenus.StartMain import StartMain

import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.UIElements.SelectionElements import SelectionBar
from Classes.imports.UIElements.SideScroll import SideScroll, CreateMenuRunImage

class CreateMenu:
    def __init__(self,startMenu) -> None:
        self.modeselectionBar : SelectionBar = SelectionBar()
        self.customizeBar : SelectionBar = SelectionBar(allowSelcNone=True)
        self.mode = 'blitz'# career, goal, or blitz
        self.gameModes = ['blitz','career','goal']
        self.modeColors = {self.gameModes[i]:[(19, 133, 100), (199, 114, 44), (196, 22, 62)][i] for i in range(3)}
        self.currentName = 'Game Name'
        self.startMenu : 'StartMain' = startMenu
        self.gameIcons = [pygame.image.load(rf'Assets\GameRuns\game Icons\image {i}.png') for i in range(1,9)]
        
        self.sideScroll = SideScroll((180,325),(520,110),(70,70))
        self.runIcons = [pygame.transform.smoothscale(g,(70,70)) for g in self.gameIcons]
        self.runIcons = [CreateMenuRunImage(self.sideScroll,g) for g in self.runIcons]
        self.sideScroll.loadCards(self.runIcons)
        self.sideScroll.setCard(index=0)
        self.haveError = False
    
    def drawModeInfo(self,screen):
        """Draws the info about the mode (Left side of the screen)"""
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1360,65,395,955),5,border_radius=10)# box for the mode info on right

        descriptions = {
            "blitz": "Make risky trades in this intense trading sprint.",
            "career": "Make strategic investments and grow your wealth over years.",
            "goal": "Reach specific financial targets within set timeframes."
        }
        extraDescriptions = {
            "blitz": ["• 1M to 5Y time frame","• All stocks are twice as volatile","• Maximize ending net worth"],
            "career": ["• Unlimited time","• Unlockable trading methods","• Grow your net worth over time"],
            "goal": ["• Unlimited Time","• Reach specific financial targets","• Achieve goals as fast as possible"]
        }
        for i in range(3):
            color = (0,0,0) if self.gameModes[i] != self.mode else self.modeColors[self.mode]
            drawCenterTxt(screen,self.gameModes[i].capitalize(),65,color,(1370,75+(i*330)),centerX=False,centerY=False)

            color = (140,140,140) if self.gameModes[i] != self.mode else (195,195,195)
            for j,txt in enumerate(separate_strings(descriptions[self.gameModes[i]],2)):# draws the quick description of the mode
                drawCenterTxt(screen,txt,40,color,(1380,140+(i*330)+(j*40)),centerX=False,centerY=False)

            color = (0,0,0) if self.gameModes[i] != self.mode else (59, 171, 22)
            for j,txt in enumerate(extraDescriptions[self.gameModes[i]]):# draws the extra info about the mode
                drawCenterTxt(screen,txt,35,color,(1400,220+(i*330)+(j*35)),centerX=False,centerY=False)

        drawCenterTxt(screen,"Mode Info",65,(0,0,0),(1360+395/2,15),centerX=True,centerY=False)

    def drawInDepthInfo(self,screen):
        """Draws the in depth info about the mode under the mode selection"""
        drawCenterTxt(screen,self.mode.capitalize(),85,self.modeColors[self.mode],(180,600),centerX=False,centerY=False)# title
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(170,590,540,430),5,border_radius=10)# rect under the game mode selector (says more info about the mode)
        descriptions = {
            "blitz": "In blitz mode, you have limited time to maximize networth in a high-volatility market. All stocks have 2x normal price swings, requiring quick analysis and decisive trading.",
            "career": "In career mode, you unlimited time to build wealth in a standard market. Start with $10k and unlock advanced tools at wealth milestones.",
            "goal": "In goal mode, you start with 10k, and must reach a specific goal within as little time as possible. Boost to your networth as quick as possible."
        }
        
        for i,txt in enumerate(separate_strings(descriptions[self.mode],5)):
            drawCenterTxt(screen,txt,45,(160,160,160),(195,665+(i*45)),centerX=False,centerY=False)

        
    def drawModeNameSelection(self,screen,mousebuttons,key):


        drawCenterTxt(screen,"Name",65,(0,0,0),(730,65),centerX=False,centerY=False)
        self.currentName = text_input(screen,(715,115),(640,75),self.currentName,key,55)

        if type(n:=self.startMenu.validName(self.currentName)) != bool:
            self.haveError = True
            drawCenterTxt(screen,n,40,(210,0,0),(730,200),centerX=False,centerY=False)

        
        drawCenterTxt(screen,"Mode",65,(0,0,0),(730,270),centerX=False,centerY=False)

        self.modeselectionBar.draw(screen,[g.capitalize() for g in self.gameModes],(710,320),(640,125),mousebuttons,list(self.modeColors.values()),50)

        if self.modeselectionBar.getSelected() != None:
            self.mode = (self.modeselectionBar.getSelected()).lower()

    def drawCustomizeInfo(self,screen,mousebuttons):
        """Draws the customize info on the right side of the screen"""

        drawCenterTxt(screen,"Customization",65,(0,0,0),(730,525),centerX=False,centerY=False,fullY=True)
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(720,530,620,195),5,border_radius=10)# rect under the game mode selector (says more info about the mode)
        if self.mode == 'blitz':
            if self.customizeBar.getSelected() == None:
                self.haveError = True
                drawCenterTxt(screen,"-Must select a time period for Blitz Mode",40,(210,0,0),(730,665),centerX=False,centerY=False)

            drawCenterTxt(screen,"Time Period",50,(180,180,180),(710+320,545),centerX=True,centerY=False)
            self.customizeBar.draw(screen,['1 M','1Y','5Y'],(730,595),(600,60),mousebuttons)
        elif self.mode == 'career':
            
            drawCenterTxt(screen,"Starting Progress",50,(180,180,180),(710+320,545),centerX=True,centerY=False)
            self.customizeBar.draw(screen,['Normal','Sandbox'],(730,595),(600,60),mousebuttons)
            if self.customizeBar.getSelected() == None:
                self.customizeBar.setSelected('Normal')
        elif self.mode == 'goal':
            if self.customizeBar.getSelected() == None:
                self.haveError = True
                drawCenterTxt(screen,"-Must select a financial target for Blitz Mode",40,(210,0,0),(730,665),centerX=False,centerY=False)

            drawCenterTxt(screen,"Financial Target",50,(180,180,180),(710+320,545),centerX=True,centerY=False)
            self.customizeBar.draw(screen,['100k','500k','1 Mil'],(730,595),(600,60),mousebuttons)

    def drawImageSelection(self,screen,mousebuttons):
        """Draws the image selection on the left top side of the screen"""
        
        if (n:=self.sideScroll.getCard(index=True)) != None:# if a card is selected
            image : pygame.Surface = self.gameIcons[n]# get the image of the card
            drawBoxedImage(screen,(180,75),image,(240,240),15,5)# draw the image of the card

        txt = '"'+self.currentName+'"'
        numLines = min(4,len(txt.split(' ')),math.ceil(len(txt)/9))
        lines = separate_strings(txt,numLines)
        for i,line in enumerate(lines):
            x = 425+(275)//2
            size = getTSizeNums(line,260,65)
            drawCenterTxt(screen,line,size,(200,200,200),(x,80+65*i),centerY=False)
    
    def drawCreateGameBox(self,screen,mousebuttons):
        """Draws the create game box"""
        color = (0,210,0) if not self.haveError else (210,0,0)
        mousex,mousey = pygame.mouse.get_pos()          
            

        n = drawClickableBoxWH(screen,(170,450),(540,130),"Create Game", 75, (0,0,0),color,mousebuttons)

        if n:
            animationList.append(BuyAnimation((mousex,mousey),20,animationList))

        if self.haveError and pygame.Rect(170,450,540,130).collidepoint(mousex,mousey):
            drawCenterTxt(screen,"Please fill out all fields",40,(255,150,150),(mousex+20,mousey),centerX=False,centerY=False,font='light')
        return (n and not self.haveError)
        
    def draw(self,screen,mousebuttons,key):
        """Draws the create game menu"""
        self.haveError = False# resets the error for each draw
         
        # pygame.draw.rect(screen,(60,60,60),pygame.Rect(150,10,1620,1060),border_radius=25)# main box

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(150,10,1620,1060),5,border_radius=25)# main box border

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(170,65,540,380),5,border_radius=10)# box for the icon selection

        self.drawModeInfo(screen)# draws the mode info on the right

        self.drawModeNameSelection(screen,mousebuttons,key)# draws the name and mode selection

        self.drawInDepthInfo(screen)

        self.drawCustomizeInfo(screen,mousebuttons)
        
        self.sideScroll.draw(screen,mousebuttons)

        self.drawImageSelection(screen,mousebuttons)
        


        # return not drawClickableBoxWH(screen,(170,450),(540,130),"Create Game", 75, (0,0,0),(200,200,200),mousebuttons)# returns False if the create game button is pressed
        return self.drawCreateGameBox(screen,mousebuttons)

