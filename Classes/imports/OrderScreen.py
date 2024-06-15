import pygame
from pygame import gfxdraw
import pygame.gfxdraw
from Defs import *
from Classes.imports.Numpad import Numpad
from Classes.UI_controls import UI_Controls

class OrderScreen:
    """This class will be used in stockbook and porfolio to buy or sell stocks"""
    def __init__(self,uicontrols) -> None:
        self.orderTypes = ['Market','Limit','Stop']
        self.orderType = 'Market'
        self.transactionTypes = ['Buy','Sell']
        self.transactionType = 'Buy'
        background = pygame.image.load(r'Assets\backgrounds\Background (9).png').convert_alpha()
        background = pygame.transform.smoothscale_by(background,2);background.set_alpha(140)
        self.background = background
        self.wh = [960,650]

        self.surf = pygame.Surface((self.wh[0],self.wh[1]))
        self.surf.blit(background,(-self.wh[0],-self.wh[1]))
        self.surfCoords = [0,0]
        self.lastMousePos = [0,0]
        self.numPad = Numpad(displayText=False)
        self.uicontrols : UI_Controls = uicontrols
    
    def draw(self,screen,stockObj,mousebuttons:int,player):
        self.uicontrols.bar.changeMaxValue(5)
        
        mousex,mousey = pygame.mouse.get_pos()
        x,y = self.surfCoords   
        points = [(480+x,270+y),(480+self.wh[0]+x,270+y),(480+self.wh[0]+x,270+self.wh[1]+y),(480+x,270+self.wh[1]+y)]  
        collide = pygame.Rect.collidepoint(pygame.Rect(460+x,250+y,self.wh[0]+40,self.wh[1]+40),mousex,mousey)

        if collide and pygame.mouse.get_pressed()[0]:
            xdiff,ydiff = mousex-self.lastMousePos[0],mousey-self.lastMousePos[1]
            if xdiff != 0 or ydiff != 0:
                self.surfCoords[0] += xdiff
                self.surfCoords[1] += ydiff
                self.surf.fill((0,0,0))
                self.surf.blit(self.background,(-self.surfCoords[0]-480,-self.surfCoords[1]-270))
                
                
        self.lastMousePos = [mousex,mousey]
        
        # gfxdraw.filled_polygon(screen,points,(50,50,50))
        screen.blit(self.surf,(480+x,270+y))    
        pygame.draw.polygon(screen,(0,0,0),points,10)
        # --------------Title that says what type of order it is--------------
        title = s_render(f'{self.orderType.upper()} Order',60,(255,255,255))
        screen.blit(title,(960-title.get_width()/2+x,280+y))
        stockName = s_render(f'{stockObj.name}',40,(stockObj.color))
        screen.blit(stockName,(1420-stockName.get_width()/2+x,280+y))

        # --------------draw the order type and transaction type--------------
        orderTypeText = s_render('Order Type',40,(255,255,255))
        screen.blit((orderTypeText),(500+x,310+y))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(490+x, 310+orderTypeText.get_height()+y, orderTypeText.get_width()+30, 5))

        result = checkboxOptions(screen,self.orderTypes,self.orderType,600,35,(500+x,y+320+orderTypeText.get_height()),mousebuttons)# draws the checkbox for the order type
        self.orderType = self.orderType if result == None else result[0]

        transactionTypeText = s_render('Transaction Type',40,(255,255,255))
        screen.blit((transactionTypeText),(500+x,390+y))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(490+x, 390+transactionTypeText.get_height()+y, transactionTypeText.get_width()+30, 5))

        result = checkboxOptions(screen,self.transactionTypes,self.transactionType,450,35,(500+x,430+y),mousebuttons)# draws the checkbox for the sell vs buy
        self.transactionType = self.transactionType if result == None else result[0]

        # --------------Drawing the Shares, price Per, and cost text-------------- 

        screen.blit(s_render('Shares',40,(255,255,255)),(500+x,510+y))
        sharesNum = s_render(self.numPad.getNumstr('SHARE'),40,(255,255,255))
        screen.blit((sharesNum),(950-sharesNum.get_width()+x,510+y))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(490+x, 515+sharesNum.get_height()+y, 900, 5))
        perPrice = s_render('Price Per',40,(255,255,255))
        screen.blit(perPrice,(500+x,555+y))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(490+x, 560+perPrice.get_height()+y, 900, 5))
        screen.blit(s_render('Cost',40,(255,255,255)),(500+x,600+y))

        self.numPad.draw(screen,(500+x,675+y),(325,250),"SHARE",mousebuttons,int(player.cash/stockObj.price))




