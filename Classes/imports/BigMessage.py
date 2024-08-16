import pygame
import pygame.gfxdraw
from Defs import *
# s_render
class BigMessage:
    def __init__(self,txtsInputs:list[tuple],boxTxts:list[tuple],descriptionTxts:list[tuple]) -> None:
        """All the txts should be in this format : [(txt,size,color)]
        txtinputs should be len = 3, box and description txts should be of len = 2
        A subclass needs to be made, see OptionMessage for an example"""

        assert len(txtsInputs) == 3, "The txtsInputs must be a list of 3 tuples"
        assert len(boxTxts) == 2, "The boxTxts must be a list of 2 tuples"
        assert len(descriptionTxts) == 2, "The descriptionTxts must be a list of 2 tuples"
        assert all([isinstance(txt,str) and isinstance(size,int) and isinstance(color,tuple) for txt,size,color in txtsInputs]), "The txtsInputs must be a list of tuples with the format (txt,size,color)"
        
        self.coords = [100,100]
        self.wh = [700,500]
        self.txtInputs = txtsInputs
        self.boxTxts = boxTxts
        self.descriptionTxts = descriptionTxts
        self.renderedTxt = [s_render(*txtinput) for txtinput in txtsInputs]
        self.biggestWidth = max([txt.get_width() for txt in self.renderedTxt])+20
        self.totalHeight = sum([txt.get_height() for txt in self.renderedTxt])
        self.lastMousePos = None
        self.background = pygame.image.load(r"Assets\backgrounds\bigMessageBack.jpg").convert_alpha()
        # self.background = pygame.image.load(r"Assets\backgrounds\Background (9).png").convert_alpha()
        
        # self.background = pygame.transform.smoothscale_by(self.background,2)
        # gfxdraw.filled_polygon(self.background,[(0,0),(1920,0),(1920,1080),(0,1080)],(40,40,40,180))
        # gfxdraw.filled_polygon(self.background,[(0,0),(1920,0),(1920,1080),(0,1080)],(40,40,40,225))
        
    def getPoly(self):
        return [(self.coords[0],self.coords[1]),(self.wh[0]+self.coords[0],self.coords[1]),(self.wh[0]+self.coords[0],self.wh[1]+self.coords[1]),(self.coords[0],self.wh[1]+self.coords[1])]
    def draw(self,screen,uiControls,mousebuttons,*args):
        """Args are all the arguments that are passed to the result1 and result2 methods"""
        uiControls.bar.set_currentvalue(0)
        self.adjustCoords()
        gfxdraw.filled_polygon(screen,self.getPoly(),(40,40,40))
        # gfxdraw.textured_polygon(screen,self.getPoly(),self.background,0,0)
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(self.coords[0],self.coords[1],self.wh[0],self.wh[1]),5)

        # box around the txts at the top
        startX = self.coords[0]+self.wh[0]//2-self.biggestWidth//2
        startY = self.coords[1]+25
        endX = startX+self.biggestWidth
        endY = startY+self.totalHeight+30
        
        # pygame.draw.rect(screen,(40,40,40),pygame.Rect(startX-10,startY-10,endX-startX+20,endY-startY+20),border_radius=15)
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(startX-10,startY-10,endX-startX+20,endY-startY+20),5,15)


        middleX = self.coords[0]+self.wh[0]//2
        yOff = 25+self.coords[1]
        for i,txt in enumerate(self.renderedTxt):# draw the texts
            drawCenterRendered(screen,txt,(middleX,yOff),centerX=True,centerY=False)
            yOff += txt.get_height()+15
        w,h = int(self.wh[0]/2)*.9,75
        x1,y1 = 20+self.coords[0],self.coords[1]+self.wh[1]//2
        x2,y2 = self.coords[0]+self.wh[0]-w-20,self.coords[1]+self.wh[1]//2
        txt1,size1,color1 = self.boxTxts[0]
        
        result1 = drawClickableBoxWH(screen,(x1,y1),(w,h),txt1,size1,color1,(255,255,255),mousebuttons,fill=True)
        txt2,size2,color2 = self.boxTxts[1]
        if result1:
            self.result1(*args)

        result2 = drawClickableBoxWH(screen,(x2,y2),(w,h),txt2,size2,color2,(255,255,255),mousebuttons,fill=True)
        if result2:
            self.result2(*args)

        for i,(txt,size,color) in enumerate(self.descriptionTxts):
            lines = 1 if len(txt) < 20 else 2
            txt = separate_strings(txt,lines)
            yOff = [y1,y2][i]+h+10
            x = [x1,x2][i]+w//2
            for j,line in enumerate(txt):
                drawCenterRendered(screen,s_render(line,size,color),(x,yOff),centerY=False)
                yOff += size+5

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

    def result1(self,*args):
        raise NotImplementedError("The result1 method must be implemented")
    def result2(self,*args):
        raise NotImplementedError("The result2 method must be implemented")
    
class OptionMessage(BigMessage):
    """the inputs for result1 and result2 are the same since they just pass the args"""
    def __init__(self,optionObj) -> None:
        txts = [("Option Has Expired",80,(200,200,200)),("DRON Call x 12,115",60,(0,102,204)),("Est Value : $1,215,000",60,(180,180,180))]
        boxTxts = [("Sell To Market",60,(0,0,0)),("Exercise",60,(0,0,0))]
        descriptionTxts = [(f"Sell for 2% loss",45,(200,200,200)),("Exercise the option",45,(200,200,200))]
        super().__init__(txts,boxTxts,descriptionTxts)
        self.optionObj = optionObj
    def result1(self,player):
        """Sell the option"""
        option = [o for o in player.options if not o.optionLive()][0]	
        player.sellAsset(option,option.getQuantity(),0.98)# sell the option for a 2% loss
        print("Result 1")
        bigMessageList.remove(self)

    def result2(self,player):
        """Ëxercise the option"""
        option = [o for o in player.options if not o.optionLive()][0]
        
        if option.optionType == 'Call':
            print("it is a call",option.getStrike()*option.getQuantity()*100,player.cash)
            if player.cash > option.getStrike()*option.getQuantity()*100:
                print('bought the asset')
                newAsset = option.getExerciseStock()
                player.buyAsset(newAsset,option.getStrike())
                player.options.remove(option)
        elif option.optionType == 'Put':
            print("it is a put")
            # player.buyStock(option.stockObj,option.getQuantity())
        print("Result 2")
        bigMessageList.remove(self)



# # EXAMPLE USAGE
# # errors = ErrorMessageHandler()
# background = pygame.image.load(r"Assets\backgrounds\Background (9).png").convert_alpha()
# background = pygame.transform.smoothscale_by(background,2);background.set_alpha(100)
# txts = [("Option Has Expired",80,(200,200,200)),("DRON Call x 12,115",60,(0,102,204)),("Est Value : $1,215,000",60,(180,180,180))]
# boxTxts = [("Sell To Market",60,(0,0,0)),("Exercise",60,(0,0,0))]
# descriptionTxts = [(f"Sell for 2% loss",45,(200,200,200)),("Exercise the option",45,(200,200,200))]
# bigMess  = BigMessage(txts,boxTxts,descriptionTxts)
# lastfps = deque(maxlen=300)
# clock = pygame.time.Clock()
# while True:
#     screen.fill((60,60,60))
#     # pygame.event.pump()
#     # pygame.draw.circle(screen, (255,255,255), (450,450), 100)

#     # errors.update(screen)
#     screen.blit(background,(0,0))
#     bigMess.draw(screen,None,0)
#     screen.blits((text,pos) for text,pos in zip(update_fps(clock,lastfps),[(850,0),(850,30),(850,60)]))
#     pygame.display.flip()

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
#             pygame.quit()
#             quit()
#         # elif event.type == pygame.MOUSEBUTTONDOWN:
#         #     print("Mouse button pressed",pygame.mouse.get_pos())
#         #     errors.addMessage(f"Pressed the Mouse at {pygame.mouse.get_pos()}",(450,450))
#         # elif event.type == pygame.KEYDOWN and event.key == pygame.K_j:
#         #     errors.addMessage(f"Already Max Quantity")
#         # elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
#         #     errors.addMessage(f"Select A stock")

#     clock.tick(60)





