import pygame
from Defs import *

pygame.init()
screen = pygame.display.set_mode([900,900])
pygame.display.set_caption("Pygame Shell")

class ScrollCard:
    def __init__(self) -> None:
        pass

class CdCard(ScrollCard):
    def __init__(self,image,name) -> None:
        super().__init__()
        self.wh = (450,450)
        self.name = name
        self.image = pygame.transform.scale(image,(self.wh[0],self.wh[1]))
        self.image.set_alpha(70) 
        self.coords = (50,50)
        
    def draw(self,screen):
        
        screen.blit(self.image,self.coords)
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(self.coords[0],self.coords[1],self.wh[0],self.wh[1]),5)

        screen.blit(s_render("CD",120,(0,0,0)),(self.coords[0]+10,self.coords[1]+10))

        drawCenterTxt(screen,"12 Months",75,(0,0,0),(self.coords[0]+self.wh[0]-15,self.coords[1]+30),centerX=False,centerY=False,fullX=True)

        apr = 7.63
        minBalance = 16000
        # risk = "N/A (FDIC Insured)"
        risk = "High (3.82%)"
        drawCenterTxt(screen,f"{round(apr,2)}%",130,(225,225,225),(self.coords[0]+self.wh[0]//2,self.coords[1]+self.wh[1]//2))

        x,y = self.coords[0]+10,self.coords[1]+(self.wh[1]//4)*3-20
        info = [("Name",self.name),("Min Balance",f"${limit_digits(minBalance,20,True)}"),("Risk",risk)]
        drawLinedInfo(screen,(x,y),(self.wh[0]-20,self.wh[1]//4+40),info,30,(0,0,0))

class SideScroll:
    def __init__(self,cards:list[ScrollCard],coords,wh) -> None:
        self.cards = cards# list of cards
        self.coords = coords
        self.wh = wh
        self.scroll = 0
        


bankIcons = {}
for file in os.listdir(r"Assets\bankIcons"):
    print(file)
    image = pygame.image.load(r"Assets\bankIcons\{}".format(file)).convert_alpha()
    name = file.split(".")[0]
    bankIcons[name] = SideScroll(image,name)

lastfps = deque(maxlen=300)
clock = pygame.time.Clock()
while True:
    screen.fill((60,60,60))
    # pygame.event.pump()
    # pygame.draw.circle(screen, (255,255,255), (450,450), 100)

    bankIcons["Regal Roar Savings"].draw(screen)
    screen.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(850,0),(850,30),(850,60)]))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse button pressed",pygame.mouse.get_pos())
            
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
            print("Pressed the J key")


    clock.tick(60)





