import pygame
from Defs import *
from Classes.imports.Gametime import getTimeStrs

# pygame.init()
# screen = pygame.display.set_mode([1850,1000])
# pygame.display.set_caption("Pygame Shell")

class ScrollCard:
    def __init__(self,name,sideScroll,data) -> None:
        self.wh = sideScroll.cardWH
        self.name :str = name
        self.sideScroll : SideScroll = sideScroll
        self.surf = pygame.Surface(self.wh).convert_alpha()

        self.data = data
        self.needToUpdate = True# if the card surf needs to be updated

    def getData(self) -> dict:
        return self.data
    
    def updateData(self,data:dict):
        if self.data != data:
            self.needToUpdate = True
            self.data = data
        
    @lru_cache(maxsize=3)
    def getPartialSurf(self,cutOff,direction):
        """Returns a surface that has cutOff pixels cut off from the direction"""
        if direction == "left":
            return self.surf.subsurface(pygame.Rect(cutOff,0,self.wh[0]-cutOff,self.wh[1]))
        elif direction == "right":
            return self.surf.subsurface(pygame.Rect(0,0,self.wh[0]-cutOff,self.wh[1]))
        elif direction == "top":
            return self.surf.subsurface(pygame.Rect(0,cutOff,self.wh[0],self.wh[1]-cutOff))
        elif direction == "bottom":
            return self.surf.subsurface(pygame.Rect(0,0,self.wh[0],self.wh[1]-cutOff))

    def draw(self,screen,coords,mousebuttons,minX=None,maxX=None,minY=None,maxY=None,customWh=None) -> bool:
        """Draws the card onto the screen at the given coords"""
        if minX == None and maxX == None:
            minX,maxX = 0,screen.get_width()
        if minY == None and maxY == None:
            minY,maxY = 0,screen.get_height()
        if customWh != None:# if the card was resized, then the card needs to be updated (temporarily)
            self.needToUpdate = True

        coords = list(coords)
        if coords[0]+self.wh[0] < minX+20 or coords[0] > maxX:
            return False
        if coords[1]+self.wh[1] < minY+20 or coords[1] > maxY:
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
        if coords[1] < minY and coords[1]+self.wh[1] > minY:
            newSurf = self.getPartialSurf(minY-coords[1],"top")
            coords[1] += (minY-coords[1])
        elif coords[1]+self.wh[1] > maxY:
            newSurf = self.getPartialSurf(coords[1]+self.wh[1]-maxY,"bottom")

        screen.blit(newSurf,coords)
        
        if pygame.Rect(coords[0],coords[1],self.wh[0],self.wh[1]).collidepoint(pygame.mouse.get_pos()):
            if mousebuttons == 1:
                soundEffects['generalClick'].play()
                return True
        return False
    
class CdCard(ScrollCard):
    def __init__(self,image,name,sideScroll,data) -> None:
        """Needs to be given the sideScroll object that will be used to draw the card"""
        super().__init__(name,sideScroll,data)

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

        drawCenterTxt(self.surf,f"{self.data['duration']} Month{'s' if self.data['duration'] > 0 else ''}",55,(0,0,0),(0+wh[0]-15,0+30),centerX=False,centerY=False,fullX=True)

        drawCenterTxt(self.surf,f"{round(self.data['apr'],2)}%",130,(225,225,225),(0+wh[0]//2,0+wh[1]//2))

        x,y = 0+10,0+(wh[1]//4)*3-20
        info = [("Min Balance",f"${limit_digits(self.data['minBalance'],20,True)}"),("Risk",self.data['risk'])]
        # info = [("Name",self.name),("Min Balance",f"${limit_digits(self.data['minBalance'],20,True)}"),("Risk",self.data['risk'])]

        drawLinedInfo(self.surf,(x,y),(wh[0]-20,wh[1]//4+20),info,30,(0,0,0))

class LoanCard(ScrollCard):
    def __init__(self,name,sideScroll,data) -> None:
        """Needs to be given the sideScroll object that will be used to draw the card"""
        super().__init__(name,sideScroll,data)

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
        
class RunCard(ScrollCard):
    def __init__(self,sideScroll,runObj) -> None:
        """Needs to be given the sideScroll object that will be used to draw the card"""
        self.runObj = runObj
        data = self.dataConfig(runObj)
        super().__init__(data['name'],sideScroll,data)

        # self.image = pygame.transform.scale(image,self.wh)
        # self.image.set_alpha(80)  
        # self.data = {"term":int,"monthly payment":int|float,"principal":int|float,"remaining":int|float}
    def dataConfig(self,runObj):
        image = runObj.runIcon
        image = pygame.transform.scale(image,(175,175))

        networthTxt = f"${limit_digits(runObj.getNetworth(),30,runObj.getNetworth()>1000)}"

        return {"placement":runObj.getRankStr(),"name":runObj.name,"networth":networthTxt,"startTime":runObj.startTime,"runIcon":image}

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

        # self.surf.blit(self.data['runIcon'],(5,5))# screenShot (175,175)
        drawBoxedImage(self.surf,(10,10),self.data['runIcon'],(175,175),15,5)

        drawCenterTxt(self.surf,self.data['placement'],50,(180,180,180),(190+(wh[0]-190)//2,10),centerY=False)


        size = getTSizeNums(self.data['networth'],wh[0]-40,135)
        # color = ((5-self.runObj.getStarRating())*35,self.runObj.getStarRating()*35,0)
        drawCenterTxt(self.surf,self.data['networth'],size,(0,180,0),(wh[0]//2,220),centerY=False)

        numLines = min(4,len(self.data['name'].split(' ')),math.ceil(len(self.data['name'])/9))
        lines = separate_strings(self.data['name'],numLines)
        for i,line in enumerate(lines):
            x = 190+(wh[0]-190)//2
            size = getTSizeNums(line,wh[0]-200,45)
            drawCenterTxt(self.surf,line,size,(200,200,200),(x,65+35*i),centerY=False)


        timeStrs = getTimeStrs(self.runObj.startTime)
        dateStr = f"{timeStrs['dayname']}, {timeStrs['monthname']} {timeStrs['day']}, {timeStrs['year']}"
        size = getTSizeNums(dateStr,wh[0]-20,35)
        drawCenterTxt(self.surf,dateStr,size,(180,180,180),(wh[0]//2,wh[1]-35),centerY=False)

class StartRunCard(ScrollCard):
    def __init__(self,sideScroll,runObj) -> None:
        """Needs to be given the sideScroll object that will be used to draw the card"""
        self.runObj = runObj
        data = self.dataConfig(runObj)
        super().__init__(data['name'],sideScroll,data)
        # self.image = pygame.transform.scale(image,self.wh)
        # self.image.set_alpha(80)  
        # self.data = {"term":int,"monthly payment":int|float,"principal":int|float,"remaining":int|float}
    def dataConfig(self,runObj):
        image = runObj.runIcon
        image = pygame.transform.scale(image,(230,230))
        networthTxt = f"${limit_digits(runObj.getNetworth(),30,runObj.getNetworth()>1000)}"

        return {"name":runObj.name,"networth":networthTxt,"startTime":runObj.startTime,"runIcon":image,"mode":runObj.gameMode,"placement":runObj.getRankStr()}

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

        drawBoxedImage(self.surf,(10,10),self.data['runIcon'],(230,230),15,5)

        drawCenterTxt(self.surf,self.data['name'],50,(180,180,180),(60+(wh[0])//2,10),centerY=False)


        size = getTSizeNums(self.data['networth'],wh[0]//2,135)
        drawCenterTxt(self.surf,self.data['networth'],size,(205,205,205),(270,80),centerX=False,centerY=False)

        color = self.gameModes = [(19, 133, 100), (199, 114, 44), (196, 22, 62)][['Career','Blitz','Goal'].index(self.data['mode'])]

        drawCenterTxt(self.surf,self.data['mode'],70,color,(255,10),centerX=False,centerY=False)
        drawCenterTxt(self.surf,self.data['placement'],70,(180,180,180),(wh[0]-20,10),centerX=False,centerY=False,fullX=True)


        timeStrs = getTimeStrs(self.runObj.startTime)
        dateStr = f"Started On {timeStrs['dayname']}, {timeStrs['monthname']} {timeStrs['day']}, {timeStrs['year']}"
        size = getTSizeNums(dateStr,wh[0]-20,35)
        drawCenterTxt(self.surf,dateStr,size,(180,180,180),(wh[0]//2,wh[1]-35),centerY=False)



class CreateMenuRunImage(ScrollCard):
    def __init__(self,sideScroll,image) -> None:
        """Needs to be given the sideScroll object that will be used to draw the card"""
        self.image = image

        super().__init__("image",sideScroll,image)


    def updateSurf(self,wh=None):
        """Draws Everything onto the card's surface - Only needs to be called when data changes"""
        if wh == None:
            wh = self.wh

        self.surf = pygame.Surface(wh).convert_alpha()
        
        self.surf.fill((0,0,0,0))

        self.surf.blit(self.image,(0,0))
        

class SideScroll:
    def __init__(self,coords,wh,cardWH) -> None:
        self.cards : list[ScrollCard] = []# list of cards
        if type(self.cards) != list:
            raise ValueError("self.cards must be a list")
        self.coords = coords
        self.cardWH = cardWH
        self.wh = wh
        self.scroll = 600
        self.mouseScrollTime = 0
        self.lastSelected = None
        self.scrollSpeed = 35
    def getCard(self,index=False):
        """Returns the card that is currently in the center of the screen
        If index is True, it will return the index of the card"""
        # newSelected = self.scroll//self.cardWH[0]
        # if self.lastSelected != newSelected:
        #     self.scroll = newSelected*self.cardWH[0]+self.cardWH[0]//2

        if self.lastSelected == None or self.lastSelected >= len(self.cards):
            self.lastSelected = None
            return None
        
        # self.lastSelected = self.scroll//self.cardWH[0]
        if index:
            return self.lastSelected
        return self.cards[self.lastSelected]
    def setCard(self,index=None,obj=None):
        """Sets the card that is currently in the center of the screen"""
        if index == None and obj == None:
            raise ValueError("Either index or obj must be given")
        if index != None:
            self.lastSelected = index
        else:
            self.lastSelected = self.cards.index(obj)
        # self.scroll = index*self.cardWH[0]+self.cardWH[0]//2
    def addCard(self,card:ScrollCard):
        """Adds a card to the list of cards"""
        self.cards.append(card)
    def loadCards(self,cards:list[ScrollCard]):
        """Needs to be called before the draw method"""
        if type(self.cards) != list:
            raise ValueError("self.cards must be a list")
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

        maxVal = (-self.cardWH[0]*(len(self.cards)-1))+175
        minVal = max(self.wh[0]-205,self.cardWH[0]*(len(self.cards)-1)-145)

        self.scroll = max(maxVal,min(self.scroll,minVal))
        
    def draw(self,screen,mousebuttons):
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(self.coords[0],self.coords[1],self.wh[0],self.wh[1]),5)

        if not self.cards:# if there are no cards, then there is nothing to do
            return
        
        self.scrollControls(mousebuttons)
        
        # middle = self.coords[0]+self.wh[0]//2
        ypos = self.coords[1]+20
        # offset = -(self.scroll%self.cardWH[0])
 
        index = self.getCard(True)
        
        minX,maxX = self.coords[0]+20,self.coords[0]+self.wh[0]-20



        for i,card in enumerate(self.cards):
            xcoord = self.scroll+(i*(self.cardWH[0]+25))
            if index == i:
                x,w = xcoord-5,self.cardWH[0]+10
                if x+w < self.coords[0] or x > self.coords[0]+self.wh[0]:# if the card is not in the screen, then continue
                    continue 
                if x < self.coords[0]:
                    w = self.cardWH[0]+10+x-self.coords[0]
                    x = self.coords[0]+10
                elif x+w > self.wh[0]+self.coords[0]:
                    w = self.wh[0]+self.coords[0]-x-10
                
                
                pygame.draw.rect(screen,(255,255,255),pygame.Rect(x,ypos-5,w,self.cardWH[1]+10),5)
            if card.draw(screen,(xcoord,ypos),mousebuttons,minX,maxX):# if the card is clicked
                if self.lastSelected != i:# if the card is not already selected
                    self.setCard(i)
                else:# if the card is already selected - deselect it
                    self.lastSelected = None

class VerticalScroll(SideScroll):
    def __init__(self, coords, wh, cardWH=(170,170)):
        super().__init__(coords, wh, cardWH)
        self.scroll = 25
        
    def draw(self, screen, mousebuttons):
        """Draws the cards vertically instead of horizontally"""
        minY, maxY = self.coords[1]+20, self.coords[1]+self.wh[1]-20
        
        # Handle scrolling
        if mousebuttons == 4:  # Scroll up
            self.scroll = min(25, self.scroll + 50)
        elif mousebuttons == 5:  # Scroll down
            maxScroll = -(len(self.cards) * (self.cardWH[1] + 25) - self.wh[1])
            self.scroll = max(maxScroll, self.scroll - 50)
        xpos = self.coords[0] + (self.wh[0]//2) - (self.cardWH[0] // 2) 
        index = self.lastSelected
        
        # Draw cards
        for i, card in enumerate(self.cards):
            ycoord = self.coords[1] + self.scroll + (i * (self.cardWH[1] + 25))
            
            # Draw selection box
            if index == i:
                y, h = ycoord-5, self.cardWH[1]+10
                if y+h < self.coords[1] or y > self.coords[1]+self.wh[1]:
                    continue
                if y < self.coords[1]:
                    h = self.cardWH[1]+10+y-self.coords[1]
                    y = self.coords[1]+10
                elif y+h > self.wh[1]+self.coords[1]:
                    h = self.wh[1]+self.coords[1]-y-10
                    
                pygame.draw.rect(screen, (255,255,255), 
                               pygame.Rect(xpos-5, y, self.cardWH[0]+10, h), 5)
            # Draw card and handle click
            if card.draw(screen, (xpos, ycoord), mousebuttons,minY=minY, maxY=maxY):
                if self.lastSelected != i:
                    self.setCard(i)
                else:
                    self.lastSelected = None
                    
        return self.getCard()