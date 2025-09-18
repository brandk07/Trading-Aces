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

    def createBaseSurf(self, gradient_start):
        surf = self.baseSurf.copy()
        numLines = int(self.wh[0] * (self.progress/100))
        
        for i in range(numLines):
            percent = i / self.wh[0]
            
            color = (
                int(220 - ((220 - gradient_start[0]) * percent)),
                int(220 - ((220 - gradient_start[1]) * percent)),
                int(220 - ((220 - gradient_start[2]) * percent))
            )
            
            color = tuple(max(0, min(255, c)) for c in color)
            
            pygame.draw.line(surf, color, (i, 0), (i, self.wh[1]))
        return surf
            

    def redraw(self):
        self.barSurf.fill((0,0,0,0))
        drawBoxedImage(self.barSurf,(0,0),self.createBaseSurf(self.color),borderRadius=20)# draws the rounded gradient to the base surface
        drawCenterTxt(self.barSurf,f"{round(self.progress,2)}%",45,(0,0,0),(10,self.wh[1]*.5),centerX=False)# draw the value of the bar
        pygame.draw.rect(self.barSurf,(0,0,0),pygame.Rect(0,0,self.wh[0],self.wh[1]),width=5,border_radius=20)# redraw the border (self.baseSurf has one, but it get drawn over sometimes)
    
    def drawBar(self,screen,coords):

        if self.changedVal:# if the value changed or the extra text is not empty
            self.redraw()
        screen.blit(self.barSurf,coords)
        self.changedVal = False


# pygame.transform.smoothscale()
surf = pygame.Surface((150,150)).convert_alpha()
surf.fill((255,255,255,100))
p1 = ProgressBar((300,100))
p1.setProgress(0)

while True:

    # for i in range(50):
    screen.fill((60,60,60))

    # p1.drawBar(screen,(100,100))
    # for iii in range(3):
    # for ii in range(3):
    #     for i in range(12):
    #         # if iii == 0 or ii == 0 and i == 0 :
    #         #     drawCenterTxt(screen,f"{(255-i*10,ii*10,iii*10)}",40,(255-i*10,ii*10,iii*10),(0+ii*150+iii*150,5),centerX=False)
    #         # if iii == 2 and i == 2:
    #         #     drawCenterTxt(screen,f"{(255-i*10,ii*10,iii*10)}",40,(255-i*10,ii*10,iii*10),(650,50+i*35),centerX=False)
    #         drawCenterTxt(screen,"Hello World",40,(255-i*10,ii*10,0),(0+ii*150,50+i*35),centerX=False)
    for i in range(10000):
        import pygame
    #     drawCenterTxt(screen,str(randint(0,10000)),80,(224, 9, 9),(100,i),centerX=False)
    # pygame.draw.circle(screen, (255,255,255), (450,450), 100)
    # screen.blit(runCard.draw(),(300,440))

    # runCard.draw(screen,(0,0),mousebuttons)
    # screen.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(850,0),(850,30),(850,60)]))
    fps_text = f"FPS: {clock.get_fps():.2f}"
    drawCenterTxt(screen,fps_text,24,(255,255,255),(10,200),centerX=False)
    
    pygame.display.flip()
    
    mousebuttons = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousebuttons = event.button
            if mousebuttons == 1:
                p1.setProgress(p1.progress+3)
                print("Mouse button pressed",pygame.mouse.get_pos())
            
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
            print("Pressed the J key")

    clock.tick(1000)





