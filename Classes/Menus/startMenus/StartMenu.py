import pygame
from Defs import *
from Classes.imports.UIElements.SelectionElements import SelectionBar
from pygame import gfxdraw

class StartMenu:
    def __init__(self) -> None:
        self.customizeBar : SelectionBar = SelectionBar(horizontal=False,allowSelcNone=True)
        self.lines = [((0,540),(0,0,0))]# ((endx,endy),color)
        self.appendLine = 0

    # def drawLineEffect(self,screen):
    #     """Draws the line effect on the screen"""
    #     if self.appendLine < 5:
    #         self.appendLine += 1
    #     else:
    #         self.appendLine = 0
    #         lineWidth = randint(1,10)
    #         lineChange = randint(-25,25)
    #         color = (0,220,0) if lineChange < 0 else (220,0,0)
    #         x = self.lines[-1][0][0] + lineWidth
    #         y = self.lines[-1][0][1] + lineChange
    #         self.lines.append(((x,y),color))# 

    #     for i,(line,color) in enumerate(self.lines):
    #         lastLine = self.lines[i-1][0] if i > 0 else (0,540)
            
    #         gfxdraw.filled_polygon(screen,[lastLine,line,(line[0],540),(lastLine[0],540)],(0,0,0))
    #         pygame.draw.line(screen,color,lastLine,line,3)
    #         if line[0] > 1920:
    #             self.lines = [((0,540),(0,0,0))]
    #             break
        # pygame.draw.line(screen,color,(0,self.linePlace),(1920,self.linePlace),lineWidth)


    def draw(self,screen:pygame.Surface):
        
        # Title
        drawCenterTxt(screen,"TRADING ACES",200,(0,0,0),(960,175),centerX=True,centerY=False,font='bold')
        
        # n = self.customizeBar.draw(screen,["Play","Create","Settings","Credits"],(660,350),(600,550))
        # draw a polygon from 0,350 to 1920,890
        # gfxdraw.filled_polygon(screen,[(0,350),(1920,350),(1920,890),(0,890)],(60,60,60,200))
        changeScreen = False
        # for i,txt in enumerate(['Play','Create','Settings','Credits']):
        for i,txt in enumerate(['Play','Create']):
            # if drawClickableBoxWH(screen,(660,350+(140*i)),(600,135),txt, 75, (0,0,0),(200,200,200)) != False:
            if drawClickableBoxWH(screen,(660,490+(140*i)),(600,135),txt, 75, (0,0,0),(200,200,200)) != False:
                changeScreen = txt

        # self.drawLineEffect(screen)

        return changeScreen if changeScreen != False else None

