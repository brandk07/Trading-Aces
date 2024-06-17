from Classes.imports.Graph import Graph
from Classes.Gametime import GameTime
from Defs import *
from datetime import datetime,timedelta

POINTSPERGRAPH = 200
class StockVisualizer:
    """Anytime a Stock needs to be drawn to screen an instance of this class can be used,
    should be used for one specific graph on the screen, can switch stock classes and has multiple drawing options"""
    def __init__(self,gametime,stockobj,stocklist):
        self.gametime : GameTime = gametime
        self.graph : Graph = Graph()
        self.stockObj = stockobj#stock object it will start with
        self.storedRanges = {}# all the ranges that different places need, different key for each range
        self.stocklist = stocklist

        # Used since when calling a draw function you can give a key rather than a graphrange and then that key will be stored in this class
        # if a parameter is truegraphrange then it has used the getVaildRange function to get the true graphrange
        self.getValidRange = lambda graphrange: graphrange if graphrange in GRAPHRANGES else self.storedRanges.setdefault(graphrange,"1D")
    def setStockObj(self,stockobj):
        """Changes the stock object that the visualizer is using"""
        self.stockObj = stockobj
    def calculateTime(self,truegraphrange,mousepoint:int):
        graphed_seconds = mousepoint*(self.stockObj.graphrangeoptions[truegraphrange]/POINTSPERGRAPH)# the amount of seconds that the stock has been graphed
        grapheddays = graphed_seconds//self.stockObj.graphrangeoptions["1D"]# the amount of days that the stock has been graphed
        seconds = graphed_seconds % self.stockObj.graphrangeoptions["1D"]# the amount of seconds that the stock has been graphed
        time_offset = self.gametime.time#time offset
        if self.gametime.isOpen(time_offset)[0] == False:
            time_offset = time_offset.replace(hour=15,minute=59,second=0)# set the time to 3:59 PM
        dayscount = 0

        while dayscount < grapheddays:# while the days count is less than the amount of days that the stock has been graphed
            time_offset -= timedelta(days=1)# add a day to the time offset
            if self.gametime.isOpen(time_offset)[0]:# if that is a day that was open for trading
                dayscount += 1# add 1 to the days count

        secondsleft = (time_offset - time_offset.replace(hour=9,minute=30,second=0)).seconds# the amount of seconds left in the day
        if seconds > secondsleft:# if the amount of seconds needed to minus is greater than the seconds left in the day
            seconds -= secondsleft
            time_offset -= timedelta(days=1)# add a day to the time offset
            while self.gametime.isOpen(time_offset)[0] == False:
                time_offset -= timedelta(days=1)
            
            time_offset = time_offset.replace(hour=15,minute=59,second=0)# set the time to 3:59 PM
            
        time_offset -= timedelta(seconds=seconds)# add a day to the time offset
        return time_offset

    def priceMouseOver(self,screen:pygame.Surface,graphpoints,spacing,coords,wh,truegraphrange):
        """Displays the price of the stock where the mouse is hovering"""
        mousex,mousey = pygame.mouse.get_pos()

        if pygame.Rect(coords[0],coords[1],(coords[0]+wh[0]-coords[0]),(coords[1]+wh[1]-coords[1])).collidepoint(mousex,mousey):

            pos = (mousex-coords[0])//spacing
            if pos < len(self.stockObj.graphs[truegraphrange]):
                valuetext = s_render(f'${self.stockObj.graphs[truegraphrange][int(pos)]:,.2f}',30,(255,255,255))# the value of the stock
                screen.blit(valuetext,(mousex,graphpoints[int(pos)]-valuetext.get_height()-5))# the value of the stock

                mousepoint = (len(self.stockObj.graphs[truegraphrange])-pos)# the amount of points from the mouse to the end of the graph (just the index of the point in the graph list)

                time_offset = self.calculateTime(truegraphrange,mousepoint)# gets the time of the stock where the mouse is hovering

                text2 = s_render(f'{time_offset.strftime("%m/%d/%Y %I:%M %p")}',30,(255,255,255))# renders the cursor time
                screen.blit(text2,(mousex,graphpoints[int(pos)]))# blits the cursor time to the screen

                # percentchange = self.stockObj.getPercent(truegraphrange)
                percentchange = round(((self.stockObj.graphs[truegraphrange][int(pos)]/self.stockObj.graphs[truegraphrange][0])-1)*100,2)
                color = p3choice((200,0,0),(0,200,0),(200,200,200),percentchange)

                screen.blit(s_render(f'{limit_digits(percentchange,15)}%',30,color),(mousex,graphpoints[int(pos)]+valuetext.get_height()+5))# the percent change of the stock
                blnkspacey = (coords[1]+wh[1]-coords[1])//10
                gfxdraw.line(screen,mousex,coords[1]+wh[1]-blnkspacey,mousex,coords[1],(255,255,255))
    
    def drawPriceLines(self,screen,truegraphrange,coords,wh,graphingpoints):
        """Draws the lines that go across the graph marking the 25, 50, 75, and 100 percent points of the graphed values"""
        blnkspacex = ((coords[0]+wh[0]-coords[0])//10)# Giving blankspace for the graph
        sortedlist = self.stockObj.graphs[truegraphrange].copy()# makes a copy of the list
        sortedlist.sort()# Sort the list
        for i in range(4):
            lenpos = int((len(self.stockObj.graphs[truegraphrange])-1)*(i/3))#Position based purely on the length of the current graph size
            point = sortedlist[lenpos]#using the sorted list so an even amount of price values are displayed
            
            #gets the position of the point in the graphingpoints (the y values) - the sorted list moves the points around so the index of the point is different
            yvalpos = np.where(self.stockObj.graphs[truegraphrange] == point)[0][0]

            text = s_render(str(limit_digits(point,13)), 30, (255,255,255))
            gfxdraw.line(screen,coords[0]+5,int(graphingpoints[yvalpos]),coords[0]+wh[0]-blnkspacex-5,int(graphingpoints[yvalpos]),(150,150,150))
            screen.blit(text,(coords[0]+wh[0]-blnkspacex-text.get_width()-10,(graphingpoints[yvalpos]-text.get_height())))

    def drawRangeControls(self,screen:pygame.Surface,coords,wh,graphrange):
        """Draws the range controls for the stock to the screen
        needs the inputed graphrange, not the valid graphrange,"""	
        blnkspacex = ((coords[0]+wh[0]-coords[0])//10)
        blnkspacey = ((coords[1]+wh[1]-coords[1])//10)
        drawingy = (wh[1])/len(GRAPHRANGES)

        # size = int(-85*math.log10(wh[0]))+255
        
        size = int(-80*math.log10((1450-wh[0])))+275
        for i,txt in enumerate(GRAPHRANGES):
            
            if txt == self.getValidRange(graphrange):
                color = (255,255,255)
            else:
                color = (100,100,100)
            text = s_render(txt, size, color)
            centeredx = blnkspacex//2-text.get_width()//2
            screen.blit(text,(coords[0]+wh[0]+centeredx,coords[1]+10+(i*drawingy)))
            # collionsion
            extraheight = text.get_height()+15
            if pygame.Rect(coords[0]+wh[0],coords[1]+(i*drawingy),blnkspacex,extraheight).collidepoint(pygame.mouse.get_pos()):
                points = [(coords[0]+wh[0],coords[1]+(i*drawingy)), (coords[0]+wh[0],coords[1]+(i*drawingy)+extraheight), (coords[0]+wh[0]+blnkspacex, coords[1]+(i*drawingy)+extraheight), (coords[0]+wh[0]+blnkspacex,coords[1]+(i*drawingy))]
                gfxdraw.filled_polygon(screen, points,(100,100,100,150))
                if pygame.mouse.get_pressed()[0]:
                    self.storedRanges[graphrange] = txt
          

    def _defaultDraw(self,screen:pygame.Surface,coords,wh,graphrange,customRange):
        """Draws the basic elements of the stock to the screen, Shouldn't really be called directly"""
        truegraphrange = self.getValidRange(graphrange)
        backcolor = p3choice((55,0,0),(0,55,0),(55,55,55),self.stockObj.getPercent(truegraphrange))
        # draws the background color for the just graph
        gfxdraw.filled_polygon(screen, [(coords[0], coords[1]), (coords[0],coords[1]+wh[1]), (coords[0]+wh[0], coords[1]+wh[1]), (coords[0]+wh[0],coords[1])],backcolor)
        
        self.graph.setPoints(self.stockObj.graphs[truegraphrange])# set the list of points
        color = p3choice((30,0,0),(0,30,0),(30,30,30),self.stockObj.getPercent(truegraphrange))
        graphheight = (coords[1]+wh[1]-coords[1])
        graphwidth = (coords[0]+wh[0]-coords[0])

        graphingpoints,spacing,minmax_same = self.graph.draw_graph(screen,(coords[0],coords[1]),(graphwidth,graphheight),color)# graph the points and get needed values
        
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(coords[0],coords[1],graphwidth,graphheight), 5)
        if customRange:
            self.drawRangeControls(screen,coords,wh,graphrange)
        return graphingpoints,spacing,minmax_same
    

    def drawBare(self,screen:pygame.Surface,coords,wh,graphrange,detectmouseover:bool,preset):
        """Draws the basic graph of the stock to the screen,
        Graphrange can be a valid range or it will be used as a key in a dict to store the range"""
        truegraphrange = self.getValidRange(graphrange)
        graphingpoints,spacing,minmax_same = self._defaultDraw(screen,coords,wh,graphrange,False)# draw the basic graph, no range controls

        if detectmouseover:
            self.priceMouseOver(screen,graphingpoints,spacing,coords,wh,truegraphrange)

        # return self.drawNamePreset(screen,coords,wh,truegraphrange,preset)
    
    def drawFull(self,screen:pygame.Surface,coords,wh,graphrange,detectmouseover:bool,preset,customRange=True):
        """Draws the full graph of the stock to the screen, 
        Graphrange can be a valid range or it will be used as a key in a dict to store the range"""
        truegraphrange = self.getValidRange(graphrange)
        backcolor = p3choice((55,0,0),(0,55,0),(55,55,55),self.stockObj.getPercent(truegraphrange))

        gfxdraw.filled_polygon(screen, [(coords[0], coords[1]), (coords[0],coords[1]+wh[1]), (coords[0]+wh[0], coords[1]+wh[1]), (coords[0]+wh[0],coords[1])],backcolor) # draws the background for the whole stock display
        
        blnkspacex = ((coords[0]+wh[0]-coords[0])//10)# Giving blankspace for the graph
        blnkspacey = ((coords[1]+wh[1]-coords[1])//10)

        graphwh = (wh[0]-blnkspacex,wh[1]-blnkspacey)# Giving blankspace for the graph

        graphingpoints,spacing,minmax_same = self._defaultDraw(screen,coords,graphwh,graphrange,customRange)# draw the basic graph

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(coords[0], coords[1], (coords[0]+wh[0] - coords[0]),(coords[1]+wh[1] - coords[1])), 5)# outline of the whole display
        
        if not minmax_same:# if the min and max are not the same, Otherwise the graph is a straight line
            self.drawPriceLines(screen,truegraphrange,coords,wh,graphingpoints)# draw the price lines

        if detectmouseover:
            self.priceMouseOver(screen,graphingpoints,spacing,coords,graphwh,truegraphrange)# display the price of the stock where the mouse is hovering
        
  
        self.drawNamePreset(screen,coords,wh,truegraphrange,preset)# draw the name of the stock based on the preset

    def swapGraph(self,screen,coords,wh):
        
        for i,stock in enumerate([s for s in self.stocklist if s != self.stockObj]):
            pygame.draw.rect(screen,(200,200,200),pygame.Rect(coords[0],coords[1],50,25))
            name = s_render(f"{stock.name}",30,stock.color)
            screen.blit(name,(coords[0]+10,coords[1]+10+(i*30)))


    def drawNamePreset(self,screen:pygame.Surface,coords,wh,graphrange,preset) -> bool:
        """Takes a preset and draws the name, percent change and price of the stock based on the preset"""
        # Setting variables that are used in all presets
        percent = self.stockObj.getPercent(graphrange)
        percentColor = p3choice((175,0,0),(0,175,0),(175,175,175),percent)
        change_text = p3choice(f'{percent:.2f}%',f'+{percent:.2f}%',f'{percent:.2f}%',percent)
        swappable = False
        if preset in ["hoverName"]:# if it is a preset that allows for the stock to be swapped 
            swappable = True

        pricetext = s_render(f"${limit_digits(self.stockObj.price,15)}", 45 if 45 > int((coords[1]+wh[1]-coords[1])/12.5) else int((coords[1]+wh[1]-coords[1])/12.5), (200,200,200))
        pricex = coords[0]+10; pricey = coords[1]+wh[1]-pricetext.get_height()-15# the x and y position of the price text
        change_text_rendered = s_render(change_text, 40, percentColor)# rendering the percent change         
        nametext = s_render(f"{self.stockObj.name}",50,self.stockObj.color)# rendering the name of the stock

        if swappable and pygame.Rect(coords[0]+10,coords[1]+10,nametext.get_width(),nametext.get_height()).collidepoint(pygame.mouse.get_pos()):#if the mouse is over the name of the stock
            nametext = s_render(f"{self.stockObj.name}",50,(230,230,230))# change the color of the name
            self.swapGraph(screen,coords,wh)
        # match preset:
        #     case "Normal":#no special things, just drawing the name and percent change
                # pricetext = s_render(f"${limit_digits(self.stockObj.price,15)}", 45 if 45 > int((coords[1]+wh[1]-coords[1])/12.5) else int((coords[1]+wh[1]-coords[1])/12.5), (200,200,200))
                # pricex = coords[0]+10; pricey = coords[1]+wh[1]-pricetext.get_height()-15# the x and y position of the price text
                # change_text_rendered = s_render(change_text, 40, percentColor)# rendering the percent change         
                # nametext = s_render(f"{self.stockObj.name}",50,self.stockObj.color)# rendering the name of the stock

        #     case "hoverName":# if the mouse is over the name of the stock, change the color of the name and return True
        #         nametext = s_render(f"{self.stockObj.name}",50,self.stockObj.color)#first render it like normal

                # if pygame.Rect(coords[0]+10,coords[1]+10,nametext.get_width(),nametext.get_height()).collidepoint(pygame.mouse.get_pos()):#if the mouse is over the name of the stock
                #     nametext = s_render(f"{self.stockObj.name}",50,(230,230,230))# change the color of the name

        #         pricetext = s_render(f"${limit_digits(self.stockObj.price,15)}", 45 if 45 > int((coords[1]+wh[1]-coords[1])/12.5) else int((coords[1]+wh[1]-coords[1])/12.5), (200,200,200))
        #         pricex = coords[0]+10; pricey = coords[1]+wh[1]-pricetext.get_height()-15# the x and y position of the price text
        #         change_text_rendered = s_render(change_text, 40, percentColor)# rendering the percent change         
        #     case "None":
        #         return False
        # blitting the text to the screen
        screen.blit(pricetext,(pricex,pricey))# draws the price
        screen.blit(change_text_rendered, (coords[0]+10, coords[1]+50))# draws the percent change
        screen.blit(nametext,(coords[0]+10,coords[1]+10))#draws the name of the stock