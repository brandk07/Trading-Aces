import pygame
from Defs import *
from pygame import gfxdraw
from Classes.menu import Menu

class Stockbook(Menu):
    def __init__(self,stocknames:list) -> None:
        super().__init__(r'Assets\stockbook\book.png',(30,150))
        self.quantity = 0
        self.stocktext = {name:[] for name in stocknames}
        self.uparrow = pygame.image.load(r'Assets\stockbook\uparrow.png').convert_alpha()
        self.uparrow = pygame.transform.scale(self.uparrow,(33,18))
        self.downarrow = pygame.transform.flip(self.uparrow,False,True)
        self.buying = True#if false then selling
        self.selectedstock = 0
        
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
        mousex,mousey = pygame.mouse.get_pos()
        for i,stock in enumerate(stocklist):
            if pygame.Rect.collidepoint(pygame.Rect(215+(i*8),120+(i*65),175,35),mousex,mousey) and Mousebuttons == 1:#if the mouse is hovering over the stock
                self.selectedstock = i
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

    def draw_info(self,screen:pygame.Surface,stocklist:list,player,Mousebuttons):
        gfxdraw.filled_polygon(screen,((290,700),(320,955),(1570,955),(1535,700)),(60,60,60))

        screen.blit(fontlist[90].render(f'{stocklist[self.selectedstock].name}',(255,255,255))[0],(300,710))
        screen.blit(self.renderedstocknames[stocklist[self.selectedstock].name],(300,710))

        # stocklist[self.selectedstock].update(screen,play_pause,player,(1100,130),(500,680),drawn=True)
        stocklist[self.selectedstock].draw(screen,player,(1100,130),(500,680),stocklist,Mousebuttons)
        for i,line in enumerate(self.stocktext[stocklist[self.selectedstock].name]):
            x,y = (305+((i-1)*8) if i != 0 else self.renderedstocknames[stocklist[self.selectedstock].name].get_width()+310),(800+((i-1)*40) if i != 0 else 725)
            screen.blit(line,(x,y))

    def quantity_controls(self,screen,Mousebuttons:int,player,stocklist:list):
        quantitytext = fontlist[40].render(f'Quanity : {self.quantity}',(255,255,255))[0]
        x = 1150+quantitytext.get_width()+self.uparrow.get_width()

        gfxdraw.filled_polygon(screen,((1125,140),(x+165,140),(x+150,190),(1110,190)),(30,30,30))
        pygame.draw.polygon(screen, (0,0,0), ((1125,140),(x+165,140),(x+150,190),(1110,190)),5)

        
        screen.blit(quantitytext,(1125,150))
        # gfxdraw
        screen.blit(self.uparrow,(1140+quantitytext.get_width(),146))
        screen.blit(self.downarrow,(1140+quantitytext.get_width(),140+24))
        mousex,mousey = pygame.mouse.get_pos()
        #sensing for the up and down arrows
        if pygame.Rect.collidepoint(pygame.Rect(1140+quantitytext.get_width(),146,self.uparrow.get_width(),self.uparrow.get_height()),mousex,mousey):
            if Mousebuttons == 1:
                self.quantity += 1
        if pygame.Rect.collidepoint(pygame.Rect(1140+quantitytext.get_width(),140+24,self.downarrow.get_width(),self.downarrow.get_height()),mousex,mousey):
            if Mousebuttons == 1 and self.quantity > 0:
                self.quantity -= 1
        
        for i in range(0,3):#the three buttons to the right of the quantity text
            if i == 2:
                gfxdraw.filled_polygon(screen,((x+(i*50),148),(x+(i*50)+45,148),(x+(i*50)+45,180),(x+(i*50),180)),(80,80,80))
            else:
                gfxdraw.filled_polygon(screen,((x+(i*50),148),(x+(i*50)+35,148),(x+(i*50)+35,180),(x+(i*50),180)),(80,80,80))
            screen.blit(fontlist[36].render(f'{["+2","+5","MAX"][i]}',(200,200,200))[0],(x+(i*50)+5,152))
            if pygame.Rect.collidepoint(pygame.Rect(x+(i*50),144,35,40),mousex,mousey):
                if Mousebuttons == 1:
                    if i == 0: self.quantity += 2
                    elif i == 1: self.quantity += 5
                    elif i == 2: 
                        if self.buying:self.quantity = int(player.cash/stocklist[self.selectedstock].price)
                        else: self.quantity = [stock[0] for stock in player.stocks].count(stocklist[self.selectedstock].name)
        if not self.buying:# if selling
            
            if self.quantity > (num:=[stock[0] for stock in player.stocks].count(stocklist[self.selectedstock].name)):#if the quantity is greater than the amount of stocks the player has
                self.quantity = num 
                player.messagedict[f"Invalid Stock Quantity"] = (time.time(),(200,0,0))

    def buysell_controls(self,screen,Mousebuttons:int,player,stocklist:list):
        gfxdraw.filled_polygon(screen,((1125,200),(1110,250),(1450,250),(1465,200)),(30,30,30))#polygon for the buy and sell button
        pygame.draw.polygon(screen, (0,0,0), ((1125,200),(1110,250),(1450,250),(1465,200)),5)#outline for the buy and sell button
        gfxdraw.filled_polygon(screen,((1280,200),(1265,250),(1270,250),(1285,200)),(0,0,0))#polygon for the line in the middle of the buy and sell button
        
        mousex,mousey = pygame.mouse.get_pos()
        buycolor,sellcolor = (200,200,200),(200,200,200)

        if pygame.Rect.collidepoint(pygame.Rect(1110,200,170,50),mousex,mousey):
            buycolor = (0,150,0);sellcolor = (200,200,200)
            if Mousebuttons == 1:self.buying = True
        if pygame.Rect.collidepoint(pygame.Rect(1280,200,170,50),mousex,mousey):
            sellcolor = (150,0,0);buycolor = (200,200,200)
            if Mousebuttons == 1:self.buying = False
        if self.buying and sellcolor == (200,200,200): buycolor = (0,150,0)
        elif not self.buying and buycolor == (200,200,200): sellcolor = (150,0,0)
        screen.blit(fontlist[45].render('BUY',buycolor)[0],(1175,210))
        screen.blit(fontlist[45].render('SELL',sellcolor)[0],(1335,210))

        text_surface, _ = fontlist[45].render(f'Total : ${round(self.quantity*stocklist[self.selectedstock].price,2)}', (255, 255, 255))
        text_width = text_surface.get_width()
        #the x coords on the left of the polygon need to be switched
        gfxdraw.filled_polygon(screen, ((1125, 260), (1125 + text_width + 35, 260), (1125 + text_width + 20, 310), (1110, 310)), (30, 30, 30))
        pygame.draw.polygon(screen, (0, 0, 0), ((1125, 260), (1125 + text_width + 35, 260), (1125 + text_width + 20, 310), (1110, 310)), 5)
        screen.blit(text_surface, (1130, 270))

        #add a new polygon below that one with a confirm button that will buy or sell the stocks using the player.buy_stock() or player.sell_stock() functions
        

        
        # make both the polygons below larger in the y direction and center the confirm button
        
        confirmcolor = (30,30,30)
        if pygame.Rect.collidepoint(pygame.Rect(1125,320,340,80),mousex,mousey) and self.quantity > 0:
            if self.buying and self.quantity*stocklist[self.selectedstock].price <= player.cash:
                 confirmcolor = (0,150,0) 
            elif not self.buying and self.quantity <= [stock[0] for stock in player.stocks].count(stocklist[self.selectedstock].name):
                confirmcolor = (0,150,0)
            else:
                confirmcolor = (150,0,0)
            if Mousebuttons == 1:
                if self.buying and self.quantity*stocklist[self.selectedstock].price <= player.cash:
                    player.buy(stocklist[self.selectedstock].name,stocklist[self.selectedstock].price,stocklist[self.selectedstock],self.quantity)
                elif self.buying and self.quantity*stocklist[self.selectedstock].price > player.cash:
                    self.quantity = int(player.cash/stocklist[self.selectedstock].price)
                    player.messagedict[f"Not Enough Funds"] = (time.time(),(200,0,0))
                else:
                    player.sell(stocklist[self.selectedstock].name,stocklist[self.selectedstock].price,stocklist[self.selectedstock],self.quantity)
                    if self.quantity > (num:=[stock[0] for stock in player.stocks].count(stocklist[self.selectedstock].name)):
                        self.quantity = num

        gfxdraw.filled_polygon(screen,((1125,320),(1110,400),(1450,400),(1465,320)),confirmcolor)#polygon for the confirm button
        pygame.draw.polygon(screen, (0,0,0), ((1125,320),(1110,400),(1450,400),(1465,320)),5)#outline confirm button polygon
        confirm_text, _ = fontlist[55].render(f'CONFIRM', (255, 255, 255))
        confirm_text_rect = confirm_text.get_rect(center=(1280, 360))
        screen.blit(confirm_text, confirm_text_rect)
        


    def selected_stock(self,screen,stocklist:list,player,Mousebuttons:int):
        """This function is called for the selected stock in the stockbook menu"""
        self.draw_info(screen,stocklist,player,Mousebuttons)
        self.quantity_controls(screen,Mousebuttons,player,stocklist)
        self.buysell_controls(screen,Mousebuttons,player,stocklist)
    
    
    
    

            