import pygame
from Defs import *

pygame.init()
screen = pygame.display.set_mode([900,900])
pygame.display.set_caption("Pygame Shell")

class Newlatter: 
    def __init__(self,wh,elementHeight) -> None:
        self.data = []
        self.elementHeight = elementHeight
        self.strings = []
        self.wh = wh
        self.coords = []
        self.surf = pygame.Surface((self.wh[0],self.wh[1])).convert_alpha()
        self.needToUpdate = True
        self.scrollvalue = 0
    
    def setStrings(self,stringData:list[list[str,int,tuple]]):
        """string Data should be [[string,size,color],n times]"""
        assert stringData, "String data is empty"
        assert len(stringData[0][0]) == 3, "Each index in String data should have 3 elements [string,size,color]"

        if len(stringData) == len(self.strings):# if the data is the same
            same = True
            for element in stringData:
                if element[0] not in self.strings:
                    same = False
                    break
            if same:
                return
        self.strings = [[string for (string,size,color) in element] for element in stringData]
        self.data = [[(string,size,color) for (string,size,color) in element] for element in stringData]
        self.needToUpdate = True
    
    def setStrCoords(self,coords:list):
        """Coords relative to each box in the latter
        all the elements in strings will use just this 1 list of coords [(x,y),(x,y),n times]"""
        assert coords, "Coords is empty"
        self.coords = coords
        self.needToUpdate = True

    def updateSurf(self):
        self.surf.fill((0,0,0,0))
        self.needToUpdate = False

        for i,element in enumerate(self.data):
            print(element,len(element))
            y = (i*self.elementHeight)+self.scrollvalue
            if y < self.wh[1] or y+self.elementHeight > 0:
                if i != 0:
                    pygame.draw.line(self.surf,(0,0,0),(15,20+y),(self.wh[0]-15,20+y),3)

                for ii,(string,size,color) in enumerate(element):
                    # print(string,size,color)
                    drawCenterTxt(self.surf,string,size,color,(self.coords[ii][0],self.coords[ii][1]+y),centerY=False)

    def scrollcontrols(self, mousebuttons, coords, wh):
        mousex,mousey = pygame.mouse.get_pos()
        if pygame.Rect.collidepoint(pygame.Rect(coords[0],coords[1],wh[0],wh[1]),mousex,mousey):
            if mousebuttons == 4 and self.scrollvalue > 0:
                self.scrollvalue -= 30; self.needToUpdate = True
            elif mousebuttons == 5:
                self.scrollvalue += 30; self.needToUpdate = True

    def draw(self,screen,mousebuttons:int,coords:tuple):
        if self.needToUpdate:
            print("Updating")
            self.updateSurf()
        # pygame.draw.rect(screen,(0,0,0),pygame.Rect(0,0,self.wh[0],self.wh[1]))
        screen.blit(self.surf,(coords))
        self.scrollcontrols(mousebuttons,coords,self.wh)


newlatter = Newlatter((400,300),100)
newlatter.setStrings([[["Hello",50,(255,55,55)],["World",25,(255,255,0)]],
                      [["ByeBye",55,(255,255,30)],["World",50,(255,0,255)]],
                      [["01/05/2032",50,(255,255,255)],["time is here",50,(255,10,255)]]
                      ])
newlatter.setStrCoords([(50,50),(250,50)])

lastfps = deque(maxlen=300)
clock = pygame.time.Clock()
mousebuttons = 0
while True:
    screen.fill((60,60,60))
    # pygame.event.pump()
    # pygame.draw.circle(screen, (255,255,255), (450,450), 100)
    for i in range(10):
        newlatter.draw(screen,mousebuttons,(150,150))

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

    clock.tick(600)





