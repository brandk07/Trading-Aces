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

# blitzRun = BlitzRun(f'Blitz run that will make your socks fall off becuase',1000.15,randint(0,5000),[randint(0,15000),randint(0,15000),randint(0,15000)],startTime="03/04/2030 09:30:20 AM")
# runCard = RunCard(None,blitzRun,(380,370))
def remove_near_white_background(image, tolerance=5):
    """
    Removes colors that are close to white (255,255,255) within specified tolerance
    Args:
        image: pygame Surface to modify
        tolerance: how far from 255 a color channel can be (default 5)
    """
    # Convert image to format that supports per-pixel alpha
    image = image.convert_alpha()
    
    # Get pixel array for direct manipulation
    px_array = pygame.PixelArray(image)
    
    # Get image dimensions
    width, height = image.get_size()
    
    # Check each pixel
    for x in range(width):
        for y in range(height):
            r, g, b, a = image.get_at((x, y))
            # If all RGB values are within tolerance of 255, make pixel transparent
            if (255 - r <= tolerance and 
                255 - g <= tolerance and 
                255 - b <= tolerance):
                px_array[x, y] = (r, g, b, 0)  # Set alpha to 0
    
    # Delete pixel array to unlock surface
    del px_array
    return image

image1 = pygame.image.load("modeIcon.jpg").convert_alpha()
image1 = remove_near_white_background(image1, tolerance=15)
image1 = pygame.transform.smoothscale(image1,(200,200))

image2 = pygame.image.load("mode2icon.jpg")


image2 = remove_near_white_background(image2, tolerance=15)
image2 = pygame.transform.smoothscale(image2,(200,200))

# image = pygame.transform.chop(image,pygame.Rect(200,0,1700,1080))

# pygame.transform.smoothscale()
surf = pygame.Surface((150,150)).convert_alpha()
surf.fill((255,255,255,100))

while True:

    # for i in range(50):
    screen.fill((60,60,60))
    # screen.blit(surf,(0,0))
    # screen.blit(image,(0,0))
    screen.blit(image1,(0,0))
    screen.blit(image2,(200,0))



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





