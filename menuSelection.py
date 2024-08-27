import pygame
from Defs import *

pygame.init()
screen = pygame.display.set_mode([900,900],pygame.SRCALPHA)
pygame.display.set_caption("Pygame Shell")

class MenuSelection:
    def __init__(self,coords,wh,choices,txtsize,colors=None) -> None:
        assert len(choices) == len(colors) if colors else True
        self.coords = coords
        self.wh = wh
        self.colors = colors if colors else [(0,0,0) for _ in range(len(choices))]
        self.choices = [s_render(choice,txtsize,self.colors[i]) for i,choice in enumerate(choices)]
        self.selectedChoices = [s_render(choice,txtsize,(255,255,255)) for choice in choices]
        self.selected = 0# the index of the selected choice
    def getSelected(self,index=False):
        """Returns the selected choice or its index"""
        return self.choices[self.selected] if not index else self.selected
    def setSelected(self,index):
        """Sets the selected choice"""
        self.selected = index
    def draw(self,screen,mousebuttons):
        """Draws the menu selection onto the screen"""
        width  = self.wh[0]//len(self.choices)
        for i,choice in enumerate(self.choices):
            drawCenterRendered(screen,choice,(self.coords[0]+width//2+i*width,self.coords[1]+self.wh[1]//2))
            if self.selected == i:# Draws the selected choice (choice in white)
                # draw a line under the selected choice
                ylevel = self.coords[1]+self.wh[1]-20
                pygame.draw.line(screen,(255,255,255),(self.coords[0]+i*width+20,ylevel),(self.coords[0]+i*width+width-20,ylevel),4)
    
            if i != len(self.choices)-1:# Draws a vertical line to separate the choices
                pygame.draw.line(screen,(0,0,0),(self.coords[0]+width*(i+1),self.coords[1]+20),(self.coords[0]+width*(i+1),self.coords[1]+self.wh[1]-20),4)

            if pygame.Rect(self.coords[0]+i*width,self.coords[1],width,self.wh[1]).collidepoint(*pygame.mouse.get_pos()) and mousebuttons == 1:
                self.selected = i
        pygame.draw.rect(screen,(0,0,0),(*self.coords,*self.wh),5,10)# draw the border of the whole menu

lastfps = deque(maxlen=300)
clock = pygame.time.Clock()
mousebuttons = 0
menu = MenuSelection((100,100),(450,150),["Start","Options","Quit"],50,[None,(0,255,0),(255,0,0)])
while True:
    screen.fill((60,60,60))
    # pygame.event.pump()
    # pygame.draw.circle(screen, (255,255,255), (450,450), 100)

    menu.draw(screen,mousebuttons)
    # pygame.draw.rect(screen,(0,0,0,50),(100,100,450,150))
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





