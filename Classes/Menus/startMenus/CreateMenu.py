from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes.Menus.startMenus.StartMain import StartMain

import pygame
import os
from Defs import *
from pygame import gfxdraw
from Classes.imports.UIElements.SelectionElements import SelectionBar
from Classes.imports.UIElements.SideScroll import SideScroll, CreateMenuRunImage
from Classes.imports.UIElements.TextInput import TextInput
from Classes.Menus.GameModeMenu import GameRun,BlitzRun,CareerRun,GoalRun,RunManager

class CreateMenu:
    def __init__(self,runManager) -> None:
        self.modeselectionBar : SelectionBar = SelectionBar()
        self.customizeBar : SelectionBar = SelectionBar(allowSelcNone=True)# the bar for the customization (blits is time, Career is mode[Career/sandbox], Goal is target)
        
        self.mode = 'Blitz'# Career, Goal, or Blitz
        self.gameModes = ['Career','Blitz','Goal']
        self.modeColors = {self.gameModes[i]:[(19, 133, 100), (199, 114, 44), (196, 22, 62)][i] for i in range(3)}
        self.currentName = 'Game Name'
        self.runManager : RunManager = runManager
        
        # Initialize the new TextInput for game name
        self.nameInput = TextInput(
            initial_text='Game Name',
            max_length=25,
            font_size=55,
            text_color=(255, 255, 255),
            cursor_color=(255, 255, 255),
            background_color=(60, 60, 60),
            border_color=(100, 100, 100),
            border_width=3,
            border_radius=10,
            padding=15
        )
        
        self.gameIcons = [pygame.image.load(os.path.join(os.path.dirname(__file__), '..', '..', 'BigClasses', 'RunIcons', f'image ({i}).png')) for i in range(8)]
        self.gameIconScroll = SideScroll((180,325),(520,110),(70,70))# the side scroll for the game icons
        self.runIcons = [pygame.transform.smoothscale(g,(70,70)) for g in self.gameIcons]
        self.runIcons = [CreateMenuRunImage(self.gameIconScroll,g) for g in self.runIcons]
        self.gameIconScroll.loadCards(self.runIcons)
        self.gameIconScroll.setCard(index=0)
        self.haveError = False

        self.currentRun = None

        # self.surf = pygame.Surface((1920,1080),pygame.SRCALPHA)
        # self.surf.fill((60,60,60,200))
    def reset(self):
        self.currentName = 'Game Name'
        self.nameInput.set_text('Game Name')
        self.mode = 'Blitz'
        self.customizeBar.setSelected(None)
        self.modeselectionBar.setSelected(None)
        self.gameIconScroll.setCard(index=0)
        self.haveError = False
        self.currentRun = None
    def drawModeInfo(self,screen):
        """Draws the info about the mode (Left side of the screen)"""
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1360,65,395,955),5,border_radius=10)# box for the mode info on right

        descriptions = {
            "Blitz": "Make risky trades in this intense trading sprint.",
            "Career": "Make strategic investments and grow your wealth over years.",
            "Goal": "Reach specific financial targets within set timeframes."
        }
        extraDescriptions = {
            "Blitz": ["1M to 5Y time frame","All stocks are twice as volatile","Maximize ending net worth"],
            "Career": ["Unlimited time","Unlockable trading methods","Grow your net worth over time"],
            "Goal": ["Unlimited Time","Reach specific financial targets","Achieve goals as fast as possible"]
        }
        for i in range(3):
            color = (0,0,0) if self.gameModes[i] != self.mode else self.modeColors[self.mode]
            drawCenterTxt(screen,self.gameModes[i],65,color,(1370,75+(i*330)),centerX=False,centerY=False)

            color = (140,140,140) if self.gameModes[i] != self.mode else (195,195,195)
            for j,txt in enumerate(separate_strings(descriptions[self.gameModes[i]],2)):# draws the quick description of the mode
                drawCenterTxt(screen,txt,40,color,(1380,140+(i*330)+(j*40)),centerX=False,centerY=False)

            # color = (0,0,0) if self.gameModes[i] != self.mode else (59, 171, 22)
            color = (0,0,0) if self.gameModes[i] != self.mode else (0, 130, 0)
            for j,txt in enumerate(extraDescriptions[self.gameModes[i]]):# draws the extra info about the mode
                drawCenterTxt(screen,txt,35,color,(1400,220+(i*330)+(j*35)),centerX=False,centerY=False)

            if pygame.Rect(1360,65+(i*330),395,330).collidepoint(*pygame.mouse.get_pos()) and mouseButton.getButton("left"):
                self.mode = self.gameModes[i]  
                self.modeselectionBar.setSelected(self.mode)


        drawCenterTxt(screen,"Mode Info",65,(0,0,0),(1360+395/2,15),centerX=True,centerY=False)

    def drawInDepthInfo(self,screen):
        """Draws the in depth info about the mode under the mode selection"""
        drawCenterTxt(screen,self.mode,85,self.modeColors[self.mode],(180,600),centerX=False,centerY=False)# title
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(170,590,540,310),5,border_radius=10)# rect under the game mode selector (says more info about the mode)
        descriptions = {
            "Blitz": "In Blitz mode, you have limited time to maximize networth in a high-volatility market. All stocks have 2x normal price swings, requiring quick analysis and decisive trading.",
            "Career": "In Career mode, you unlimited time to build wealth in a standard market. Start with $10k and unlock advanced tools at wealth milestones.",
            "Goal": "In Goal mode, you start with 10k, and must reach a specific Goal within as little time as possible. Boost to your networth as quick as possible."
        }
        
        for i,txt in enumerate(separate_strings(descriptions[self.mode],5)):
            drawCenterTxt(screen,txt,45,(160,160,160),(195,665+(i*45)),centerX=False,centerY=False)

        
    def drawModeNameSelection(self,screen,events):
        drawCenterTxt(screen,"Name",65,(0,0,0),(730,65),centerX=False,centerY=False)
        
        # Update the text input and draw it
        self.nameInput.update()
        
        # Handle events for the text input
        for event in events:
            self.nameInput.handle_event(event)
        
        # Draw the text input
        name_rect = pygame.Rect(715, 115, 640, 75)
        self.nameInput.draw(screen, name_rect)
        
        # Update current name from text input
        self.currentName = self.nameInput.get_text()

        if type(n:=self.runManager.validName(self.currentName)) != bool:
            self.haveError = True
            drawCenterTxt(screen,n,40,(210,0,0),(730,200),centerX=False,centerY=False)

        
        drawCenterTxt(screen,"Mode",65,(0,0,0),(730,270),centerX=False,centerY=False)

        self.modeselectionBar.draw(screen,[g for g in self.gameModes],(710,320),(640,125),list(self.modeColors.values()),50)

        if self.modeselectionBar.getSelected() != None:
            self.mode = self.modeselectionBar.getSelected()

    def drawCustomizeInfo(self,screen):
        """Draws the customize info on the right side of the screen"""

        drawCenterTxt(screen,"Customization",65,(0,0,0),(730,525),centerX=False,centerY=False,fullY=True)
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(720,530,620,195),5,border_radius=10)# rect under the game mode selector (says more info about the mode)
        if self.mode == 'Blitz':
            if self.customizeBar.getSelected() is None:
                self.haveError = True
                drawCenterTxt(screen,"-Must select a time period for Blitz Mode",40,(220,0,0),(730,665),centerX=False,centerY=False)

            drawCenterTxt(screen,"Time Period",50,(180,180,180),(710+320,545),centerX=True,centerY=False)
            self.customizeBar.draw(screen,['1M','1Y','5Y'],(730,595),(600,60))
        elif self.mode == 'Career':
            
            drawCenterTxt(screen,"Starting Progress",50,(180,180,180),(710+320,545),centerX=True,centerY=False)
            self.customizeBar.draw(screen,['Career','Sandbox'],(730,595),(600,60))
            if self.customizeBar.getSelected() is None:
                self.customizeBar.setSelected('Career')

        elif self.mode == 'Goal':
            if self.customizeBar.getSelected() is None:
                self.haveError = True
                drawCenterTxt(screen,"-Must select a financial target for Goal Mode",40,(220,0,0),(730,665),centerX=False,centerY=False)

            drawCenterTxt(screen,"Financial Target",50,(180,180,180),(710+320,545),centerX=True,centerY=False)
            self.customizeBar.draw(screen,['100k','500k','1 Mil'],(730,595),(600,60))

    def drawImageSelection(self,screen):
        """Draws the image selection on the left top side of the screen"""
        
        if (n:=self.gameIconScroll.getCard(index=True)) != None:# if a card is selected
            image : pygame.Surface = self.gameIcons[n]# get the image of the card
            drawBoxedImage(screen,(180,75),image,(240,240),15,5)# draw the image of the card

        txt = '"'+self.currentName+'"'
        numLines = min(4,len(txt.split(' ')),math.ceil(len(txt)/9))
        lines = separate_strings(txt,numLines)
        for i,line in enumerate(lines):
            x = 425+(275)//2
            size = getTSizeNums(line,260,65)
            drawCenterTxt(screen,line,size,(200,200,200),(x,80+65*i),centerY=False)

    def createNewRun(self):
        imageInd = self.gameIconScroll.getCard(index=True)
        if self.mode == 'Blitz':# if the mode is Blitz
            gameDuration = self.customizeBar.getSelected()
            # ind = self.gameIconScroll.getCard(index=True)
            self.currentRun = BlitzRun(self.currentName,[],None,imageInd,gameDuration,self.runManager)

        elif self.mode == 'Career':
            mode = {'Career':False,'Sandbox':True}[self.customizeBar.getSelected()]# converts the selected string to a boolean            
            self.currentRun = CareerRun(self.currentName,[],None,imageInd,{},{},mode,self.runManager)

        elif self.mode == 'Goal':
            goalNetworth = {key:value for key,value in zip(['100k','500k','1 Mil'],[100000,500000,1000000])}[self.customizeBar.getSelected()]# converts the selected string to a number
            self.currentRun = GoalRun(self.currentName,[],None,imageInd,goalNetworth,self.runManager)

        
    def drawCreateGameBox(self,screen):
        """Draws the create game box"""
        color = (0,210,0) if not self.haveError else (210,0,0)
        mousex,mousey = pygame.mouse.get_pos()          

        n = drawClickableBoxWH(screen,(170,450),(540,130),"Create Game", 75, (0,0,0),color)

        if n and not self.haveError:# if the create game button is pressed and its all good, then create the game and enter it
            self.createNewRun()

        if self.haveError and pygame.Rect(170,450,540,130).collidepoint(mousex,mousey):
            drawCenterTxt(screen,"Please fill out all fields",40,(255,150,150),(mousex+20,mousey),centerX=False,centerY=False,font='light')
        return (n and not self.haveError)
        
    def draw(self,screen,events):
        """Draws the create game menu"""
        self.haveError = False# resets the error for each draw

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(150,10,1620,1060),5,border_radius=25)# main box border

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(170,65,540,380),5,border_radius=10)# box for the icon selection

        self.drawModeInfo(screen)# draws the mode info on the right

        self.drawModeNameSelection(screen,events)# draws the name and mode selection

        self.drawInDepthInfo(screen)# draws the in depth info about the mode

        self.drawCustomizeInfo(screen)# draws the customize info on the right side of the screen
        
        self.gameIconScroll.draw(screen)# draws the side scroll

        self.drawImageSelection(screen)# draws the image selection on the left top side of the screen

        # return not drawClickableBoxWH(screen,(170,450),(540,130),"Create Game", 75, (0,0,0),(200,200,200),)# returns False if the create game button is pressed
        return self.drawCreateGameBox(screen)

