import pygame
from Defs import *

pygame.init()
screen = pygame.display.set_mode([1850,1000])
pygame.display.set_caption("Pygame Shell")

class ScrollCard:
    def __init__(self) -> None:
        pass

class CdCard(ScrollCard):
    def __init__(self,image,name,sideScroll) -> None:
        """Needs to be given the sideScroll object that will be used to draw the card"""
        super().__init__()
        self.wh = (450,450)
        self.name = name
        self.image = pygame.transform.scale(image,((self.wh[1]//4)*3-30,(self.wh[1]//4)*3-30))
        self.image.set_alpha(70) 
        self.sideScroll = sideScroll
        self.surf = pygame.Surface(self.wh)
        self.data = {
            "duration":12,
            "apr":7.63,
            "minBalance":16000,
            "risk":"High (3.82%)"# "N/A (FDIC Insured)"
        }
        self.needToUpdate = True# if the card surf needs to be updated
        

    def updateData(self,data:dict):
        self.data = data
    @lru_cache(maxsize=1)
    def getPartialSurf(self,cutOff,direction):
        """Returns a surface that has cutOff pixels cut off from the direction"""
        if direction == "left":
            return self.surf.subsurface(pygame.Rect(cutOff,0,self.wh[0]-cutOff,self.wh[1]))
        else:
            return self.surf.subsurface(pygame.Rect(0,0,self.wh[0]-cutOff,self.wh[1]))
        
        # return self.surf.subsurface(pygame.Rect(0,0,cutOff,self.wh[1]))
    def draw(self,screen,coords,mousebuttons,minX,maxX) -> bool:
        """Draws the card onto the screen at the given coords"""
        coords = list(coords)
        if coords[0]+self.wh[0] < minX or coords[0] > maxX:
            return False

        if self.needToUpdate:
            self.updateSurf()
            self.needToUpdate = False

        newSurf = self.surf
        if coords[0] < minX and coords[0]+self.wh[0] > minX:
            newSurf = self.getPartialSurf(minX-coords[0],"left")
            coords[0] += (minX-coords[0])
        elif coords[0]+self.wh[0] > maxX:
            newSurf = self.getPartialSurf(coords[0]+self.wh[0]-maxX,"right")
        screen.blit(newSurf,coords)
        
        if pygame.Rect(coords[0],coords[1],self.wh[0],self.wh[1]).collidepoint(pygame.mouse.get_pos()):
            if mousebuttons == 1:
                return True
        return False
    def updateSurf(self):
        """Draws Everything onto the card's surface - Only needs to be called when data changes"""
        pygame.draw.rect(self.surf,(60,60,60),pygame.Rect(0,0,self.wh[0],self.wh[1]))
        self.surf.blit(self.image,(0+self.wh[0]//8,0))
        pygame.draw.rect(self.surf,(0,0,0),pygame.Rect(0,0,self.wh[0],self.wh[1]),5)

        self.surf.blit(s_render("CD",120,(0,0,0)),(0+10,0+10))

        drawCenterTxt(self.surf,f"{self.data['duration']} Months",75,(0,0,0),(0+self.wh[0]-15,0+30),centerX=False,centerY=False,fullX=True)

        drawCenterTxt(self.surf,f"{round(self.data['apr'],2)}%",130,(225,225,225),(0+self.wh[0]//2,0+self.wh[1]//2))

        x,y = 0+10,0+(self.wh[1]//4)*3-20
        info = [("Name",self.name),("Min Balance",f"${limit_digits(self.data['minBalance'],20,True)}"),("Risk",self.data['risk'])]

        drawLinedInfo(self.surf,(x,y),(self.wh[0]-20,self.wh[1]//4+40),info,30,(0,0,0))

        

class SideScroll:
    def __init__(self,coords,wh,cardWH) -> None:
        self.cards : list[ScrollCard] = []# list of cards
        self.coords = coords
        self.cardWH = cardWH
        self.wh = wh
        self.scroll = 0
        self.mouseScrollTime = 0
        self.lastSelected = -1# the index of the last selected card
        self.scrollSpeed = 35
    def getCard(self,index=False):
        """Returns the card that is currently in the center of the screen
        If index is True, it will return the index of the card"""
        newSelected = self.scroll//self.cardWH[0]
        # if self.lastSelected != newSelected:
        #     self.scroll = newSelected*self.cardWH[0]+self.cardWH[0]//2
        self.lastSelected = self.scroll//self.cardWH[0]
        if index:
            return self.lastSelected
        return self.cards[self.lastSelected]
    def setCard(self,index):
        """Sets the card that is currently in the center of the screen"""
        self.scroll = index*self.cardWH[0]+self.cardWH[0]//2
    def loadCards(self,cards:list[ScrollCard]):
        """Needs to be called before the draw method"""
        self.cards : ScrollCard = cards
    def scrollControls(self,mousebuttons):
        if mousebuttons == 4:
            self.scroll += self.scrollSpeed
        elif mousebuttons == 5:
            self.scroll -= self.scrollSpeed
        self.scroll = max(0,min(self.scroll,self.cardWH[0]*(len(self.cards)-1)))
        
    def draw(self,screen,mousebuttons):
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(self.coords[0],self.coords[1],self.wh[0],self.wh[1]),10)
        self.scrollControls(mousebuttons)
        print(self.scroll)
        
        middle = self.coords[0]+self.wh[0]//2
        ypos = self.coords[1]+20
        index = self.getCard(index=True)
        offset = -(self.scroll%self.cardWH[0])
        #draw a rect for the selected card
        pygame.draw.rect(screen,(255,255,255),pygame.Rect(middle-self.cardWH[0]-10+offset+self.cardWH[0],ypos-10,self.cardWH[0]+20,self.cardWH[1]+20),10)
        minX,maxX = self.coords[0]+20,self.coords[0]+self.wh[0]-20
        self.cards[index].draw(screen,(middle+offset,ypos),mousebuttons,minX,maxX)
        for i,card in enumerate(self.cards):
            if i != index:
                if card.draw(screen,(middle+(i-index)*(self.cardWH[0]+25)+offset,ypos),mousebuttons,minX,maxX):
                    self.setCard(i)
        # if index > 0:
        #     if self.cards[index-1].draw(screen,(middle-475+offset,ypos),mousebuttons,minX,maxX):
        #         self.setCard(index-1)
        # if index < len(self.cards)-1:
        #     if self.cards[index+1].draw(screen,(middle+475+offset,ypos),mousebuttons,minX,maxX):
        #         self.setCard(index+1)


        
        

sideSroll = SideScroll((50,50),(1350,500),(450,450))
bankIcons = {}
for file in os.listdir(r"Assets\bankIcons"):
    print(file)
    image = pygame.image.load(r"Assets\bankIcons\{}".format(file)).convert_alpha()
    name = file.split(".")[0]
    bankIcons[name] = CdCard(image,name,sideSroll)

sideSroll.loadCards(list(bankIcons.values()))



background = pygame.image.load(r'Assets\backgrounds\Background (9).png').convert_alpha()
background = pygame.transform.smoothscale_by(background,2);background.set_alpha(100)

lastfps = deque(maxlen=300)
clock = pygame.time.Clock()
mousebuttons = 0
while True:
    screen.fill((60,60,60))
    # pygame.event.pump()
    screen.blit(background,(0,0))
    # pygame.draw.circle(screen, (255,255,255), (450,450), 100)

    sideSroll.draw(screen,mousebuttons)


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


    clock.tick(250)





