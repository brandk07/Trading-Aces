from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes.Menus.startMenus.StartMain import StartMain

import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.UIElements.SelectionElements import MultiSelectionBar,MenuSelection,SelectionBar
from Classes.imports.UIElements.SideScroll import *
from Classes.Menus.GameModeMenu import GameRun,BlitzRun,CareerRun,GoalRun,RunManager
from Classes.imports.UIElements.Latterscroll import LatterScroll
from Classes.imports.UIElements.OrderBox import OrderBox

class PlayMenu:
    def __init__(self,runManager:RunManager) -> None:
        # self.latterScroll = LatterScroll()
       
        self.vertScroll = VerticalScroll((740,115),(1040,920),(930,255))
        self.gameModes = ['Career','Blitz','Goal']
        self.modeColors = {self.gameModes[i]:[(19, 133, 100), (199, 114, 44), (196, 22, 62)][i] for i in range(3)}
        self.runManager = runManager
        self.selectionBar = SelectionBar()
        self.orderBox = OrderBox((170,640),(530,240))
        self.liveOrPast = MenuSelection((175,20),(525,95),["Live","Complete"],55,[(34, 139, 34), (220, 20, 60)])
        self.selectionBar.setSelected("Career")# sets initial selected mode
        self.liveOrPast.setSelected("Live")  # sets initial selected state
        self.updateRunCards()

    def updateRunCards(self):
        """Fills/Updates the run cards that are used in the vertScroll
        MUST be called anytime something changes like deleting or adding a run"""
        self.runCards: dict = {r.name: StartRunCard(self.vertScroll, r) for r in self.runManager.getAllRuns(True)}
        self.completedCards: dict = {r.name: StartRunCard(self.vertScroll, r) for r in self.runManager.getAllCompletedRuns(True)}
        # sort the dict by the lastPlayed attribute - it is a datetime object
        # self.runCards = dict(sorted(self.runCards.items(),key=lambda x: x[1].runObj.lastPlayed,reverse=True))

    def reset(self):
        # self.vertScroll.reset()
        self.selectionBar.setSelected("Career")# sets initial selected mode
        self.liveOrPast.setSelected("Live")
        self.updateRunCards()

    def drawLatterScroll(self,screen:pygame.Surface,runs:list[GameRun]):

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(715,115,1040,920),5,border_radius=25)# outline for the latter scroll

        # cards = [StartRunCard(self.vertScroll,c) for c in runs]
        cards = [self.runCards[r.name] for r in runs] if self.liveOrPast.getSelected() == "Live" else [self.completedCards[r.name] for r in runs]
        cards.sort(key=lambda x: x.runObj.lastPlayed,reverse=True)
        self.vertScroll.loadCards(cards)
        if self.vertScroll.draw(screen):
            self.orderBox.reset()
    def drawSelected(self,screen:pygame.Surface):
        run = self.vertScroll.getCard().runObj
        
        drawCenterTxt(screen,run.name,85,(200,200,200),(440,140),centerY=False)

        info = [
            ("Mode",run.gameMode),
            ("Net Worth",f"${limit_digits(run.getNetworth(),18)}"),
            ("Last Played On",run.lastPlayed.strftime(DFORMAT)),
        ]
        
        drawLinedInfo(screen,(170,215),(540,260),info,45,colors=(self.modeColors[run.gameMode],(0,200,0),(180,180,180)))

 
        self.orderBox.loadData("Deleting Run",f"$0",[("Action Irreversible","","")],showTotal=False)# if the run is completedRuns then the only option is to delete it
        
        result = self.orderBox.draw(screen)
        if result:
            self.runManager.removeRun(run)
            self.updateRunCards()
            

        

    def draw(self,screen:pygame.Surface):
        
        
        selectMode = self.selectionBar.getSelected()
        if self.liveOrPast.getSelected() == "Live":
            runs = self.runManager.getRuns(selectMode)
   
        else:
            runs = self.runManager.getRunsCompleted(selectMode)


        self.drawLatterScroll(screen,runs)

        if self.vertScroll.getCard() != None:
            self.drawSelected(screen)

        self.selectionBar.draw(screen,['Career','Blitz','Goal'],(985,20),(500,85),colors=[(19, 133, 100), (199, 114, 44), (196, 22, 62)],txtsize=50)

        self.liveOrPast.draw(screen)
        # drawCenterTxt(screen,"Select A Run",85,(200,200,200),(175,25),centerX=False,centerY=False)

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(150,10,1620,1060),5,border_radius=25)# main box border

        if self.vertScroll.getCard() != None and drawClickableBoxWH(screen,(180,450),(510,110),"PLAY" if self.liveOrPast.getSelected() == "Live" else "VIEW", 65, (0,0,0),(0,210,0)):
            return self.vertScroll.getCard().runObj

        

