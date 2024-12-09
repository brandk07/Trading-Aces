import pygame
from Defs import *

pygame.init()
screen = pygame.display.set_mode([900,900])
pygame.display.set_caption("Pygame Shell")

class Bar():
    def __init__(self,maxVal,wh,sliderW,color) -> None:
        self.maxVal = maxVal
        self.val = 0
        self.wh = wh
        self.color = color
        self.barSurf = pygame.Surface((wh[0],wh[1])).convert_alpha()
        self.barSurf.fill((0,0,0,0))
        self.baseSurf = self.barSurf.copy().convert_alpha()# base surf is draw over the bar surf to reset the bar surf each time it needs to be updated
        drawBoxedImage(self.baseSurf,(0,0),self.createBaseSurf(color),borderRadius=20)# draws the rounded gradient to the base surface
        self.barSurf.blit(self.baseSurf,(0,0))# blit the base surface to the bar surface
        drawCenterTxt(self.barSurf,str(self.val)+"x" ,45,(0,0,0),(self.wh[0]*.5,self.wh[1]*.5))# draw the value of the bar
        self.sliderW = sliderW
    def getValue(self):
        return self.val
    def changeMaxValue(self,newMax):
        self.maxVal = newMax
        self.value = self.value if self.value < newMax else newMax
    
    def createBaseSurf(self,gradient_start):
        numLines = self.wh[0]
        surf = self.barSurf.copy()
        for i in range(numLines):
            color = (
                gradient_start[0] + (220 - gradient_start[0]) * i / numLines,
                gradient_start[1] + (220 - gradient_start[1]) * i / numLines,
                gradient_start[2] + (220 - gradient_start[2]) * i / numLines
            )
            pygame.draw.line(surf, color, (self.wh[0]-i, 0),(self.wh[0]-i, self.wh[1]))
        return surf
    def scrollDetection(self,mousebuttons):
        """Look for mousewheel scrolling"""
        if mousebuttons == 4:
            self.val = min(self.maxVal,self.val+1)
            return True
        elif mousebuttons == 5:
            self.val = max(0,self.val-1)
            return True
        return False

    def collisionDetection(self,coords,mousebuttons) -> bool:
        """Returns True if the value has changed"""
        mousex,mousey = pygame.mouse.get_pos()
        n = False
        if pygame.Rect(coords[0],coords[1],self.wh[0],self.wh[1]).collidepoint(mousex,mousey):
            n = self.scrollDetection(mousebuttons)
            if pygame.mouse.get_pressed()[0]:
                ratio = (self.wh[0]-self.sliderW) / self.maxVal
                spotInRatio = int(((mousex+self.sliderW*.5) - coords[0] - self.sliderW) / ratio)
                spotInRatio = max(0,spotInRatio)
                spotInRatio = min(self.maxVal,spotInRatio)

                n = n or (self.val != spotInRatio)
                self.val = spotInRatio   
            
        return n
            
    def drawSlider(self,coords):
        mousex,mousey = pygame.mouse.get_pos()
        x = int((self.val/self.maxVal) * (self.wh[0]-self.sliderW))
        pygame.draw.rect(self.barSurf,(170,170,170),pygame.Rect(x,0,self.sliderW,self.wh[1]),border_radius=20)
        pygame.draw.rect(self.barSurf,(0,0,0),pygame.Rect(x,0,self.sliderW,self.wh[1]),width=5,border_radius=20)

    def determineExtraTxt(self):
        """Determines the extra text to be drawn on the bar"""
        return ""
    
    def drawBar(self,screen,coords,mousebuttons):
        changedVal = self.collisionDetection(coords,mousebuttons)# Need to check if the value has changed first

        if (txt:=self.determineExtraTxt()) != "" or changedVal:# if the value changed or the extra text is not empty
            self.barSurf.blit(self.baseSurf,(0,0))# reset the bar surf
            self.drawSlider(coords)
            txt = str(self.val)+"x" if txt == "" else txt
            drawCenterTxt(self.barSurf,txt,45,(0,0,0),(self.wh[0]*.5,self.wh[1]*.5))# draw the value of the bar
            pygame.draw.rect(self.barSurf,(0,0,0),pygame.Rect(0,0,self.wh[0],self.wh[1]),width=5,border_radius=20)# redraw the border (self.baseSurf has one, but it get drawn over sometimes)

        screen.blit(self.barSurf,coords)
    
class TimeBar(Bar):
    def __init__(self,maxVal,wh,sliderW,color) -> None:
        super().__init__(maxVal,wh,sliderW,color)
    def determineExtraTxt(self):
        txt = "" if self.val != 69 else "Nice"
        return txt


lastfps = deque(maxlen=300)
clock = pygame.time.Clock()
bar1 = TimeBar(90,(450,100),50,(0,180,0))
mousebuttons = 0
while True:
    screen.fill((60,60,60))
    # pygame.event.pump()
    # pygame.draw.circle(screen, (255,255,255), (45
    # 0,450), 100)

    bar1.drawBar(screen,(300,300),mousebuttons)

    screen.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(850,0),(850,30),(850,60)]))
    pygame.display.flip()
    
    mousebuttons = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousebuttons = event.button
            if mousebuttons == 1:
                print("Mouse button pressed",pygame.mouse.get_pos())
            
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
            print("Pressed the J key")

    clock.tick(120)





