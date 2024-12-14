from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Classes.Menus.startMenus.StartMain import StartMain

import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.UIElements.SelectionElements import MultiSelectionBar
from Classes.imports.UIElements.SideScroll import *
from Classes.Menus.GameModeMenu import GameRun,BlitzRun,CareerRun,GoalRun,RunManager
from Classes.imports.UIElements.Latterscroll import LatterScroll

class PlayMenu:
    def __init__(self,runManager:RunManager) -> None:
        # self.latterScroll = LatterScroll()
       
        self.vertScroll = VerticalScroll((740,115),(1040,920),(930,255))
        
        self.runManager = runManager
        self.selectionBar = MultiSelectionBar()
        self.selectionBar.setSelected(["Blitz","Career","Goal"])# sets all the options to be selected

    def drawLatterScroll(self,screen:pygame.Surface,runs:list[GameRun],mousebuttons:int):

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(715,115,1040,920),5,border_radius=25)# outline for the latter scroll

        cards = [StartRunCard(self.vertScroll,c) for c in self.runManager.getRuns("Blitz")]
        self.vertScroll.loadCards(cards)
        self.vertScroll.draw(screen,mousebuttons)

    def draw(self,screen:pygame.Surface,mousebuttons:int):
        runs = []
        for r in self.selectionBar.getSelected():
            runs.extend(self.runManager.getRuns(r))
        self.drawLatterScroll(screen,runs,mousebuttons)


        # centered at 1235
        self.selectionBar.draw(screen,["Blitz","Career","Goal"],(985,20),(500,85),mousebuttons,txtsize=50)

        drawCenterTxt(screen,"Select A Run",85,(200,200,200),(175,25),centerX=False,centerY=False)

        pygame.draw.rect(screen,(0,0,0),pygame.Rect(150,10,1620,1060),5,border_radius=25)# main box border

        if self.vertScroll.getCard() != None and  drawClickableBoxWH(screen,(170,115),(540,130),"Play", 75, (0,0,0),(0,210,0),mousebuttons):
            return self.vertScroll.getCard().runObj

        

