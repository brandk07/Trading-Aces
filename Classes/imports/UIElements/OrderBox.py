import pygame
from Defs import *

class OrderBox:
    def __init__(self,coords:tuple,wh:tuple,gametime) -> None:
        self.coords = list(coords)
        self.wh = list(wh)
        self.gametime = gametime
        self.quantStr = ""
        self.extraData = []
        self.stage = 0# 0 is the first stage (proceeding to confirm screen), 1 is the second stage (confirming the order)
        self.middleData = []
    def reset(self):
        self.stage = 0
        self.extraData = []
        self.quantStr = ""
        
    def loadData(self,quantStr:str,totalStr:str,extraData:list[tuple[str,str,str]]) -> None:
        """extraData is [(key,value,middleVal)]"""
        
        # Condensed code
        def update_extra_data():
            self.extraData = extraData
            self.extraData.append(("Total", totalStr, ""))
            self.quantStr = quantStr

        if self.stage == 1:
            if self.extraData[0][0] == "Quantity":
                extra_slice = self.extraData[1:-1]
            else:
                extra_slice = self.extraData[:-1]
            if extra_slice != extraData or self.quantStr != quantStr:
                self.stage = 0
                update_extra_data()
        else:
            update_extra_data()
        


    def draw(self,screen:pygame.Surface,mousebuttons:int,resetClicked=True) -> bool:
        """Returns True if the confirm button is pressed resets after confirm button is pressed"""
        
        pygame.draw.rect(screen,(50,50,50),pygame.Rect(self.coords[0],self.coords[1],self.wh[0],self.wh[1]),border_radius=15)
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(self.coords[0],self.coords[1],self.wh[0],self.wh[1]),5,15)


        if self.stage == 0:
            # DRAWING THE VALUE STRING
            x,y = self.coords[0]+self.wh[0]//2,self.coords[1]+10
            w,h = self.wh[0]-20,self.wh[1]//5
            drawBoxedTextWH(screen,(x,y),(w,h),self.quantStr,50,(0,0,0),centerX=True)

            # DRAWING THE EXTRA DATA
            x,y = self.coords[0]+10,self.coords[1]+(self.wh[1]//5)+10
            w,h = self.wh[0]-20,(self.wh[1]//5)*3-15
            if self.extraData:
                data = [(key,value) for key,value,middle in self.extraData]
                middle = [middle for key,value,middle in self.extraData]
                drawLinedInfo(screen,(x,y),(w,h),data,35,(0,0,0),middleData=middle)
            
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
            if self.extraData[0][0] == "Quantity":
                self.extraData[0] = ("Quantity",self.quantStr,"")
                
            data = [(key,value) for key,value,middle in self.extraData]
            middle = [middle for key,value,middle in self.extraData]
            drawLinedInfo(screen,(x,y),(w,h),data,35,(0,0,0),middleData=middle)

        if result:
            if self.gametime.speedBar.getValue() > 0 and not self.gametime.speedBar.frozen:
                errors.addMessage("Can't Proceed While Game Running")
                return False
            if self.stage == 0: self.stage = 1# if the proceed button is pressed, move to the next stage
            elif self.stage == 1:
                self.stage = 0
                self.extraData = []
                return True# if the confirm button is pressed, return True
            
        return False