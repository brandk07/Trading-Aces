import pygame
import pygame.gfxdraw
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Defs import *

pygame.init()
screen = pygame.display.set_mode([1800,980])
pygame.display.set_caption("Pygame Shell")

# class ErrorMessage:
#     def __init__(self,coords:list,text:str,txtSize:int,txtColor:tuple,backColor:tuple,s_render) -> None:
#         self.coords = list(coords)
#         self.text = text
#         self.txtSize = txtSize
#         self.txtColor = txtColor
#         self.backColor = backColor
#         self.s_render = s_render
#         self.surf = self.createSurface()
#         self.life = 240
        

#     def createSurface(self):
#         renderedTxt : pygame.Surface = self.s_render(self.text, self.txtSize, self.txtColor)
#         self.coords[1] -= renderedTxt.get_height()+15
#         self.coords[0] -= renderedTxt.get_width()//2
#         surf = pygame.Surface((renderedTxt.get_width()+40,renderedTxt.get_height()+20))

#         pygame.draw.rect(surf,self.backColor,pygame.Rect(0,0,surf.get_width(),surf.get_height()),border_radius=15)
#         pygame.draw.rect(surf,(1,1,1),pygame.Rect(0,0,surf.get_width(),surf.get_height()),5,15)

#         surf.blit(renderedTxt,(20,10))
#         surf.set_colorkey((0,0,0))
#         return surf.convert_alpha()
    
#     def draw(self,screen:pygame.Surface):
#         # pygame.draw.rect(screen,(255,255,255),pygame.Rect(10,10,50,50))
#         if self.life > 0:
#             self.surf.set_alpha(min(255,self.life*1.5))
#             screen.blit(self.surf,self.coords)
#             self.coords[1] -= 0.75
#             self.life -= 1
#             return True
#         return False
        
        

# class ErrorMessageHandler:
#     def __init__(self,s_render) -> None:
#         self.messageList : list[ErrorMessage] = [] 
#         self.sRender = s_render
#         self.framesAgoAdd = 0

#     def addMessage(self,txt:str,txtColor=(190,190,190),backColor=(160,10,10),txtSize=35,coords:list=None):
#         """If coords aren't given, the message will be displayed at the mouse position"""
#         if self.framesAgoAdd == 0:
#             coords = pygame.mouse.get_pos() if coords == None else coords
#             self.messageList.append(ErrorMessage(coords,txt,txtSize,txtColor,backColor,self.sRender))
#             self.framesAgoAdd = 30

    
#     def update(self,screen):
#         if self.framesAgoAdd > 0:
#             self.framesAgoAdd -= 1
#         for i in range(len(self.messageList)-1,0,-1):
#             message = self.messageList[i]
#             if not message.draw(screen):# draws the message and checks if the message has life left
#                 self.messageList.pop(i)
class BigMessage:
    def __init__(self,txtsInputs:list[tuple],boxTxts:list[tuple],descriptionTxts:list[tuple]) -> None:
        """All the txts should be in this format : [(txt,size,color)]
        txtinputs should be len = 3, box and description txts should be of len = 2"""

        assert len(txtsInputs) == 3, "The txtsInputs must be a list of 3 tuples"
        assert len(boxTxts) == 2, "The boxTxts must be a list of 2 tuples"
        assert len(descriptionTxts) == 2, "The descriptionTxts must be a list of 2 tuples"
        assert all([isinstance(txt,str) and isinstance(size,int) and isinstance(color,tuple) for txt,size,color in txtsInputs]), "The txtsInputs must be a list of tuples with the format (txt,size,color)"
        
        self.coords = [100,100]
        self.wh = [700,500]
        self.txtInputs = txtsInputs
        self.boxTxts = boxTxts
        self.descriptionTxts = descriptionTxts
        self.renderedTxt = [s_render(txtinput) for txtinput in txtsInputs]
        self.lastMousePos = None
        # self.background = pygame.image.load(r"Assets\backgrounds\bigMessageBack.jpg").convert_alpha()
        self.background = pygame.image.load(r"Assets\backgrounds\Background (9).png").convert_alpha()
        self.background = pygame.transform.smoothscale_by(self.background,2);self.background.set_alpha(100)
        # gfxdraw.filled_polygon(self.background,[(0,0),(1920,0),(1920,1080),(0,1080)],(40,40,40,180))
        gfxdraw.filled_polygon(self.background,[(0,0),(1920,0),(1920,1080),(0,1080)],(0,0,0))
        
    def getPoly(self):
        return [(self.coords[0],self.coords[1]),(self.wh[0]+self.coords[0],self.coords[1]),(self.wh[0]+self.coords[0],self.wh[1]+self.coords[1]),(self.coords[0],self.wh[1]+self.coords[1])]
    def draw(self,screen,uiControls,mousebuttons):
        # uiControls.bar.set_currentvalue(0)
        self.adjustCoords()

        # pygame.draw.rect(screen,(45,45,45),pygame.Rect(self.coords[0],self.coords[1],self.wh[0],self.wh[1]),border_radius=15)
        
        gfxdraw.textured_polygon(screen,self.getPoly(),self.background,0,0)
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(self.coords[0],self.coords[1],self.wh[0],self.wh[1]),5,border_radius=15)
       
        middleX = self.coords[0]+self.wh[0]//2
        yOff = 25+self.coords[1]
        for i,txt in enumerate(self.renderedTxt):# draw the texts
            drawCenterRendered(screen,txt,(middleX,yOff),centerX=True,centerY=False)
            yOff += txt.get_height()+15
        w,h = int(w/3),75
        x1,y1 = 20+self.coords[0],self.coords[1]+self.wh[1]//2
        x2,y2 = self.coords[0]+self.wh[0]-w-20,self.coords[1]+self.wh[1]//2
        txt1,size1,color1 = self.boxTxts[0]
        result1 = drawClickableBoxWH(screen,(x1,y1),(w,h),txt1,size1,color1,(255,255,255),mousebuttons)
        
    
    def adjustCoords(self):
        mousex,mousey = pygame.mouse.get_pos()
        x,y = self.coords   
        wh = self.wh

        # points = [(x,y),(wh[0]+x,y),(wh[0]+x,wh[1]+y),(x,wh[1]+y)]  
        collide = pygame.Rect.collidepoint(pygame.Rect(x-20,y-20,wh[0]+40,wh[1]+40),mousex,mousey)

        if collide and pygame.mouse.get_pressed()[0]:
            if self.lastMousePos != None:# if there is a last mouse pos
                xdiff,ydiff = mousex-self.lastMousePos[0],mousey-self.lastMousePos[1]
                if xdiff != 0 or ydiff != 0:
                    self.coords[0] += xdiff
                    self.coords[1] += ydiff

            else:# if there isn't a last mouse pos
                self.lastMousePos = [mousex,mousey]
                
                
        self.lastMousePos = [mousex,mousey]



# EXAMPLE USAGE
# errors = ErrorMessageHandler()
background = pygame.image.load(r"Assets\backgrounds\Background (9).png").convert_alpha()
background = pygame.transform.smoothscale_by(background,2);background.set_alpha(100)
txts = [("Option Has Expired",80,(200,200,200)),("DRON Call x 12,115",60,(0,102,204)),("Est Value : $1,215,000",60,(0,0,0))]
boxTxts = [("Sell To Market",60,(0,0,0)),("Execute",60,(0,0,0))]
descriptionTxts = [(f"Sell Immediately 98% of value",60,(0,0,0)),("Execute the option",60,(0,0,0))]
bigMess  = BigMessage(txts)
lastfps = deque(maxlen=300)
clock = pygame.time.Clock()
while True:
    screen.fill((60,60,60))
    # pygame.event.pump()
    # pygame.draw.circle(screen, (255,255,255), (450,450), 100)

    # errors.update(screen)
    screen.blit(background,(0,0))
    bigMess.draw(screen,None)
    screen.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(850,0),(850,30),(850,60)]))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     print("Mouse button pressed",pygame.mouse.get_pos())
        #     errors.addMessage(f"Pressed the Mouse at {pygame.mouse.get_pos()}",(450,450))
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
        #     errors.addMessage(f"Already Max Quantity")
        # elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
        #     errors.addMessage(f"Select A stock")

    clock.tick(60)





