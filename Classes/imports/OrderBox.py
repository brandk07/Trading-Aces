import pygame
from Defs import *

class OrderBox:
    def __init__(self,coords:tuple,wh:tuple) -> None:
        self.coords = list(coords)
        self.wh = list(wh)
        self.quantStr = ""
        self.extraData = []
        self.stage = 0# 0 is the first stage (proceeding to confirm screen), 1 is the second stage (confirming the order)
        self.middleData = []
        
    def loadData(self,quantStr:str,totalStr:str,extraData:list[tuple[str,str,str]]):
        """extraData is [(key,value,middleVal)]"""
        self.extraData = extraData
        self.extraData.append(("Total",totalStr,""))
        self.quantStr = quantStr

    def draw(self,screen:pygame.Surface,mousebuttons:int) -> bool:
        """Returns True if the confirm button is pressed"""
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(self.coords[0],self.coords[1],self.wh[0],self.wh[1]),5,15)

        if self.stage == 0:
            # DRAWING THE VALUE STRING
            x,y = self.coords[0]+self.wh[0]//2,self.coords[1]+10
            w,h = self.wh[0]-20,self.wh[1]//5
            drawBoxedTextWH(screen,(x,y),(w,h),self.quantStr,50,(0,0,0),centerX=True)

            # DRAWING THE EXTRA DATA
            x,y = self.coords[0]+10,self.coords[1]+(self.wh[1]//5)+10
            w,h = self.wh[0]-20,(self.wh[1]//5)*3-15
            data = [(key,value) for key,value,middle in self.extraData]
            middle = [middle for key,value,middle in self.extraData]
            drawLinedInfo(screen,(x,y),(w,h),data,35,(0,0,0),middle)
            
            # DRAWING THE PROCEED BUTTON
            x,y = self.coords[0]+10,self.coords[1]+(self.wh[1]//5)*4-5
            w,h = self.wh[0]-20,self.wh[1]//5-10
            result = drawClickableBoxWH(screen,(x,y),(w,h),"Proceed",35,(0,0,0),(255,255,255),mousebuttons,fill=True)

        elif self.stage == 1:
            # DRAWING THE CONFIRMATION SCREEN
            x,y = self.coords[0]+10,self.coords[1]+10
            w,h = self.wh[0]-20,self.wh[1]//5
            result = drawClickableBoxWH(screen,(x,y),(w,h),"Confirm",35,(0,0,0),(255,255,255),mousebuttons,fill=True)

            # DRAWING THE EXTRA DATA
            x,y = self.coords[0]+10,self.coords[1]+(self.wh[1]//5)+10
            w,h = self.wh[0]-20,(self.wh[1]//5)*4
            self.extraData.insert(0,("Quantity",self.quantStr,""))
            data = [(key,value) for key,value,middle in self.extraData]
            middle = [middle for key,value,middle in self.extraData]
            drawLinedInfo(screen,(x,y),(w,h),data,35,(0,0,0),middle)

        if result:
            if self.stage == 0: self.stage = 1# if the proceed button is pressed, move to the next stage
            elif self.stage == 1:
                self.stage = 0
                return True# if the confirm button is pressed, return True
            
        return False