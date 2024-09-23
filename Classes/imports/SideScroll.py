import pygame
from Defs import *

# pygame.init()
# screen = pygame.display.set_mode([1850,1000])
# pygame.display.set_caption("Pygame Shell")

class ScrollCard:
    def __init__(self,name,sideScroll,data,wh) -> None:
        self.wh = wh
        self.name :str = name
        self.sideScroll : SideScroll = sideScroll
        self.surf = pygame.Surface(self.wh).convert_alpha()

        self.data = data
        self.needToUpdate = True# if the card surf needs to be updated

    def getData(self) -> dict:
        return self.data
    
    def updateData(self,data:dict):
        self.data = data
        self.needToUpdate = True
    @lru_cache(maxsize=3)
    def getPartialSurf(self,cutOff,direction):
        """Returns a surface that has cutOff pixels cut off from the direction"""
        if direction == "left":
            return self.surf.subsurface(pygame.Rect(cutOff,0,self.wh[0]-cutOff,self.wh[1]))
        else:
            return self.surf.subsurface(pygame.Rect(0,0,self.wh[0]-cutOff,self.wh[1]))

    def draw(self,screen,coords,mousebuttons,minX=None,maxX=None,customWh=None) -> bool:
        """Draws the card onto the screen at the given coords"""
        if minX == None and maxX == None:
            minX,maxX = 0,screen.get_width()
        if customWh != None:# if the card was resized, then the card needs to be updated (temporarily)
            self.needToUpdate = True

        coords = list(coords)
        if coords[0]+self.wh[0] < minX+20 or coords[0] > maxX:
            return False

        if self.needToUpdate:
            self.updateSurf(customWh)# update the card's surface
            if customWh == None:# if the card was resized, then the coords need to be updated again
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
    
class CdCard(ScrollCard):
    def __init__(self,image,name,sideScroll,data,wh) -> None:
        """Needs to be given the sideScroll object that will be used to draw the card"""
        super().__init__(name,sideScroll,data,wh)

        self.image = pygame.transform.scale(image,self.wh)
        self.image.set_alpha(80)         
    
    def updateSurf(self,wh=None):
        """Draws Everything onto the card's surface - Only needs to be called when data changes"""
        # pygame.draw.rect(self.surf,(60,60,60),pygame.Rect(0,0,self.wh[0],self.wh[1]))
        # self.surf.fill((60,60,60,120))
        if wh == None:
            wh = self.wh
        self.surf = pygame.Surface(wh).convert_alpha()
        
        self.surf.fill((0,0,0,0))
        gfxdraw.filled_polygon(self.surf,[(0,0),(wh[0],0),(wh[0],wh[1]),(0,wh[1])],(60,60,60,120))
        # self.surf.blit(self.image,(0+wh[0]//8,0))
        self.surf.blit(self.image,(0,0))    
        pygame.draw.rect(self.surf,(0,0,0),pygame.Rect(0,0,wh[0],wh[1]),5)

        self.surf.blit(s_render("CD",120,(0,0,0)),(0+10,0+10))

        drawCenterTxt(self.surf,f"{self.data['duration']} Months",55,(0,0,0),(0+wh[0]-15,0+30),centerX=False,centerY=False,fullX=True)

        drawCenterTxt(self.surf,f"{round(self.data['apr'],2)}%",130,(225,225,225),(0+wh[0]//2,0+wh[1]//2))

        x,y = 0+10,0+(wh[1]//4)*3-20
        info = [("Min Balance",f"${limit_digits(self.data['minBalance'],20,True)}"),("Risk",self.data['risk'])]
        # info = [("Name",self.name),("Min Balance",f"${limit_digits(self.data['minBalance'],20,True)}"),("Risk",self.data['risk'])]

        drawLinedInfo(self.surf,(x,y),(wh[0]-20,wh[1]//4+20),info,30,(0,0,0))

class LoanCard(ScrollCard):
    def __init__(self,name,sideScroll,data,wh) -> None:
        """Needs to be given the sideScroll object that will be used to draw the card"""
        super().__init__(name,sideScroll,data,wh)

        # self.image = pygame.transform.scale(image,self.wh)
        # self.image.set_alpha(80)  
        # self.data = {"term":int,"monthly payment":int|float,"principal":int|float,"remaining":int|float}
    
    def updateSurf(self,wh=None):
        """Draws Everything onto the card's surface - Only needs to be called when data changes"""
        # pygame.draw.rect(self.surf,(60,60,60),pygame.Rect(0,0,self.wh[0],self.wh[1]))
        # self.surf.fill((60,60,60,120))
        if wh == None:
            wh = self.wh
        self.surf = pygame.Surface(wh).convert_alpha()
        
        self.surf.fill((0,0,0,0))
        gfxdraw.filled_polygon(self.surf,[(0,0),(wh[0],0),(wh[0],wh[1]),(0,wh[1])],(60,60,60,120))

        pygame.draw.rect(self.surf,(0,0,0),pygame.Rect(0,0,wh[0],wh[1]),5)

        self.surf.blit(s_render(f"LOAN {self.sideScroll.cards.index(self)+1}",80,(0,0,0)),(0+10,0+10))

        drawCenterTxt(self.surf,f"{self.data['term']} Months",55,(0,0,0),(0+wh[0]-15,0+20),centerX=False,centerY=False,fullX=True)
        monthlyPayment = "$"+limit_digits(self.data['monthly payment'],20,self.data['monthly payment']>100)
        tSize = getTSizeNums(monthlyPayment,wh[0]-80,170)
        monthlyPayment = s_render(monthlyPayment,tSize,(225,225,225))
        drawCenterRendered(self.surf,monthlyPayment,(0+wh[0]//2,0+wh[1]//2+15))
        drawCenterTxt(self.surf,"Monthly Payment",50,(100,100,100),(0+wh[0]//2,0+wh[1]//2-monthlyPayment.get_height()//2+5),centerY=False,fullY=True)

        x,y = 0+10,0+(wh[1]//4)*3-20
        info = [("Principal (Og)",f"${limit_digits(self.data['principal'],20,True)}"),("Principal Left",f"${limit_digits(self.data['remaining'],20,True)}")]

        drawLinedInfo(self.surf,(x,y),(wh[0]-20,wh[1]//4+20),info,35,(0,0,0))

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
    def updateCards(self,data:list[dict]):
        """Args should be the arguments for whatever child class of ScrollCard.updateData Needs"""
        for i,card in enumerate(self.cards):
            card.updateData(data[i])

    def scrollControls(self,mousebuttons):
        if mousebuttons == 4:
            self.scroll += self.scrollSpeed
        elif mousebuttons == 5:
            self.scroll -= self.scrollSpeed
        self.scroll = max(0,min(self.scroll,self.cardWH[0]*(len(self.cards)-1)))
        
    def draw(self,screen,mousebuttons):
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(self.coords[0],self.coords[1],self.wh[0],self.wh[1]),5)
        self.scrollControls(mousebuttons)
        
        middle = self.coords[0]+self.wh[0]//2
        ypos = self.coords[1]+20
        index = self.getCard(index=True)
        offset = -(self.scroll%self.cardWH[0])
        #draw a rect for the selected card
        pygame.draw.rect(screen,(255,255,255),pygame.Rect(middle-self.cardWH[0]-5+offset+self.cardWH[0],ypos-5,self.cardWH[0]+10,self.cardWH[1]+10),5)
        minX,maxX = self.coords[0]+20,self.coords[0]+self.wh[0]-20
        self.cards[index].draw(screen,(middle+offset,ypos),mousebuttons,minX,maxX)
        for i,card in enumerate(self.cards):
            if i != index:
                if card.draw(screen,(middle+(i-index)*(self.cardWH[0]+25)+offset,ypos),mousebuttons,minX,maxX):
                    self.setCard(i)


        
        

# sideSroll = SideScroll((50,50),(1350,500),(450,450))
# bankIcons = {}
# for file in os.listdir(r"Assets\bankIcons"):
#     print(file)
#     image = pygame.image.load(r"Assets\bankIcons\{}".format(file)).convert_alpha()
#     name = file.split(".")[0]
#     bankIcons[name] = CdCard(image,name,sideSroll)

# sideSroll.loadCards(list(bankIcons.values()))

#     sideSroll.draw(screen,mousebuttons)



