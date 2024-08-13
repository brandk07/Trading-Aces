import pygame
from collections import deque
from random import randint
import math

class BuyAnimation:
    def __init__(self,coords:tuple|list,radius:int,animationList:list) -> None:
        self.coords = coords
        self.radius = radius
        self.dots = []
        self.life = 180
        self.speedMult = .2
        self.animationList : list = animationList
        for i in range(100):
            color = (randint(0,255),randint(0,255),randint(0,255))
            rads = math.radians(randint(0,360))
            amplitude = randint(int(self.radius/2),self.radius*10)/10
            coords = (self.coords[0]+amplitude*math.cos(rads),self.coords[1]+amplitude*math.sin(rads))
            size = randint(1,5)
            slope = (coords[0]-self.coords[0])*self.speedMult,(coords[1]-self.coords[1])*self.speedMult# (xslope,yslope)
            self.dots.append((coords,color,size,slope))
       
    def update(self,screen:pygame.Surface):
        for i in range(len(self.dots)):
            coords,color,size,slope = self.dots[i]
            coords = (coords[0]+slope[0],coords[1]+slope[1])# adjust the coords by the slope
            size = min(max(1,size+randint(-1,1)),5)
            self.dots[i] = (coords,color,size,slope)
        self.draw(screen)
        self.life -= 1
        if self.life == 0:
            self.animationList.remove(self)
    def draw(self,screen):
        for coords,color,size,slope in self.dots:
            pygame.draw.circle(screen,color,coords,size)

# EXAMPLE USAGE
# animationList = []
# while True:
#     screen.fill((0, 0, 0))

#     # pygame.draw.circle(screen, (255, 255, 255), (450, 450), 100)
    
    
#     screen.blit(text_surface, (350, 800))  # Position the text at (350, 800)
    
#     screen.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(850,0),(850,30),(850,60)]))

#     for animation in animationList:
#         animation.update(screen)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
#             pygame.quit()
#             quit()
#         elif event.type == pygame.MOUSEBUTTONDOWN:
#             print("Mouse button pressed", pygame.mouse.get_pos())
#             animationList.append(BuyAnimation(pygame.mouse.get_pos(),100,animationList))

#     pygame.display.update()
#     clock.tick(60)