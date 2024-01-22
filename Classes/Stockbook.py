import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.Menu import Menu
import numpy as np
from Classes.imports.Bar import SliderBar
def quantityControls(screen, mousebuttons:int, maxpurchase, quantity, coords):
    """This function is called for the buy and sell controls in the stockbook menu"""
    mousex, mousey = pygame.mouse.get_pos()
    x, y = coords[0],coords[1]+100
    tempquantity = quantity
    # quantity controls
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x + 15, y - 45, 334, 10))  # line with circles on it for the quantity

    if maxpurchase > 0:# if the player can afford to buy the stock
        if maxpurchase < 8:  # if there are less than 9 indicators on the line
            indictamt = maxpurchase
            multiplier = 1
            spotlist = [[], [1], [1, 2], [2], [], [3], [2, 5]]  # used to determine which spots should have text
            quantity = int(maxpurchase) if quantity > maxpurchase else quantity# Never let the quantity be greater than the max purchase

            for i in range(indictamt + 1):  # the rectanges sticking out of the line that indicate the quantity
                if i == quantity:
                    pygame.draw.rect(screen, (120, 120, 120),pygame.Rect(x + 15 + (i * (324 / (indictamt))), y - 60, 10, 40))
                    text = fontlist[30].render(f'{i}', (0, 150, 0))[0]
                    screen.blit(text, (x + 20 + (i * (324 / (indictamt))) - (text.get_width() // 2), y - 85))

                elif i == 0 or i == indictamt or i in spotlist[indictamt - 1]:
                    pygame.draw.rect(screen, (0, 0, 0),pygame.Rect(x + 15 + (i * (324 / (indictamt))), y - 60, 10, 40))
                    text = fontlist[30].render(f'{i}', (255, 255, 255))[0]
                    screen.blit(text, (x + 20 + (i * (324 / (indictamt))) - (text.get_width() // 2), y - 85))
                else:
                    pygame.draw.rect(screen, (0, 0, 0),pygame.Rect(x + 17 + (i * (324 / (indictamt))), y - 55, 5, 30))
        else:
            indictamt = maxpurchase if maxpurchase < 8 else 8  # the amount of indicators on the line
            multiplier = maxpurchase / 8  # the multiplier for the quantity - there can only be 8 lines, but they can represent any number

            if quantity % int(multiplier) != 0:  # if the quantity is not a multiple of the multiplier
                
                quantity = int((quantity/maxpurchase)*8*multiplier)#turning quanity into an valid index
                if quantity < (maxpurchase*multiplier):
                    quantity = int(round(quantity / multiplier)) * multiplier

            quantity = int(maxpurchase) if quantity > maxpurchase else quantity# Never let the quantity be greater than the max purchase
                # quantity = quantity if quantity <= maxpurchase else quantity - int(multiplier)  # if the quantity is less than the max purchase, add the multiplier, else subtract it
            
            for i in range(indictamt + 1):  # the rectanges sticking out of the line that indicate the quantity
                if i == int(quantity / multiplier):
                    pygame.draw.rect(screen, (120, 120, 120),pygame.Rect(x + 15 + (i * (324 / (indictamt))), y - 60, 10, 40))
                    text = fontlist[30].render(f'{int(i * multiplier)}', (0, 150, 0))[0]
                    screen.blit(text, (x + 20 + (i * (324 / (indictamt))) - (text.get_width() // 2), y - 85))
                elif i == 0 or i == indictamt or i % 2 == 0:
                    pygame.draw.rect(screen, (0, 0, 0),pygame.Rect(x + 15 + (i * (324 / (indictamt))), y - 60, 10, 40))
                    text = fontlist[30].render(f'{int(i * multiplier)}', (255, 255, 255))[0]
                    screen.blit(text, (x + 20 + (i * (324 / (indictamt))) - (text.get_width() // 2), y - 85))
                else:
                    pygame.draw.rect(screen, (0, 0, 0),pygame.Rect(x + 17 + (i * (324 / (indictamt))), y - 55, 5, 30))

        # -------------for both greater and less than 8 indicators -----------------

        # list of all the rect objects
        rectlist = [pygame.Rect(x + 5 + (i * (324 / (indictamt))), y - 60, 40, 40) for i in range(indictamt + 1)]
        # first check if we are still collided from last frame
        if (n := pygame.Rect.collidelist(pygame.Rect(mousex, mousey, 1, 1), rectlist)) != -1:  # if the mouse is hovering over the quantity line
            tempquantity = ((n) * multiplier)  # set the quantity to the amount of the line the mouse is hovering over
            if mousebuttons == 1:
                quantity = tempquantity

        if tempquantity != quantity:  # if the quantity has changed
            pygame.draw.circle(screen, (225, 225, 225),(x + 20 + int(tempquantity / multiplier) * (324 / (indictamt)), y - 35), 10)  # the circle that moves along the line
            pygame.draw.circle(screen, (80, 80, 80),(x + 20 + int(quantity / multiplier) * (324 / (indictamt)), y - 35), 10)  # the circle that moves along the line
        else:
            pygame.draw.circle(screen, (225, 225, 225),(x + 20 + int(quantity / multiplier) * (324 / (indictamt)), y - 35), 10)
    else:
        text = fontlist[30].render(f'{0}', (255, 255, 255))[0]
        screen.blit(text, (x + 182 - (text.get_width() // 2), y - 80))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x + 177, y - 60, 10, 40))
        pygame.draw.circle(screen, (0, 150, 0), (x + 182, y - 40), 10)
    return quantity

class Stockbook(Menu):
    def __init__(self,stocknames:list) -> None:
        self.icon = pygame.image.load(r'Assets\Menu_Icons\stockbook.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon,(140,100))
        super().__init__(self.icon)
        self.quantity = 0
        self.stocktext = {name:[] for name in stocknames}
        self.selectedstock = 0
        self.menudrawn = False
        self.purchasetext = [fontlist[65].render(text, color)[0] for text,color in zip(['PURCHASE','PURCHASE','INSUFFICIENT'],[(0,150,0),(225,225,225),(150,0,0)])]
        self.quantitybar = SliderBar(50,[(150,150,150),(10,10,10)],barcolor=((20,130,20),(40,200,40)))
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
                    self.stocktext[key][i] = fontlist[30].render(line,(225, 130, 0))[0]
        
    def draw_menu_content(self,screen:pygame.Surface,stocklist:list,mousebuttons:int,player):
        """Draws all the main content for the stockbook menu (the stocks on the left side of the screen)"""
        mousex,mousey = pygame.mouse.get_pos()
        for i,stock in enumerate(stocklist):
            points = [(215+(i*8),120+(i*65)),(225+(i*8),160+(i*65)),(450+(i*8),160+(i*65)),(440+(i*8),120+(i*65))]
            if (hover:=point_in_polygon((mousex,mousey),points)):#if the mouse is hovering over the stock name
                if mousebuttons == 1:#if the mouse is hovering over the stock
                    self.selectedstock = i
                    soundEffects['clickbutton2'].play()
                    self.quantity = 0

            change = stock.price - stock.graphrangelists[stock.graphrange][0]
            if hover or self.selectedstock == i:
                color = (0, 160, 0) if change > 0 else (160, 0, 0)
                color = (160, 160, 160) if change == 0 else color
            else:
                color = (0, 80, 0) if change > 0 else (80, 0, 0)
                color = (80, 80, 80) if change == 0 else color

            gfxdraw.filled_polygon(screen,points,color)# polygon for the stock name
            outlinecolor = (0, 0, 0) if self.selectedstock != i else (180, 180, 180)#
            pygame.draw.polygon(screen, outlinecolor, points,5)

            screen.blit(fontlist[36].render(f'{stock.name} ${limit_digits(stock.price,12)}',(255,255,255))[0],(230+(i*8),130+(i*65)))
            if self.selectedstock == i:
                self.selected_stock(screen,stocklist,player,mousebuttons)

    def draw_descriptions(self,screen:pygame.Surface,stocklist:list,player,mousebuttons):
        """Draws the stock descriptions and the stock graph for the selected stock"""
        gfxdraw.filled_polygon(screen,((290,700),(320,955),(1570,955),(1535,700)),(60,60,60))#  polygon for the stock description
        screen.blit(self.renderedstocknames[stocklist[self.selectedstock].name],(300,710))# blits the stock name to the screen

        # stocklist[self.selectedstock].update(screen,play_pause,player,(1100,130),(500,680),drawn=True)
        stocklist[self.selectedstock].draw(screen,player,(550,130),(550,550),stocklist,mousebuttons)
        for i,line in enumerate(self.stocktext[stocklist[self.selectedstock].name]):
            x,y = (305+((i-1)*8) if i != 0 else self.renderedstocknames[stocklist[self.selectedstock].name].get_width()+310),(800+((i-1)*40) if i != 0 else 725)
            screen.blit(line,(x,y))
            
    def draw_costpurchase(self,screen,mousebuttons:int,player,stocklist:list,abletobuy:bool):
        """This function is called for the cost and purchase buttons in the stockbook menu"""
        mousex,mousey = pygame.mouse.get_pos()
        # Cost button polygon and outline
        gfxdraw.filled_polygon(screen,((1110,200),(1125,250),(1465,250),(1450,200)),(30,30,30))
        pygame.draw.polygon(screen, (0,0,0), ((1110,200),(1125,250),(1465,250),(1450,200)),5)

        text = fontlist[45].render(f'Cost : ${self.quantity*stocklist[self.selectedstock].price:.2f}',(255, 255, 255))[0]
        screen.blit(text,(1175,210))

        if abletobuy and point_in_polygon((mousex,mousey),[(1110,265),(1125,335),(1465,335),(1450,265)]):
            purchasecolor = (0,150,0)
            if mousebuttons == 1:
                player.buy(stocklist[self.selectedstock],stocklist[self.selectedstock].price,int(self.quantity))
                self.quantity = 0
        elif not abletobuy:
            purchasecolor = (150,0,0)
        else:
            purchasecolor = (225,225,225)
        gfxdraw.filled_polygon(screen,((1110,265),(1125,335),(1465,335),(1450,265)),(30,30,30))#polygon for the purchase button
        pygame.draw.polygon(screen, (0,0,0), ((1110,265),(1125,335),(1465,335),(1450,265)),5)#outline confirm button polygon

        confirm_text = self.purchasetext[[(0,150,0),(225,225,225),(150,0,0)].index(purchasecolor)]
        confirm_text_rect = confirm_text.get_rect(center=(1280, 300))
        screen.blit(confirm_text, confirm_text_rect)
        


    def selected_stock(self,screen,stocklist:list,player,mousebuttons:int):
        """This function is called for the selected stock in the stockbook menu"""
        self.draw_descriptions(screen,stocklist,player,mousebuttons)
        # self.quantitycontrols(screen,mousebuttons,player,stocklist)
        stock = stocklist[self.selectedstock]
        # self.quantity = quantityControls(screen,mousebuttons,int(player.cash/stock.price),self.quantity,(1105,110))
        abletobuy = int(player.cash/stock.price) > 0
        if abletobuy:
            self.quantitybar.changemaxvalue(int(player.cash/stock.price))
            self.quantitybar.draw_bar(screen,[1110,140],[340,45],orientation='horizontal',reversedscroll=True)
            self.quantity = self.quantitybar.value
        else:
            self.quantity = 0
            
        self.draw_costpurchase(screen,mousebuttons,player,stocklist,abletobuy)

    
    
    
    

            