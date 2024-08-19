import pygame
from Defs import *

pygame.init()
screen = pygame.display.set_mode([900,900])
pygame.display.set_caption("Pygame Shell")

class OrderBox:
    def __init__(self,coords:tuple,wh:tuple) -> None:
        self.coords = list(coords)
        self.wh = list(wh)
        self.quantStr = ""
        self.extraData = []
        self.stage = 0# 0 is the first stage (proceeding to confirm screen), 1 is the second stage (confirming the order)
        self.middleData = []
    def loadData(self,quantStr:str,totalStr:str,extraData:list[tuple[str,str,str]]):
        """extraData is [(key,value,middleVal)]"""
        self.extraData = extraData
        self.extraData.append(("Total",totalStr,""))
        self.quantStr = quantStr

    def draw(self,screen:pygame.Surface,mousebuttons:int) -> bool:
        """Returns True if the confirm button is pressed"""
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(self.coords[0],self.coords[1],self.wh[0],self.wh[1]),5,15)

        if self.stage == 0:
            # DRAWING THE VALUE STRING
            x,y = self.coords[0]+self.wh[0]//2,self.coords[1]+10
            w,h = self.wh[0]-20,self.wh[1]//5
            drawBoxedTextWH(screen,(x,y),(w,h),self.quantStr,50,(0,0,0),centerX=True)

            # DRAWING THE EXTRA DATA
            x,y = self.coords[0]+10,self.coords[1]+(self.wh[1]//5)+25
            w,h = self.wh[0]-20,(self.wh[1]//5)*3
            data = [(key,value) for key,value,middle in self.extraData]
            middle = [middle for key,value,middle in self.extraData]
            drawLinedInfo(screen,(x,y),(w,h),data,35,(0,0,0),middle)
            
            # DRAWING THE PROCEED BUTTON
            x,y = self.coords[0]+10,self.coords[1]+(self.wh[1]//5)*4-5
            w,h = self.wh[0]-20,self.wh[1]//5-10
            result = drawClickableBoxWH(screen,(x,y),(w,h),"Proceed",35,(0,0,0),(255,255,255),mousebuttons,fill=True)

        elif self.stage == 1:
            # DRAWING THE CONFIRMATION SCREEN
            x,y = self.coords[0]+10,self.coords[1]+10
            w,h = self.wh[0]-20,self.wh[1]//5
            result = drawClickableBoxWH(screen,(x,y),(w,h),"Confirm",35,(0,0,0),(255,255,255),mousebuttons,fill=True)

            # DRAWING THE EXTRA DATA
            x,y = self.coords[0]+10,self.coords[1]+(self.wh[1]//5)+25
            w,h = self.wh[0]-20,(self.wh[1]//5)*4
            self.extraData.insert(0,("Quantity",self.quantStr,""))
            data = [(key,value) for key,value,middle in self.extraData]
            middle = [middle for key,value,middle in self.extraData]
            drawLinedInfo(screen,(x,y),(w,h),data,35,(0,0,0),middle)

        if result:
            if self.stage == 0: self.stage = 1# if the proceed button is pressed, move to the next stage
            elif self.stage == 1:
                return True# if the confirm button is pressed, return True
            
        return False

orderbox = OrderBox((100,100),(300,400))
lastfps = deque(maxlen=300)
mousebuttons = 0
clock = pygame.time.Clock()
while True:
    screen.fill((60,60,60))
    # pygame.event.pump()
    # pygame.draw.circle(screen, (255,255,255), (450,450), 100)
    orderbox.loadData("2,513 Shares",f"$252,556.5",[("Value","$100.5","x"),("Fee","1.2%","x")])

    orderbox.draw(screen,mousebuttons)
    screen.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(850,0),(850,30),(850,60)]))
    pygame.display.flip()


    mousebuttons = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()            
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
            print("Pressed the J key")

        elif event.type == pygame.MOUSEBUTTONDOWN and mousebuttons == 0:# left mouse button
                mousebuttons = event.button
                if mousebuttons == 1:
                    print("Mouse button pressed",pygame.mouse.get_pos())


    clock.tick(60)




