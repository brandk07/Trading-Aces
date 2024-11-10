import pygame
from Defs import *

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


temp_surface = pygame.Surface((900, 900))
temp_surface.fill((60, 60, 60))
pygame.draw.rect(temp_surface,(0,255,255),pygame.Rect(0,0,500,100))
background_bytes = bytes(temp_surface.get_buffer())


while True:

    for i in range(50):
        # screen.fill((60,60,60))
        # gfxdraw.filled_polygon(screen,[(0,0),(900,0),(900,900),(0,900)],(60,60,60))

        pixels = screen.get_buffer()
        pixels.write(background_bytes)
        del pixels  # Release the buffer

        # screen.blit(screen2,(0,0))
        # screen = screen2.copy()
        # screen.blit(surface,(0,0))
        # screen = surface.copy()


    pygame.draw.circle(screen, (255,255,255), (450,450), 100)
    screen.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(850,0),(850,30),(850,60)]))
    
    pygame.display.flip()
    # pygame.display.update()
    
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





