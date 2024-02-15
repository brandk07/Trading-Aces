import pygame
from pygame import gfxdraw
import math
from Defs import *
import timeit
class StockGraphManager:
    def __init__(self,stocknames):
        self.graph_config = {
            'single': (1,1),
            'quad': (2,2),
            'six' : (3,2),
            'nona': (3,3),
        }
        self.images = {
            'single': pygame.image.load('Assets/graph manager/single.png').convert_alpha(),
            'quad': pygame.image.load('Assets/graph manager/quad.png').convert_alpha(),
            'six' : pygame.image.load('Assets/graph manager/six.png').convert_alpha(),
            'nona': pygame.image.load('Assets/graph manager/nona.png').convert_alpha(),
        }
        
        self.hoverimages = {name:image for name,image in self.images.items()}
        for key,image in self.images.items():# makes the hover images for the ui controls (the images that appear brighter when you hover over them)
            image = pygame.transform.scale(image,(50,50))
            surface = pygame.Surface((image.get_width()+6,image.get_height()+6))
            surface.fill((110,110,110))
            surface.blit(image,(3,3))
            self.images[key] = surface.copy()
            surface.fill((180,180,180))
            surface.blit(image,(3,3))
            self.hoverimages[key] = surface

        self.ui_rects = [pygame.Rect(745+(i*66),990,56,56) for i in range(len(self.images))]
        self.wh = [1400,880]# the start coords of the graph

        self.current_config = 'nona'
        self.allstocks = stocknames

        self.picked_stocks = [stock for stock in self.allstocks]
        self.mousehovering = None
        self.pickedstockconfig = {#the stocks that are picked for each config
            'single': [self.allstocks[i] for i in range(1)],
            'quad': [self.allstocks[i] for i in range(4)],
            'six': [self.allstocks[i] for i in range(6)],
            'nona': [self.allstocks[i] for i in range(9)],
        }
        # self.mcontrolstext = [[fontlist[45].render(text,(220,220,220))[0],text.lower()] for text in ["1H","1D","1W","1M","3M","1Y","Custom"]]
        self.renderedstocknames = {name:fontlist[25].render(name,(255,255,255))[0] for name in self.allstocks}
        self.masterrange = "1H"
        self.dragstock = [None,None,None]# [stock object, xoffset, yoffset]

    def draw_ui(self,screen,mousebuttons:int,stocklist:list):
        # gfxdraw.filled_polygon(screen,[(710,90),(740,10),(1050,10),(1015,90)],(50,50,50))#polygon at top of screen behind ui controls
        mousex,mousey = pygame.mouse.get_pos()
        collide = None
        for i,rect in enumerate(self.ui_rects):#draws the ui controls to the screen, and senses for clicks
            if rect.collidepoint(mousex,mousey):
                collide = i
                if mousebuttons == 1:
                    self.pickedstockconfig[self.current_config] = self.picked_stocks.copy()#saves the current stock config
                    self.current_config = list(self.images.keys())[i]
                    self.picked_stocks.clear()#reset stock list and repopulate it with the correct amount of stocks (using math.prod which is a little unnecessary) in allstocks list
                    self.picked_stocks = self.pickedstockconfig[self.current_config].copy()#uses the pickedstockconfig dict to see which stocks it needs to use

        if collide == None:
            if pygame.Rect(710,10,340,80).collidepoint(mousex,mousey):
                collide = 'Not None'#this is just to make it so when you are over the polygon it will remove the hover image, otherwise everytime you go between ui images it will blink
        for i,(name,image) in enumerate(self.images.items()):
            #bit complex if statement but the first part is for the current config, and the second part is for the other configs
            if ((name == self.current_config and collide != None) and collide != list(self.images.keys()).index(self.current_config)) or (collide != i and name != self.current_config):
                screen.blit(image,(745+(i*66),990))
            elif name == self.current_config or collide == i:
                screen.blit(self.hoverimages[name],(745+(i*66),990))
    
    # def changestockbutton(self,screen:pygame.Surface,startpos,endpos,mousebuttons:int,stockname:str,stocklist:list):
    #     mousex,mousey = pygame.mouse.get_pos()
    #     #polygon at the top of each stock graph
    #     gfxdraw.filled_polygon(screen,[(startpos[0]-140,startpos[1]+30),(startpos[0]-130,startpos[1]+5),(startpos[0]-5,startpos[1]+5),(startpos[0]-15,startpos[1]+30)],(180,180,180))
    #     #Smaller polgyon on top of the first one to make it look like a button
    #     gfxdraw.filled_polygon(screen,[(startpos[0]-135,startpos[1]+27),(startpos[0]-130,startpos[1]+7),(startpos[0]-10,startpos[1]+7),(startpos[0]-17,startpos[1]+27)],(110,110,110))
    #     screen.blit(fontlist[25].render('SWAP STOCK',(0,0,0))[0],(startpos[0]-120,startpos[1]+10))
    #     #seeing if the mouse is hovering over the button
    #     if pygame.Rect(startpos[0]-140,startpos[1]+5,135,25).collidepoint(mousex,mousey) or self.mousehovering == stockname:

    #         if pygame.Rect(startpos[0]-140,startpos[1]+5,135,245).collidepoint(mousex,mousey):#if the mouse is hovering over the button or the list of stocks below it
    #             self.mousehovering = stockname

    #         for stock in self.allstocks:#draws the list of stocks below the button
    #             if stock != stockname and stock not in self.picked_stocks:#if the stock is not the current stock
    #                 index_place = len([used_stock for used_stock in self.allstocks if used_stock in self.picked_stocks and self.allstocks.index(used_stock) < self.allstocks.index(stock)])-1
                    
    #                 yadj = ((self.allstocks.index(stock)-index_place)*30)

    #                 color = (0,0,180)#default color
    #                 if pygame.Rect(startpos[0]-140,startpos[1]+5+yadj,135,25).collidepoint(mousex,mousey):#if the mouse is hovering over the stock button
    #                     color = (0,180,180)
    #                     if mousebuttons == 1:
    #                         mousebuttons = 0
    #                         # oldstockobj = [stockobj for stockobj in stocklist if stockobj.name == stockname][0]#finds the stock object of the stock that is being replaced
    #                         # stockobj = [stockobj for stockobj in stocklist if stockobj.name == stock][0]#finds the stock object of the stock that is replacing the old stock
    #                         self.picked_stocks[self.picked_stocks.index(stockname)] = stock#replaces the old stock with the new stock in the picked_stocks list
    #                         self.pickedstockconfig[self.current_config][self.pickedstockconfig[self.current_config].index(stockname)] = stock#replaces the old stock with the new stock in the pickedstockconfig dict
    #                         self.mousehovering = None
    #                 #draws the stock button, and the name of the stock
    #                 # gfxdraw.filled_polygon(screen,[(startpos[0]-140,startpos[1]+30+yadj),(startpos[0]-130,startpos[1]+5+yadj),(startpos[0]-55,startpos[1]+5+yadj),(startpos[0]-60,startpos[1]+30+yadj)],color)
    #                 gfxdraw.filled_polygon(screen,[(startpos[0]-113,startpos[1]+30+yadj),(startpos[0]-103,startpos[1]+5+yadj),(startpos[0]-32,startpos[1]+5+yadj),(startpos[0]-37,startpos[1]+30+yadj)],color)
    #                 screen.blit(fontlist[25].render(stock,(255,255,255))[0],(startpos[0]-92,startpos[1]+yadj+10))
                    

    #     if stockname == self.mousehovering and not pygame.Rect(startpos[0]-140,startpos[1]+5,135,250).collidepoint(mousex,mousey):
    #         self.mousehovering = None
    
    def stockBar(self, screen: pygame.Surface, stocklist: list):

        def stockOver(mousex, mousey, picked_stocks, draggedstock):
            # stocknames = [stock.name for stock in stocklist]
            for i, selected in enumerate(picked_stocks):
                # stock = stocklist[stocknames.index(selected)]
                xlength = self.wh[0]/self.graph_config[self.current_config][0]
                ylength = self.wh[1]/self.graph_config[self.current_config][1]

                yind = i//self.graph_config[self.current_config][0]
                xind = i-(yind*self.graph_config[self.current_config][0])
                stockcoords = (xind*xlength+200, yind*ylength+100)
                stockwh = (xlength, ylength)

                if mousex >= stockcoords[0] and mousex <= stockcoords[0] + stockwh[0]:
                    if mousey >= stockcoords[1] and mousey <= stockcoords[1] + stockwh[1]:
                        picked_stocks.remove(selected)
                        picked_stocks.insert(i, draggedstock.name)
            return picked_stocks

                            
        if len(self.picked_stocks) < len(stocklist):
            newlist = [stock for stock in stocklist if stock.name not in self.picked_stocks]
            mousex, mousey = pygame.mouse.get_pos()
            width = 1400 / len(newlist)

            if self.dragstock[0] == None:# if the stock is not being dragged
                if pygame.mouse.get_pressed()[0]:# if the mouse is being pressed
                    for i, stock in enumerate(newlist):# for each stock in the list of stocks
                        x = int(200 + (i * width))
                        y = 10
                        # if pygame.Rect(x + 5, y + 10, 1400 / len(newlist), 80).collidepoint(mousex, mousey):
                        #     self.dragstock = [stock, mousex - x, mousey - y]
                        if mousex >= x and x+width >= mousex:
                            if mousey > y and mousey <= y+80:
                                self.dragstock = [stock, mousex - x, mousey - y]
            else:                
                if not pygame.mouse.get_pressed()[0]:# if the mouse is not being pressed
                    # coords = (mousex - self.dragstock[1], mousey - self.dragstock[2])
                    # wh = (int(width), 80)
                    self.picked_stocks = stockOver(mousex, mousey, self.picked_stocks, self.dragstock[0])
                    self.dragstock = [None, None, None]

            for i, stock in enumerate(newlist):
                if self.dragstock[0] == stock:
                    x = mousex - self.dragstock[1]
                    y = mousey - self.dragstock[2]
                else:
                    x = int(200 + (i * width))
                    y = 10
                stock.baredraw(screen, (x + 5, y), (int(width), 80), self.masterrange if self.masterrange != 'Custom' else '1H')

                pchange = round(((stock.graphs[stock.graphrange][-1] / stock.graphs[stock.graphrange][0]) - 1) * 100, 2)
                color = (0, 200, 0) if pchange >= 0 else (200, 0, 0)
                if pchange == 0:
                    color = (180, 180, 180)
                # nametext = fontlist[25].render(stock.name, color)[0]
                nametext = self.renderedstocknames[stock.name]
                screen.blit(nametext, (x + int(width / 2) - nametext.get_width() / 2, y + 10))

    def masterControls(self,screen,mousebuttons:int,stocklist:list):
        mousex,mousey = pygame.mouse.get_pos()

        for i,text in enumerate(["1H","1D","1W","1M","3M","1Y","Custom"]): 
            width = 150    
            height = 60
            x = 1620
            y = 100+(i*height)
                    
            color = (30,30,30) if text != self.masterrange else (140,0,0)
            gfxdraw.filled_polygon(screen,[(x-10,y+55),(x-10,y+5),(x+width,y+5),(x+width,y+55)],color)# polygon behind the text (the graph range)
            pygame.draw.polygon(screen,(0,0,0),[(x-10,y+55),(x-10,y+5),(x+width,y+5),(x+width,y+55)],4)# outline
            trender = s_render(text,45,(220,220,220))
            screen.blit(trender,(x+((width-trender.get_width())//2),(y+trender.get_height()//2)))

            if pygame.Rect(x-10,y+10,width,height).collidepoint(mousex,mousey):
                if mousebuttons == 1:
                    mousebuttons = 0
                    self.masterrange = text
                    if self.masterrange != 'Custom':
                        for stock in stocklist:
                            stock.graphrange = self.masterrange


    def draw_graphs(self, screen, stocklist:list, player, mousebuttons, gametime):
        self.draw_ui(screen,mousebuttons,stocklist)
        
        
        for i in range(self.graph_config[self.current_config][1]):# for each row
            for ii in range(self.graph_config[self.current_config][0]):# for each column
                xlength = int(self.wh[0]/self.graph_config[self.current_config][0])# the length of the x axis
                ylength = int(self.wh[1]/self.graph_config[self.current_config][1])# the length of the y axis
                # print(xlength,ylength,'xlength,ylength')
                
                # startpos = ((ii+1)*xlength+200,i*ylength+100)
                # endpos = (ii*xlength+200,(i+1)*ylength+100)    
                coords = (ii*xlength+200,i*ylength+100)  
                wh = (((ii+1)*xlength)-(ii*xlength),((i+1)*ylength)-(i*ylength))          

                stockname = self.picked_stocks[(i*self.graph_config[self.current_config][0])+ii]

                stock = [stock for stock in stocklist if stock.name == stockname][0]
                # if not [obj.name for obj in stocklist][stockbook.selectedstock] == stockname or not stockbook.menudrawn:#make sure the stock isn't being drawn on the buy sell page
                #     stock.update(screen,play_pause,player,startpos,endpos,drawn=not menudrawn)

                stock.draw(screen,player,coords,wh,mousebuttons,gametime,rangecontroldisp=(True if self.masterrange == 'Custom' else False))
                    
                # if self.current_config != 'nona':#if no menus are drawn and the current config is not nona
                #     self.changestockbutton(screen,startpos,endpos,mousebuttons,stockname,stocklist)#  ------------------------Used for changing stocks, don't want right now
        self.stockBar(screen,stocklist)
        self.masterControls(screen,mousebuttons,stocklist)
                
