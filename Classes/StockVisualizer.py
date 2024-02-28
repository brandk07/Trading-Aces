from Classes.Stock import Stock,POINTSPERGRAPH
from Classes.imports.Graph import Graph
from Classes.Gametime import GameTime
from Defs import *
from datetime import datetime,timedelta

class StockVisualizer:
    def __init__(self,gametime):
        self.gametime : GameTime = gametime
        self.graph : Graph = Graph()
    
    def calculateTime(self,stock:Stock,graphrange,mousepoint:int):
        graphed_seconds = mousepoint*(stock.graphrangeoptions[graphrange]/POINTSPERGRAPH)# the amount of seconds that the stock has been graphed
        grapheddays = graphed_seconds//stock.graphrangeoptions["1D"]# the amount of days that the stock has been graphed
        seconds = graphed_seconds%stock.graphrangeoptions["1D"]# the amount of seconds that the stock has been graphed
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

    def priceMouseOver(self,screen:pygame.Surface,graphpoints,spacing,coords,wh,stock:Stock,graphrange):
        """Displays the price of the stock where the mouse is hovering"""
        mousex,mousey = pygame.mouse.get_pos()
        if pygame.Rect(coords[0],coords[1],(coords[0]+wh[0]-coords[0]),(coords[1]+wh[1]-coords[1])).collidepoint(mousex,mousey):
            pos = (mousex-coords[0])//spacing
            if pos < len(stock.graphs[graphrange]):
                valuetext = s_render(f'${stock.graphs[graphrange][int(pos)]:,.2f}',30,(255,255,255))# the value of the stock
                screen.blit(valuetext,(mousex,graphpoints[int(pos)]-valuetext.get_height()-5))# the value of the stock

                mousepoint = (len(stock.graphs[graphrange])-pos)# the amount of points from the mouse to the end of the graph (just the index of the point in the graph list)

                time_offset = self.calculateTime(stock,graphrange,mousepoint)# gets the time of the stock where the mouse is hovering

                text2 = s_render(f'{time_offset.strftime("%m/%d/%Y %I:%M %p")}',30,(255,255,255))# renders the cursor time
                screen.blit(text2,(mousex,graphpoints[int(pos)]))# blits the cursor time to the screen

                percentchange = stock.getPercent(graphrange)
                color = percentColor((0,205,0),(205,0,0),(205,205,205),percentchange)

                screen.blit(s_render(f'{limit_digits(percentchange,15)}%',30,color),(mousex,graphpoints[int(pos)]+valuetext.get_height()+5))# the percent change of the stock
                blnkspacey = (coords[1]+wh[1]-coords[1])//10
                gfxdraw.line(screen,mousex,coords[1]+wh[1]-blnkspacey,mousex,coords[1],(255,255,255))
    def drawPriceLines(screen,stock:Stock,graphrange,coords,wh,graphingpoints):
        """Draws the lines that go across the graph marking the 25, 50, 75, and 100 percent points of the graphed values"""
        blnkspacex = ((coords[0]+wh[0]-coords[0])//10)# Giving blankspace for the graph
        sortedlist = stock.graphs[graphrange].copy()# makes a copy of the list
        sortedlist.sort()# Sort the list
        for i in range(4):
            lenpos = int((len(stock.graphs[graphrange])-1)*(i/3))#Position based purely on the length of the current graph size
            point = sortedlist[lenpos]#using the sorted list so an even amount of price values are displayed
            
            #gets the position of the point in the graphingpoints (the y values) - the sorted list moves the points around so the index of the point is different
            yvalpos = np.where(stock.graphs[graphrange] == point)[0][0]

            text = s_render(str(limit_digits(point,13)), 30, (255,255,255))
            gfxdraw.line(screen,coords[0]+5,int(graphingpoints[yvalpos]),coords[0]+wh[0]-blnkspacex-5,int(graphingpoints[yvalpos]),(150,150,150))
            screen.blit(text,(coords[0]+wh[0]-blnkspacex-text.get_width()-10,(graphingpoints[yvalpos]-text.get_height())))

    def defaultDraw(self,screen:pygame.Surface,stock:Stock,coords,wh,graphrange):
        """Draws the basic elements of the stock to the screen"""
        backcolor = percentColor((55,0,0),(0,55,0),(55,55,55),stock.getPercent(graphrange))
        gfxdraw.filled_polygon(screen, [(coords[0], coords[1]), (coords[0],coords[1]+wh[1]), (coords[0]+wh[0], coords[1]+wh[1]), (coords[0]+wh[0],coords[1])],backcolor)
        
        color = self.graph.setPoints(stock.graphs[graphrange])# set the list of points
        percentColor((30,0,0),(0,30,0),(30,30,30),stock.getPercent(graphrange))
        graphheight = (coords[1]+wh[1]-coords[1])
        graphwidth = (coords[0]+wh[0]-coords[0])

        graphingpoints,spacing,minmax_same = self.graph.draw_graph(screen,(coords[0],coords[1]),(graphwidth,graphheight),color)# graph the points and get needed values
        
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(coords[0],coords[1],graphwidth,graphheight), 5)

        return graphingpoints,spacing,minmax_same
    
    def drawBare(self,screen:pygame.Surface,stock:Stock,coords,wh,graphrange,mouseover):
        graphingpoints,spacing,minmax_same = self.defaultDraw(screen,stock,coords,wh,graphrange)

        if mouseover:
            self.priceMouseOver(screen,graphingpoints,spacing,coords,wh,stock,graphrange)

    
    def drawFull(self,screen:pygame.Surface,stock:Stock,coords,wh,graphrange,mouseover):
        """Draws the full graph of the stock to the screen"""
        backcolor = percentColor((55,0,0),(0,55,0),(55,55,55),stock.getPercent(graphrange))

        gfxdraw.filled_polygon(screen, [(coords[0], coords[1]), (coords[0],coords[1]+wh[1]), (coords[0]+wh[0], coords[1]+wh[1]), (coords[0]+wh[0],coords[1])],backcolor) # draws the perimeter around graphed values
        
        blnkspacex = ((coords[0]+wh[0]-coords[0])//10)# Giving blankspace for the graph
        blnkspacey = ((coords[1]+wh[1]-coords[1])//10)

        graphwh = (wh[0]-blnkspacex,wh[1]-blnkspacey)# Giving blankspace for the graph

        graphingpoints,spacing,minmax_same = self.defaultDraw(screen,stock,coords,graphwh,graphrange)# draw the basic graph

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(coords[0], coords[1], (coords[0]+wh[0] - coords[0]),(coords[1]+wh[1] - coords[1])), 5)# outline of the whole display
        
        if not minmax_same:# if the min and max are not the same, Otherwise the graph is a straight line
            self.drawPriceLines(screen,stock,graphrange,coords,wh,graphingpoints)# draw the price lines

        
        if mouseover:
            self.priceMouseOver(screen,graphingpoints,spacing,coords,graphwh,stock,graphrange)