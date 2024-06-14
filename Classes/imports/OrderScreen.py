import pygame
from pygame import gfxdraw
import pygame.gfxdraw
from Defs import *
from Classes.imports.Numpad import Numpad

class OrderScreen:
    """This class will be used in stockbook and porfolio to buy or sell stocks"""
    def __init__(self) -> None:
        self.orderTypes = ['Market','Limit','Stop']
        self.orderType = 'Market'
        self.transactionTypes = ['Buy','Sell']
        self.transactionType = 'Buy'
        self.numPad = Numpad()
    
    def draw(self,screen,stockObj,mousebuttons:int):
        points = [(480,270),(1440,270),(1440,810),(480,810)]
        pygame.draw.polygon(screen,(0,0,0),points,5)
        gfxdraw.filled_polygon(screen,points,(50,50,50))
        # --------------Title that says what type of order it is--------------
        title = s_render(f'{self.orderType} Order',60,(255,255,255))
        screen.blit(title,(960-title.get_width()/2,280))
        stockName = s_render(f'{stockObj.name}',40,(stockObj.color))
        screen.blit(stockName,(1420-stockName.get_width()/2,280))

        # --------------draw the order type and transaction type--------------
        orderTypeText = s_render('Order Type:',40,(255,255,255))
        screen.blit((orderTypeText),(500,310))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(490, 310, orderTypeText.get_width()+30, 10))

        result = checkboxOptions(screen,self.orderTypes,self.orderType,600,35,(500,340),mousebuttons)
        self.orderType = self.orderType if result == None else result[0]

        transactionTypeText = s_render('Transaction Type:',40,(255,255,255))
        screen.blit((transactionTypeText),(500,380))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(490, 360, transactionTypeText.get_width()+30, 10))

        result = checkboxOptions(screen,self.transactionTypes,self.transactionType,600,35,(500,410),mousebuttons)
        self.transactionType = self.transactionType if result == None else result[0]

        # --------------Drawing the Shares, price Per, and cost text-------------- 

        screen.blit(s_render('Shares:',40,(255,255,255)),(500,450))
        sharesNum = s_render(f'{self.numPad.getNumstr('Share')}',40,(255,255,255))
        screen.blit((sharesNum),(950-sharesNum.get_width(),490))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(490, 450, 900, 10))
        screen.blit(s_render('Price Per:',40,(255,255,255)),(500,490))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(490, 490, 900, 10))
        screen.blit(s_render('Cost:',40,(255,255,255)),(500,530))




