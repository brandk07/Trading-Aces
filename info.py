import pygame
from Defs import *

pygame.init()
screen = pygame.display.set_mode([900,900])
pygame.display.set_caption("Pygame Shell")

class InfoButton:
    def __init__(self,text:str,txtSize:int,txtColor:tuple,icon:str='i',iconSize:int=40) -> None:
        self.text = text
        self.txtSize = txtSize
        self.txtColor = txtColor
        # self.renderedTxt = s_render(self.text,txtSize,txtColor)
        self.icon = s_render(icon,iconSize,txtColor)
    
    def draw(self,screen,coords:tuple,lineNum:int):
        # screen.blit(self.renderedTxt,coords)
        mousex,mousey = pygame.mouse.get_pos()
        # myrect = pygame.Rect(coords[0]-25,coords[1]-15,50,50)
        # pygame.draw.rect(screen,(0,0,0),myrect)
        
        if pygame.Rect(coords[0]-25,coords[1]-15,50,50).collidepoint(mousex,mousey):
            drawBoxedLines(screen,(mousex,mousey),self.text,lineNum,self.txtSize,self.txtColor,centerX=True,fullY=True)
        screen.blit(self.icon,(coords[0],coords[1]))


infoButton = InfoButton("Not Including the added interest from bad credit score",30,(255,255,255),icon='*')
infoButton2 = InfoButton("Not Including the added interest from bad credit score",30,(255,255,255))
lastfps = deque(maxlen=300)
clock = pygame.time.Clock()
mousebuttons = 0
while True:
    screen.fill((60,60,60))
    # pygame.event.pump()
    # pygame.draw.circle(screen, (255,255,255), (450,450), 100)
    infoButton.draw(screen,(450,450),4)
    infoButton2.draw(screen,(450,50),4)
    infoButton2.draw(screen,(885,50),4)
    infoButton2.draw(screen,(885,885),4)
    infoButton2.draw(screen,(0,0),4)

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

    clock.tick(60)





