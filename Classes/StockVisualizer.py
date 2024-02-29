from Classes.imports.Graph import Graph
from Classes.Gametime import GameTime
from Defs import *
from datetime import datetime,timedelta

POINTSPERGRAPH = 200
class StockVisualizer:
    """Stocks will inherit this class and use the methods to draw the stock to the screen"""
    def __init__(self,gametime,stockobj):
        self.gametime : GameTime = gametime
        self.graph : Graph = Graph()
        self.stockObj = stockobj
    
    def calculateTime(self,graphrange,mousepoint:int):
        graphed_seconds = mousepoint*(self.stockObj.graphrangeoptions[graphrange]/POINTSPERGRAPH)# the amount of seconds that the stock has been graphed
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

    def priceMouseOver(self,screen:pygame.Surface,graphpoints,spacing,coords,wh,graphrange):
        """Displays the price of the stock where the mouse is hovering"""
        mousex,mousey = pygame.mouse.get_pos()
        if pygame.Rect(coords[0],coords[1],(coords[0]+wh[0]-coords[0]),(coords[1]+wh[1]-coords[1])).collidepoint(mousex,mousey):
            pos = (mousex-coords[0])//spacing
            if pos < len(self.stockObj.graphs[graphrange]):
                valuetext = s_render(f'${self.stockObj.graphs[graphrange][int(pos)]:,.2f}',30,(255,255,255))# the value of the stock
                screen.blit(valuetext,(mousex,graphpoints[int(pos)]-valuetext.get_height()-5))# the value of the stock

                mousepoint = (len(self.stockObj.graphs[graphrange])-pos)# the amount of points from the mouse to the end of the graph (just the index of the point in the graph list)

                time_offset = self.calculateTime(graphrange,mousepoint)# gets the time of the stock where the mouse is hovering

                text2 = s_render(f'{time_offset.strftime("%m/%d/%Y %I:%M %p")}',30,(255,255,255))# renders the cursor time
                screen.blit(text2,(mousex,graphpoints[int(pos)]))# blits the cursor time to the screen

                percentchange = self.stockObj.getPercent(graphrange)
                color = percent3choices((0,205,0),(205,0,0),(205,205,205),percentchange)

                screen.blit(s_render(f'{limit_digits(percentchange,15)}%',30,color),(mousex,graphpoints[int(pos)]+valuetext.get_height()+5))# the percent change of the stock
                blnkspacey = (coords[1]+wh[1]-coords[1])//10
                gfxdraw.line(screen,mousex,coords[1]+wh[1]-blnkspacey,mousex,coords[1],(255,255,255))
    
    def drawPriceLines(self,screen,graphrange,coords,wh,graphingpoints):
        """Draws the lines that go across the graph marking the 25, 50, 75, and 100 percent points of the graphed values"""
        blnkspacex = ((coords[0]+wh[0]-coords[0])//10)# Giving blankspace for the graph
        sortedlist = self.stockObj.graphs[graphrange].copy()# makes a copy of the list
        sortedlist.sort()# Sort the list
        for i in range(4):
            lenpos = int((len(self.stockObj.graphs[graphrange])-1)*(i/3))#Position based purely on the length of the current graph size
            point = sortedlist[lenpos]#using the sorted list so an even amount of price values are displayed
            
            #gets the position of the point in the graphingpoints (the y values) - the sorted list moves the points around so the index of the point is different
            yvalpos = np.where(self.stockObj.graphs[graphrange] == point)[0][0]

            text = s_render(str(limit_digits(point,13)), 30, (255,255,255))
            gfxdraw.line(screen,coords[0]+5,int(graphingpoints[yvalpos]),coords[0]+wh[0]-blnkspacex-5,int(graphingpoints[yvalpos]),(150,150,150))
            screen.blit(text,(coords[0]+wh[0]-blnkspacex-text.get_width()-10,(graphingpoints[yvalpos]-text.get_height())))

    def _defaultDraw(self,screen:pygame.Surface,coords,wh,graphrange):
        """Draws the basic elements of the stock to the screen, Shouldn't really be called directly"""
        backcolor = percent3choices((55,0,0),(0,55,0),(55,55,55),self.stockObj.getPercent(graphrange))
        # draws the background color for the just graph
        gfxdraw.filled_polygon(screen, [(coords[0], coords[1]), (coords[0],coords[1]+wh[1]), (coords[0]+wh[0], coords[1]+wh[1]), (coords[0]+wh[0],coords[1])],backcolor)
        
        self.graph.setPoints(self.stockObj.graphs[graphrange])# set the list of points
        color = percent3choices((30,0,0),(0,30,0),(30,30,30),self.stockObj.getPercent(graphrange))
        graphheight = (coords[1]+wh[1]-coords[1])
        graphwidth = (coords[0]+wh[0]-coords[0])

        graphingpoints,spacing,minmax_same = self.graph.draw_graph(screen,(coords[0],coords[1]),(graphwidth,graphheight),color)# graph the points and get needed values
        
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(coords[0],coords[1],graphwidth,graphheight), 5)

        return graphingpoints,spacing,minmax_same
    
    def drawBare(self,screen:pygame.Surface,coords,wh,graphrange,detectmouseover:bool,preset):
        """Draws the basic graph of the stock to the screen"""
        graphingpoints,spacing,minmax_same = self._defaultDraw(screen,coords,wh,graphrange)

        if detectmouseover:
            self.priceMouseOver(screen,graphingpoints,spacing,coords,wh,graphrange)

        return self.drawNamePreset(screen,coords,wh,graphrange,preset)

    
    def drawFull(self,screen:pygame.Surface,coords,wh,graphrange,detectmouseover:bool,preset):
        """Draws the full graph of the stock to the screen"""
        backcolor = percent3choices((55,0,0),(0,55,0),(55,55,55),self.stockObj.getPercent(graphrange))

        gfxdraw.filled_polygon(screen, [(coords[0], coords[1]), (coords[0],coords[1]+wh[1]), (coords[0]+wh[0], coords[1]+wh[1]), (coords[0]+wh[0],coords[1])],backcolor) # draws the background for the whole stock display
        
        blnkspacex = ((coords[0]+wh[0]-coords[0])//10)# Giving blankspace for the graph
        blnkspacey = ((coords[1]+wh[1]-coords[1])//10)

        graphwh = (wh[0]-blnkspacex,wh[1]-blnkspacey)# Giving blankspace for the graph

        graphingpoints,spacing,minmax_same = self._defaultDraw(screen,coords,graphwh,graphrange)# draw the basic graph

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(coords[0], coords[1], (coords[0]+wh[0] - coords[0]),(coords[1]+wh[1] - coords[1])), 5)# outline of the whole display
        
        if not minmax_same:# if the min and max are not the same, Otherwise the graph is a straight line
            self.drawPriceLines(screen,graphrange,coords,wh,graphingpoints)# draw the price lines

        if detectmouseover:
            self.priceMouseOver(screen,graphingpoints,spacing,coords,graphwh,graphrange)# display the price of the stock where the mouse is hovering
        
        return self.drawNamePreset(screen,coords,wh,graphrange,preset)# draw the name of the stock based on the preset

    def drawNamePreset(self,screen:pygame.Surface,coords,wh,graphrange,preset) -> bool:
        """Takes a preset and draws the name, percent change and price of the stock based on the preset"""
        # Setting variables that are used in all presets
        percent = self.stockObj.getPercent(graphrange)
        percentColor = percent3choices((175,0,0),(0,175,0),(175,175,175),percent)
        change_text = percent3choices(f'{percent:.2f}%',f'+{percent:.2f}%',f'{percent:.2f}%',percent)
        conditional = False# can be used for multiple things, (used for if the mouse is over the name of the stock in one of the presets)

        match preset:
            case "Normal":#no special things, just drawing the name and percent change
                pricetext = s_render(f"${limit_digits(self.stockObj.price,15)}", 45 if 45 > int((coords[1]+wh[1]-coords[1])/12.5) else int((coords[1]+wh[1]-coords[1])/12.5), (200,200,200))
                pricex = coords[0]+10; pricey = coords[1]+wh[1]-pricetext.get_height()-15# the x and y position of the price text
                change_text_rendered = s_render(change_text, 40, percentColor)# rendering the percent change         
                nametext = s_render(f"{self.stockObj.name}",50,self.stockObj.color)# rendering the name of the stock

            case "hoverName":# if the mouse is over the name of the stock, change the color of the name and return True
                nametext = s_render(f"{self.stockObj.name}",50,self.stockObj.color)#first render it like normal

                if pygame.Rect(coords[0]+10,coords[1]+10,nametext.get_width(),nametext.get_height()).collidepoint(pygame.mouse.get_pos()):#if the mouse is over the name of the stock
                    nametext = s_render(f"{self.stockObj.name}",50,(230,230,230))# change the color of the name
                    conditional = True  

                pricetext = s_render(f"${limit_digits(self.stockObj.price,15)}", 45 if 45 > int((coords[1]+wh[1]-coords[1])/12.5) else int((coords[1]+wh[1]-coords[1])/12.5), (200,200,200))
                pricex = coords[0]+10; pricey = coords[1]+wh[1]-pricetext.get_height()-15# the x and y position of the price text
                change_text_rendered = s_render(change_text, 40, percentColor)# rendering the percent change         
            case "None":
                return False
        # blitting the text to the screen
        screen.blit(pricetext,(pricex,pricey))# draws the price
        screen.blit(change_text_rendered, (coords[0]+10, coords[1]+50))# draws the percent change
        screen.blit(nametext,(coords[0]+10,coords[1]+10))#draws the name of the stock
        return conditional