import pygame
from Defs import *
from pygame import gfxdraw

class Stockbook:
    def __init__(self,stocknames:list) -> None:
        surface = pygame.Surface((140,115))
        self.icon = pygame.image.load(r'Assets\book.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon,(140,100))
        surface.fill((60,60,60))
        surface.blit(self.icon,(0,5))
        pygame.draw.rect(surface,(0,0,0),pygame.Rect(0,0,140,115),5)
        self.icon = surface.copy()
        self.buyselltext = fontlist[36].render('BUY & SELL',(255,255,255))[0]
        self.menudrawn = False
        self.selectedstock = 0

        self.stocktext = {name:[] for name in stocknames}
        
        with open(r'Assets\stockdescriptions.txt','r') as descriptions:

            filecontents = descriptions.readlines()
            for i,line in enumerate(filecontents):
                print(line.replace('\n',''))
                for stockname in stocknames:
                    print(line.replace('\n',''))
                    if line.replace('\n','') == stockname:
                        for x in range(1,5):
                            self.stocktext[stockname].append(filecontents[i+x].replace('\n',''))

        self.renderedstocknames = {name:fontlist[90].render(name,(150,150,150))[0] for name in stocknames}
        for key,lines in self.stocktext.items():
            for i,line in enumerate(lines):
                if i == 0:
                    self.stocktext[key][i] = fontlist[40].render(line,(120, 120, 120))[0]
                else:
                    self.stocktext[key][i] = fontlist[30].render(line,(255, 117, 24))[0]

    def draw_icon(self,screen:pygame.Surface,Mousebuttons:int,stocklist:list,play_pause):
        if self.icon_sensing(screen,Mousebuttons,stocklist,play_pause):
            width1 = self.icon.get_width(); height1 = self.icon.get_height();height2 = self.buyselltext.get_height()
            gfxdraw.filled_polygon(screen,[(25,95),(width1+35,95),(width1+35,110+height1+height2),(25,110+height1+height2)],(110,110,110))
        screen.blit(self.icon,(30,100))
        screen.blit(self.buyselltext,(50,self.icon.get_height()+105))
    
    def icon_sensing(self,screen,mousebuttons:int,stocklist,play_pause):
        # print(pygame.mouse.get_pos())
        mousex,mousey = pygame.mouse.get_pos()
        collide = pygame.Rect.collidepoint(pygame.Rect(30,100,self.icon.get_width(),self.icon.get_height()+self.buyselltext.get_height()),mousex,mousey)
        if self.menudrawn:
            self.draw_menu(screen,stocklist,mousebuttons,play_pause)

        if collide:
            if mousebuttons == 1:
                self.menudrawn = not self.menudrawn
            else:
                return True

    def draw_menu(self,screen:pygame.Surface,stocklist:list,Mousebuttons:int,play_pause):
        gfxdraw.filled_polygon(screen, ((200,100),(1500,100),(1600,980),(300,980)),(40,40,40))
        pygame.draw.polygon(screen, (0,0,0), ((200,100),(1500,100),(1600,980),(300,980)),10)
        
        for i,stock in enumerate(stocklist):
            if self.menu_sensing(pygame.Rect(215+(i*8),120+(i*65),175,35)) and Mousebuttons == 1:
                self.selectedstock = i
            if stock.recent_movementvar[2] == (180,180,180):
                color = (0,0,150)  if self.selectedstock == i else (80,80,80) 
            else:
                color = stock.recent_movementvar[2]
            gfxdraw.filled_polygon(screen,((215+(i*8),120+(i*65)),(225+(i*8),155+(i*65)),(400+(i*8),155+(i*65)),(390+(i*8),120+(i*65))),color)
            screen.blit(fontlist[36].render(f'{stock.name} ${round(stock.pricepoints[-1][1],2)}',(255,255,255))[0],(225+(i*8),125+(i*65)))
            if self.selectedstock == i:
                pygame.draw.polygon(screen, (0,0,0), ((215+(i*8),120+(i*65)),(225+(i*8),155+(i*65)),(400+(i*8),155+(i*65)),(390+(i*8),120+(i*65))),5)
                self.selected_stock(screen,stocklist,play_pause)

            if Mousebuttons == 1:#CAN REMOVE LATER ------------------------------------------------------------
                print(pygame.mouse.get_pos())
            
    
    def menu_sensing(self,rect:pygame.Rect):
        mousex,mousey = pygame.mouse.get_pos()
        if pygame.Rect.collidepoint(rect,mousex,mousey):
            return True
        return False
    
    def draw_info(self,screen:pygame.Surface,stocklist:list,play_pause):
        gfxdraw.filled_polygon(screen,((290,700),(320,955),(1570,955),(1535,700)),(60,60,60))

        screen.blit(fontlist[90].render(f'{stocklist[self.selectedstock].name}',(255,255,255))[0],(300,710))
        screen.blit(self.renderedstocknames[stocklist[self.selectedstock].name],(300,710))

        stocklist[self.selectedstock].update(screen,play_pause,None,(1100,130),(500,680),drawn=True)
        for i,line in enumerate(self.stocktext[stocklist[self.selectedstock].name]):
            x,y = (305+((i-1)*8) if i != 0 else self.renderedstocknames[stocklist[self.selectedstock].name].get_width()+310),(800+((i-1)*40) if i != 0 else 725)
            screen.blit(line,(x,y))

    def selected_stock(self,screen,stocklist:list,play_pause):
        self.draw_info(screen,stocklist,play_pause)
    

            