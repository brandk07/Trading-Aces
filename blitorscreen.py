import pygame
from Defs import *
from Classes.imports.UIElements.SideScroll import RunCard
from Classes.Menus.GameModeMenu import BlitzRun

pygame.init()
screen = pygame.display.set_mode([900,900])
pygame.display.set_caption("Pygame Shell")
screen.fill((60,60,60))
screen2 = screen.copy()

surface = pygame.Surface((900,900))
pygame.draw.rect(surface,(255,255,255),pygame.Rect(0,0,900,900))

lastfps = deque(maxlen=300)
clock = pygame.time.Clock()
mousebuttons = 0


# class ProgressBar:
#     def __init__(self,color=(0,255,0),txtsize=45):
#         self.txtSize = txtsize
#         self.progress : float|int = 0
#         self.color = (0,255,0)
#     def setProgress(self,progress:int|float):
#         """Progress should be a number 0,100"""
#         self.progress = progress
#     def draw(self,screen,pos,wh):

#         pygame.draw.rect(screen,self.color,pygame.Rect(pos,(wh[0]*self.progress,wh[1])),border_radius=15)
#         pygame.draw.rect(screen,(0,0,0),pygame.Rect(pos,wh),5,15)
        
#         drawCenterTxt(screen,str(int(self.progress*100))+"%",self.txtSize,(0,0,0),(pos[0]+10,pos[1]+wh[1]//2),centerX=False)

class ProgressBar():
    def __init__(self,wh,color=(0,255,0),txtsize=45) -> None:
        self.progress : float|int = 0
        self.wh = wh
        self.color = color
        self.barSurf = pygame.Surface((wh[0],wh[1])).convert_alpha()
        self.barSurf.fill((0,0,0,0))
        self.baseSurf = self.barSurf.copy().convert_alpha()# base surf is draw over the bar surf to reset the bar surf each time it needs to be updated
        self.changedVal = True

        drawBoxedImage(self.baseSurf,(0,0),self.createBaseSurf(color),borderRadius=20)# draws the rounded gradient to the base surface
        self.barSurf.blit(self.baseSurf,(0,0))# blit the base surface to the bar surface
        drawCenterTxt(self.barSurf,f"{round(self.progress,2)}%",45,(0,0,0),(10,self.wh[1]*.5),centerX=False)
    def setProgress(self,progress:int|float):
        """Progress should be a number 0,100"""
        self.progress = progress
        self.changedVal = True
    def createBaseSurf(self,gradient_start):
        numLines = int(self.wh[0]*(self.progress/100))
        surf = self.barSurf.copy()
        for i in range(numLines):
            color = (
                gradient_start[0] + (220 - gradient_start[0]) * i / numLines,
                gradient_start[1] + (220 - gradient_start[1]) * i / numLines,
                gradient_start[2] + (220 - gradient_start[2]) * i / numLines
            )
            pygame.draw.line(surf, color, (self.wh[0]-i, 0),(self.wh[0]-i, self.wh[1]))
        return surf
            

    def redraw(self):
        self.barSurf.blit(self.baseSurf,(0,0))# reset the bar surf
        drawCenterTxt(self.barSurf,f"{round(self.progress,2)}%",45,(0,0,0),(10,self.wh[1]*.5),centerX=False)# draw the value of the bar
        pygame.draw.rect(self.barSurf,(0,0,0),pygame.Rect(0,0,self.wh[0],self.wh[1]),width=5,border_radius=20)# redraw the border (self.baseSurf has one, but it get drawn over sometimes)
    
    def drawBar(self,screen,coords):

        if self.changedVal:# if the value changed or the extra text is not empty
            self.barSurf.blit(self.baseSurf,(0,0))# reset the bar surf
            drawCenterTxt(self.barSurf,f"{round(self.progress,2)}%",45,(0,0,0),(10,self.wh[1]*.5),centerX=False)# draw the value of the bar
            pygame.draw.rect(self.barSurf,(0,0,0),pygame.Rect(0,0,self.wh[0],self.wh[1]),width=5,border_radius=20)# redraw the border (self.baseSurf has one, but it get drawn over sometimes)

        screen.blit(self.barSurf,coords)
        self.changedVal = False


# pygame.transform.smoothscale()
surf = pygame.Surface((150,150)).convert_alpha()
surf.fill((255,255,255,100))
p1 = ProgressBar((300,100))
p1.setProgress(0.5)

while True:

    # for i in range(50):
    screen.fill((60,60,60))

    p1.drawBar(screen,(100,100))



    # pygame.draw.circle(screen, (255,255,255), (450,450), 100)
    # screen.blit(runCard.draw(),(300,440))

    # runCard.draw(screen,(0,0),mousebuttons)
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

    clock.tick(1000)





