import pygame
from Defs import fontlist,point_in_polygon
from pygame import gfxdraw
from Classes.imports.Menu import Menu
import numpy as np

class Stockbook(Menu):
    def __init__(self,stocknames:list) -> None:
        super().__init__(r'Assets\stockbook\book.png',(30,165))
        self.quantity = 0
        self.stocktext = {name:[] for name in stocknames}
        self.selectedstock = 0
        self.menudrawn = False
        with open(r'Assets\stockdescriptions.txt','r') as descriptions:

            filecontents = descriptions.readlines()
            for i,line in enumerate(filecontents):
                for stockname in stocknames:
                    if line.replace('\n','') == stockname:
                        for x in range(1,5):
                            self.stocktext[stockname].append(filecontents[i+x].replace('\n',''))

        self.renderedstocknames = {name:fontlist[90].render(name,(150,150,150))[0] for name in stocknames}
        for key,lines in self.stocktext.items():#rendering the text that displays info about the stocks
            for i,line in enumerate(lines):
                if i == 0:#if its the first line, render it with a larger font and grey color
                    self.stocktext[key][i] = fontlist[40].render(line,(120, 120, 120))[0]
                else:#else render it with a smaller font and orange color
                    self.stocktext[key][i] = fontlist[30].render(line,(225, 90, 15))[0]
        
    def draw_menu_content(self,screen:pygame.Surface,stocklist:list,Mousebuttons:int,player):
        """Draws all the main content for the stockbook menu (the stocks on the left side of the screen)"""
        mousex,mousey = pygame.mouse.get_pos()
        for i,stock in enumerate(stocklist):
            if pygame.Rect.collidepoint(pygame.Rect(215+(i*8),120+(i*65),175,35),mousex,mousey) and Mousebuttons == 1:#if the mouse is hovering over the stock
                self.selectedstock = i
                self.quantity = 0
            if stock.price > stock.graphrangelists[stock.graphrange][0]:# if the price is greater than the first point in the current graph
                color = (0,120,0) if self.selectedstock == i else (0,80,0)
            else:
                color = (120,0,0) if self.selectedstock == i else (80,0,0)
            # the polygons and text for each of the stocks with the names and prices on the left side of the screen
            gfxdraw.filled_polygon(screen,((215+(i*8),120+(i*65)),(225+(i*8),155+(i*65)),(400+(i*8),155+(i*65)),(390+(i*8),120+(i*65))),color)
            screen.blit(fontlist[36].render(f'{stock.name} ${round(stock.price,2)}',(255,255,255))[0],(225+(i*8),125+(i*65)))
            if self.selectedstock == i:
                pygame.draw.polygon(screen, (0,0,0), ((215+(i*8),120+(i*65)),(225+(i*8),155+(i*65)),(400+(i*8),155+(i*65)),(390+(i*8),120+(i*65))),5)
                self.selected_stock(screen,stocklist,player,Mousebuttons)

    def draw_descriptions(self,screen:pygame.Surface,stocklist:list,player,Mousebuttons):
        """Draws the stock descriptions and the stock graph for the selected stock"""
        gfxdraw.filled_polygon(screen,((290,700),(320,955),(1570,955),(1535,700)),(60,60,60))

        screen.blit(fontlist[90].render(f'{stocklist[self.selectedstock].name}',(255,255,255))[0],(300,710))
        screen.blit(self.renderedstocknames[stocklist[self.selectedstock].name],(300,710))

        # stocklist[self.selectedstock].update(screen,play_pause,player,(1100,130),(500,680),drawn=True)
        stocklist[self.selectedstock].draw(screen,player,(1100,130),(500,680),stocklist,Mousebuttons)
        for i,line in enumerate(self.stocktext[stocklist[self.selectedstock].name]):
            x,y = (305+((i-1)*8) if i != 0 else self.renderedstocknames[stocklist[self.selectedstock].name].get_width()+310),(800+((i-1)*40) if i != 0 else 725)
            screen.blit(line,(x,y))

    def quantitycontrols(self,screen,Mousebuttons:int,player,stocklist:list):
        """This function is called for the buy and sell controls in the stockbook menu"""
        mousex,mousey = pygame.mouse.get_pos()
        # quantity controls
        maxpurchase = int(player.cash/stocklist[self.selectedstock].price)
        # quantitytext = fontlist[40].render(f'Quanity : {self.quantity}',(255,255,255))[0]
        tempquantity = self.quantity
        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1120,155,334,10))# line with circle on it for the quantity
            
        if maxpurchase > 0:
            if maxpurchase < 8:# if there are less than 9 indicators on the line
                indictamt = maxpurchase
                multiplier = 1
                spotlist = [[],[1],[1,2],[2],[],[3],[2,5]]# used to determine which spots should have text 

                for i in range(indictamt+1):# the rectanges sticking out of the line that indicate the quantity
                    if i == self.quantity:
                        pygame.draw.rect(screen,(120,120,120),pygame.Rect(1120+(i*(324/(indictamt))),140,10,40))
                        text = fontlist[30].render(f'{i}',(0,150,0))[0]
                        screen.blit(text,(1125+(i*(324/(indictamt))-(text.get_width()//2)),115))

                    elif i == 0 or i == indictamt or i in spotlist[indictamt-1]:
                        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1120+(i*(324/(indictamt))),140,10,40))
                        text = fontlist[30].render(f'{i}',(255,255,255))[0]
                        screen.blit(text,(1125+(i*(324/(indictamt))-(text.get_width()//2)),115))
                    else:
                        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1122+(i*(324/(indictamt))),145,5,30))
            else:
                indictamt = maxpurchase if maxpurchase < 8 else 8# the amount of indicators on the line

                multiplier = maxpurchase / 8 # the multiplier for the quantity - there can only be 8 lines, but they can represent any number

                for i in range(indictamt+1):# the rectanges sticking out of the line that indicate the quantity
                    if i*multiplier == self.quantity:
                        pygame.draw.rect(screen,(120,120,120),pygame.Rect(1120+(i*(324/(indictamt))),140,10,40))
                        text = fontlist[30].render(f'{int(i*multiplier)}',(0,150,0))[0]
                        screen.blit(text,(1125+(i*(324/(indictamt))-(text.get_width()//2)),115))
                    elif i == 0 or i == indictamt or i % 2 == 0:
                        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1120+(i*(324/(indictamt))),140,10,40))
                        text = fontlist[30].render(f'{int(i*multiplier)}',(255,255,255))[0]
                        screen.blit(text,(1125+(i*(324/(indictamt))-(text.get_width()//2)),115))
                    else:
                        pygame.draw.rect(screen,(0,0,0),pygame.Rect(1122+(i*(324/(indictamt))),145,5,30))
            # -------------for both greater and less than 8 indicators -----------------
            # list of all the rect objects
            rectlist = [pygame.Rect(1105+(i*(324/(indictamt))),140,40,40) for i in range(indictamt+1)]
            # first check if we are still collided from last frame
            if (n:= pygame.Rect.collidelist(pygame.Rect(mousex,mousey,1,1),rectlist)) != -1:# if the mouse is hovering over the quantity line
                tempquantity = ((n)*multiplier)# set the quantity to the amount of the line the mouse is hovering over
                if Mousebuttons == 1:
                    self.quantity = tempquantity
            
            if tempquantity != self.quantity:# if the quantity has changed
                pygame.draw.circle(screen,(225,225,225),(1125+(int(tempquantity/multiplier)*(324/(indictamt))),160),10)# the circle that moves along the line
                pygame.draw.circle(screen,(80,80,80),(1125+(int(self.quantity/multiplier)*(324/(indictamt))),160),10)# the circle that moves along the line
            else:
                pygame.draw.circle(screen,(225,225,225),(1125+(int(self.quantity/multiplier)*(324/(indictamt))),160),10)
        else:
            text = fontlist[30].render(f'{0}',(255,255,255))[0]
            screen.blit(text,(1287-(text.get_width()//2),120))
            pygame.draw.rect(screen,(0,0,0),pygame.Rect(1282,140,10,40))
            pygame.draw.circle(screen,(0,150,0),(1287,160),10)
            
    def draw_costpurchase(self,screen,Mousebuttons:int,player,stocklist:list):
        """This function is called for the cost and purchase buttons in the stockbook menu"""
        mousex,mousey = pygame.mouse.get_pos()
        # Cost button polygon and outline
        gfxdraw.filled_polygon(screen,((1110,200),(1125,250),(1465,250),(1450,200)),(30,30,30))
        pygame.draw.polygon(screen, (0,0,0), ((1110,200),(1125,250),(1465,250),(1450,200)),5)

        text = fontlist[45].render(f'Cost : ${self.quantity*stocklist[self.selectedstock].price:.2f}',(255, 255, 255))[0]
        screen.blit(text,(1175,210))

        if point_in_polygon((mousex,mousey),[(1110,265),(1125,335),(1465,335),(1450,265)]):
            purchasecolor = (0,150,0)
            if Mousebuttons == 1:
                player.buy(stocklist[self.selectedstock],stocklist[self.selectedstock].price,int(self.quantity))
                self.quantity = 0
        else:
            purchasecolor = (225,225,225)
        gfxdraw.filled_polygon(screen,((1110,265),(1125,335),(1465,335),(1450,265)),(30,30,30))#polygon for the purchase button
        pygame.draw.polygon(screen, (0,0,0), ((1110,265),(1125,335),(1465,335),(1450,265)),5)#outline confirm button polygon

        confirm_text, _ = fontlist[65].render(f'PURCHASE', purchasecolor)
        confirm_text_rect = confirm_text.get_rect(center=(1280, 300))
        screen.blit(confirm_text, confirm_text_rect)
        


    def selected_stock(self,screen,stocklist:list,player,Mousebuttons:int):
        """This function is called for the selected stock in the stockbook menu"""
        self.draw_descriptions(screen,stocklist,player,Mousebuttons)
        self.quantitycontrols(screen,Mousebuttons,player,stocklist)
        self.draw_costpurchase(screen,Mousebuttons,player,stocklist)

    
    
    
    

            