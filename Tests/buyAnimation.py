import pygame
from collections import deque
from random import randint

pygame.init()
screen = pygame.display.set_mode([900, 900])
pygame.display.set_caption("Pygame Shell")
clock = pygame.time.Clock()

# Initialize font module and create a font object
pygame.font.init()
font = pygame.font.SysFont('Arial', 36)

text_surface = font.render('Hello, Pygame!', True, (255, 255, 255))

def update_fps(clock:pygame.time.Clock,lastfps:deque):
    fps = str(int(clock.get_fps()))
    lastfps.append(fps)
    fps_text = font.render(fps, True, (225,64,35))
    intlastfps = [int(fps) for fps in lastfps]
    averagefps = sum(intlastfps)/len(lastfps)
    averagefps_text = font.render(str(int(averagefps)), True, (225,64,35))
    lowestfps = min(intlastfps)
    lowestfps_text = font.render(str(lowestfps), True, (225,64,35))
    return fps_text,averagefps_text,lowestfps_text

lastfps = deque(maxlen=300)

class BuyAnimation:
    def __init__(self,coords,wh,animationList) -> None:
        self.coords = coords
        self.wh = wh
        self.dots = []
        self.life = 240
        for i in range(50):
            color = (randint(0,255),randint(0,255),randint(0,255))
            coords = (randint(self.coords[0],self.coords[0]+wh[0]),randint(self.coords[1],self.coords[1]+wh[1]))
            size = randint(1,5)
            self.dots.append((coords,color,size))
        # print(self.dots)
       
    def update(self):
        for i in range(len(self.dots)-1,0,-1):
            coords,color,size = self.dots[i]
            coords = (coords[0]+randint(-1,1),coords[1]+randint(-1,1))
            size = min(max(1,size+randint(-1,1)),5)
            self.dots[i] = (coords,color,size)
        self.draw(screen)
        self.life -= 1
        if self.life == 0:
            animationList.remove(self)
    def draw(self,screen):
        # pygame.draw.rect(screen,(255,255,255),pygame.Rect(self.coords,self.wh))
        for coords,color,size in self.dots:
            pygame.draw.circle(screen,color,coords,size)
    
animationList = []
while True:
    screen.fill((0, 0, 0))

    # pygame.draw.circle(screen, (255, 255, 255), (450, 450), 100)
    
    
    screen.blit(text_surface, (350, 800))  # Position the text at (350, 800)
    
    screen.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(850,0),(850,30),(850,60)]))

    for animation in animationList:
        animation.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse button pressed", pygame.mouse.get_pos())
            animationList.append(BuyAnimation(pygame.mouse.get_pos(),(100,100),animationList))

    pygame.display.update()
    clock.tick(60)