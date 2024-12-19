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




# pygame.transform.smoothscale()
surf = pygame.Surface((150,150)).convert_alpha()
surf.fill((255,255,255,100))

while True:

    # for i in range(50):
    screen.fill((60,60,60))




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





