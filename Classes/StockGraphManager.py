import pygame
from pygame import gfxdraw
import math
from Defs import *
import timeit
class StockGraphManager:
    def __init__(self):
        self.graph_config = {
            'single': (1,1),
            'dual': (2,1),
            'quad': (2,2),
            'nona': (3,3),
        }
        self.images = {
            'single': pygame.image.load('Assets/graph manager/single.png').convert_alpha(),
            'dual': pygame.image.load('Assets/graph manager/dual.png').convert_alpha(),
            'quad': pygame.image.load('Assets/graph manager/quad.png').convert_alpha(),
            'nona': pygame.image.load('Assets/graph manager/nona.png').convert_alpha(),
        }
        
        self.hoverimages = {name:image for name,image in self.images.items()}
        for key,image in self.images.items():
            image = pygame.transform.scale(image,(50,50))
            surface = pygame.Surface((image.get_width()+6,image.get_height()+6))
            surface.fill((110,110,110))
            surface.blit(image,(3,3))
            self.images[key] = surface.copy()
            surface.fill((180,180,180))
            surface.blit(image,(3,3))
            self.hoverimages[key] = surface

        self.ui_rects = [pygame.Rect(745+(i*66),25,56,56) for i in range(len(self.images))]

        self.current_config = 'nona'
        self.allstocks = ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO']
        self.picked_stocks = [stock for stock in self.allstocks]
        self.mousehovering = None
        self.pickedstockconfig = {#the stock that is picked for each config
            'single': [self.allstocks[i] for i in range(1)],
            'dual': [self.allstocks[i] for i in range(2)],
            'quad': [self.allstocks[i] for i in range(4)],
            'nona': [self.allstocks[i] for i in range(9)],
        }
    
    def draw_ui(self,screen,Mousebuttons:int,stocklist:list):
        gfxdraw.filled_polygon(screen,[(710,90),(740,10),(1050,10),(1015,90)],(50,50,50))#polygon at top of screen behind ui controls
        mousex,mousey = pygame.mouse.get_pos()
        collide = None
        for i,rect in enumerate(self.ui_rects):#draws the ui controls to the screen, and senses for clicks
            if rect.collidepoint(mousex,mousey):
                collide = i
                if Mousebuttons == 1:
                    self.current_config = list(self.images.keys())[i]
                    self.picked_stocks.clear()#reset stock list and repopulate it with the correct amount of stocks (using math.prod which is a little unnecessary) in allstocks list
                    self.picked_stocks = self.pickedstockconfig[self.current_config].copy()#uses the pickedstockconfig dict to see which stocks it needs to use


        if collide == None:
            if pygame.Rect(710,10,340,80).collidepoint(mousex,mousey):
                collide = 'Not None'#this is just to make it so when you are over the polygon it will remove the hover image, otherwise everytime you go between ui images it will blink
        for i,(name,image) in enumerate(self.images.items()):
            #bit complex if statement but the first part is for the current config, and the second part is for the other configs
            if ((name == self.current_config and collide != None) and collide != list(self.images.keys()).index(self.current_config)) or (collide != i and name != self.current_config):
                screen.blit(image,(745+(i*66),25))
            elif name == self.current_config or collide == i:
                screen.blit(self.hoverimages[name],(745+(i*66),25))
    
    def changestockbutton(self,screen:pygame.Surface,startpos,endpos,Mousebuttons:int,stockname:str,stocklist:list):
        mousex,mousey = pygame.mouse.get_pos()
        #polygon at the top of each stock graph
        gfxdraw.filled_polygon(screen,[(startpos[0]-140,startpos[1]+30),(startpos[0]-130,startpos[1]+5),(startpos[0]-5,startpos[1]+5),(startpos[0]-15,startpos[1]+30)],(180,180,180))
        #Smaller polgyon on top of the first one to make it look like a button
        gfxdraw.filled_polygon(screen,[(startpos[0]-135,startpos[1]+27),(startpos[0]-130,startpos[1]+7),(startpos[0]-10,startpos[1]+7),(startpos[0]-17,startpos[1]+27)],(110,110,110))
        screen.blit(fontlist[25].render('SWAP STOCK',(0,0,0))[0],(startpos[0]-120,startpos[1]+10))
        #seeing if the mouse is hovering over the button
        if pygame.Rect(startpos[0]-140,startpos[1]+5,135,25).collidepoint(mousex,mousey) or self.mousehovering == stockname:

            if pygame.Rect(startpos[0]-140,startpos[1]+5,135,245).collidepoint(mousex,mousey):#if the mouse is hovering over the button or the list of stocks below it
                self.mousehovering = stockname

            for stock in self.allstocks:#draws the list of stocks below the button
                if stock != stockname and stock not in self.picked_stocks:#if the stock is not the current stock
                    index_place = len([used_stock for used_stock in self.allstocks if used_stock in self.picked_stocks and self.allstocks.index(used_stock) < self.allstocks.index(stock)])-1
                    
                    yadj = ((self.allstocks.index(stock)-index_place)*30)

                    color = (0,0,180)#default color
                    if pygame.Rect(startpos[0]-140,startpos[1]+5+yadj,135,25).collidepoint(mousex,mousey):#if the mouse is hovering over the stock button
                        color = (0,180,180)
                        if Mousebuttons == 1:
                            Mousebuttons = 0
                            # oldstockobj = [stockobj for stockobj in stocklist if stockobj.name == stockname][0]#finds the stock object of the stock that is being replaced
                            # stockobj = [stockobj for stockobj in stocklist if stockobj.name == stock][0]#finds the stock object of the stock that is replacing the old stock
                            #resets the pricepoints except for the last one, which keeps the y (current price) and uses the x from the old stock object
                            # stockobj.pricepoints = [[oldstockobj.startingpos[0],stockobj.pricepoints[-1][1]]] 
                            self.picked_stocks[self.picked_stocks.index(stockname)] = stock#replaces the old stock with the new stock in the picked_stocks list
                            self.pickedstockconfig[self.current_config][self.pickedstockconfig[self.current_config].index(stockname)] = stock#replaces the old stock with the new stock in the pickedstockconfig dict
                            self.mousehovering = None
                    #draws the stock button, and the name of the stock
                    # gfxdraw.filled_polygon(screen,[(startpos[0]-140,startpos[1]+30+yadj),(startpos[0]-130,startpos[1]+5+yadj),(startpos[0]-55,startpos[1]+5+yadj),(startpos[0]-60,startpos[1]+30+yadj)],color)
                    gfxdraw.filled_polygon(screen,[(startpos[0]-113,startpos[1]+30+yadj),(startpos[0]-103,startpos[1]+5+yadj),(startpos[0]-32,startpos[1]+5+yadj),(startpos[0]-37,startpos[1]+30+yadj)],color)
                    screen.blit(fontlist[25].render(stock,(255,255,255))[0],(startpos[0]-92,startpos[1]+yadj+10))
                    

        if stockname == self.mousehovering and not pygame.Rect(startpos[0]-140,startpos[1]+5,135,250).collidepoint(mousex,mousey):
            self.mousehovering = None


    def draw_graphs(self, screen, stocklist:list, player, play_pause, Mousebuttons, menudrawn:bool, stockbook,currentime):
        self.draw_ui(screen,Mousebuttons,stocklist)
        
        for i in range(self.graph_config[self.current_config][1]):
            for ii in range(self.graph_config[self.current_config][0]):
                xlength = int(1400/self.graph_config[self.current_config][0])
                ylength = int(880/self.graph_config[self.current_config][1])
                # print(xlength,ylength,'xlength,ylength')
                
                startpos = ((ii+1)*xlength+200,i*ylength+100)
                endpos = (ii*xlength+200,(i+1)*ylength+100)                

                stockname = self.picked_stocks[(i*self.graph_config[self.current_config][0])+ii]

                stock = [stock for stock in stocklist if stock.name == stockname][0]
                # if not [obj.name for obj in stocklist][stockbook.selectedstock] == stockname or not stockbook.menudrawn:#make sure the stock isn't being drawn on the buy sell page
                #     stock.update(screen,play_pause,player,startpos,endpos,drawn=not menudrawn)
                if not menudrawn:
                    stock.draw(screen,player,startpos,endpos,stocklist)
                    
                if self.current_config != 'nona' and not menudrawn:
                    self.changestockbutton(screen,startpos,endpos,Mousebuttons,stockname,stocklist)
                # stock.buy_sell(player,screen,Mousebuttons)
                

        # for stock in stocklist:
        #     if not [obj.name for obj in stocklist][stockbook.selectedstock] == stock.name or not stockbook.menudrawn:
        #         if stock.name not in self.picked_stocks:
        #             stock.update(screen,play_pause,player,startpos,endpos,drawn=False)

        # player.update(screen,play_pause,player,(1920,0),(1600,400),stocklist=stocklist)
        # player.draw(screen,player,(1920,0),(1600,400),stocklist,currentime)
