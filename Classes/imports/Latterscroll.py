from Defs import *
import pygame,pygame.gfxdraw
from collections import deque

class LatterScroll():
    def __init__(self,polysdisplayed=5):
        self.texts = []# list of dicts, each dict is {(x,y):text}, each is for a different polygon
        self.totalwidth = []# the total width of the box, each item is a int for each polygon
        self.scrollvalue = 0
        # the coords and heights of each polygon drawn in the last call of draw_polys, Not used in this class, but may be used in child classes
        self.coords_height = []
        self.omittedstocks = (0,None)#index of the first and last stock omitted from the latter scroll
        self.updatetexts = 0# used when the texts shouldn't be updated each frame
        self.lasttexts = []# the last texts drawn
        self.lasttextcoords = []# the last textcoords drawn 
        self.textcoords = []

    def decidebottomcolor(self,hover,selected_value,numdrawn,*args):
        """This can be overriden in child classes"""
        return (80,80,80) if hover or numdrawn == selected_value else (50,50,50)
    
    def set_textcoords(self,textcoords):
        """textcoords is a list of lists of tuples, each tuple is y the coords for each text drawn [[(x,y),(x2,y2)]] 
        contains a list for each polygon, each list contains the coords for each text drawn in that polygon
        The furthest text to the left should be the last element in the list"""
        # if textcoords != self.textcoords:
        #     self.updatetexts = 0
        # if self.updatetexts <= 0:
        self.textcoords = textcoords

    def storetextinfo(self,textinfo):
        """textinfo is a list of lists, each list is (text,size,color)"""
        # print([t[0] for t in textinfo] != [t[0] for t in self.texts])
        # for t in textinfo:
        #     print(t,'textinfo')
        # for t in self.texts:
        #     print(t,'self')
        # for t in textinfo:
        #     if t not in self.texts:
        #         print(t,'not in textinfo')
        # print('/'*20)

            
        # if len(textinfo) != len(self.texts):
        if [t[0] for t in textinfo] != [t[0] for t in self.texts]:
            self.updatetexts = 0
        if self.updatetexts <= 0:
            self.texts = textinfo

    def get_textcoord(self,textcoord:list,strtexts,rendertexts) -> list:
        """textcoord is a list of tuples, each tuple is the coords for each text drawn
        strtexts is a list of strings, each string is the text for each text drawn"""
        for i in range(len(textcoord)):
            x,y = textcoord[i]
            if len(rendertexts) < i:break# if only some of the text is on the screen (partially off the screen)

            if type(x) == tuple:# if the x is ('text',offset) it is a variable width
                x = rendertexts[strtexts.index(x[0])].get_width()+x[1]# the width of the text + the offset
            if type(y) == tuple:
                y = rendertexts[strtexts.index(y[0])].get_height()+y[1]
            
            textcoord[i] = (x,y)

        return textcoord
    
    def trim_poly(self,y,polyheight,maxcoords,coords,ndrawn,textcoords,renderedtexts):
        ty = y# top y adjustment - if it is partially off the screen, it will be adjusted
        if y < coords[1]:# if the polygon is partially off the screen
            ty = coords[1]
            for i in range(len(renderedtexts[-1])-1,-1,-1):
                if y+textcoords[ndrawn][i][1] < coords[1]:
                    # renderedtexts[ndrawn].remove(renderedtexts[ndrawn][i])
                    renderedtexts[ndrawn] = renderedtexts[ndrawn][:i] + renderedtexts[ndrawn][i+1:]
                    textcoords[ndrawn].remove(textcoords[ndrawn][i])
                else:
                    textcoords[ndrawn][i] = (textcoords[ndrawn][i][0],textcoords[ndrawn][i][1]-(coords[1]-y))

        by = y# bottom y adjustment - if it is partially off the screen, it will be adjusted
        if y+polyheight > maxcoords[1]:
            by = maxcoords[1]-polyheight
            for i in range(len(renderedtexts[-1])-1,-1,-1):
                if y > maxcoords[1]-polyheight+textcoords[ndrawn][i][1]:
                    # Suppose i is the index of the element you want to remove
                    renderedtexts[ndrawn] = renderedtexts[ndrawn][:i] + renderedtexts[ndrawn][i+1:]
                    # renderedtexts[ndrawn] = renderedtexts[ndrawn][:-1]
                    textcoords[ndrawn].remove(textcoords[ndrawn][i])
                else:
                    textcoords[ndrawn][i] = (textcoords[ndrawn][i][0],textcoords[ndrawn][i][1]-(y+polyheight-maxcoords[1]))

        return ty,by,textcoords,renderedtexts

    def store_rendercoords(self,coords:tuple,maxcoords:tuple,polyheight:tuple,xcoordshift:int,polyshift:int,updatefreq=0) -> None:
        """Stores the coords for the polygons and the texts, and stores the rendered texts"""	
        if self.updatetexts <= 0:# if the texts should be updated
            self.lasttexts = []
            self.updatetexts = updatefreq

        else:# if the texts shouldn't be updated
            self.updatetexts -= 1
        # self.renderedtexts = [t.copy() for t in self.lasttexts]
        self.renderedtexts = self.lasttexts.copy()

        self.polycoords = []
        self.polyheight = polyheight

        x,y = coords[0]+5,0+coords[1]-self.scrollvalue
        ndrawn = 0
        height = polyheight*.9
        maxwidth = 0
        for i,text in enumerate(self.texts):
            if y+polyheight-30 >= coords[1] and y < maxcoords[1]-40:
                if ndrawn == 0:
                    self.omittedstocks = (i,self.omittedstocks[1])
                    self.textcoords = self.textcoords[i:]

                if self.updatetexts == updatefreq:# If it is at zero that means that it got reset because it hit the updatefreq, so the texts need to be updated
                    render = tuple(s_render(info[0],info[1],info[2]) for info in text)
                    self.renderedtexts.append(render)
                    self.lasttexts.append(render)


                self.textcoords[ndrawn] = self.get_textcoord(self.textcoords[ndrawn].copy(),[(t[0]) for t in text],self.renderedtexts[ndrawn])         
                       
                ty,by,self.textcoords,self.renderedtexts = self.trim_poly(y,polyheight,maxcoords,coords,ndrawn,self.textcoords.copy(),self.renderedtexts)

                self.polycoords.append([(x, ty), (x + polyshift, by + height), (x + polyshift + maxcoords[0] -10, by + height), (x + maxcoords[0]-10, ty)])
                
                ndrawn += 1
                x += xcoordshift
            else:# stock isn't being drawn (too high or too low)
                if ndrawn > 0:# Stocks that are too far down to be drawn
                    self.omittedstocks = (self.omittedstocks[0],i)

            y += polyheight  
        return self.omittedstocks[0]+1,self.omittedstocks[0]+ndrawn+1
    
    def get_bottompoints(self,points:list):
         return [
                (points[1][0],points[1][1]),
                (points[1][0]+20,points[1][1]-20),
                (points[2][0],points[2][1]-20),
                (points[2][0],points[2][1]),
                (points[1][0],points[1][1]),]
    
    def scrollcontrols(self, mousebuttons, coords, wh):
        mousex,mousey = pygame.mouse.get_pos()
        svalue = self.scrollvalue# the scroll value before it changes
        if pygame.Rect.collidepoint(pygame.Rect(coords[0],coords[1],wh[0],wh[1]),mousex,mousey):
            if mousebuttons == 4 and self.scrollvalue > 0:
                self.scrollvalue -= 30
            elif mousebuttons == 5 and self.scrollvalue < len(self.texts)*self.polyheight - self.polyheight*2:
                self.scrollvalue += 30
        # checking if the scroll value is out of bounds
        if self.scrollvalue < 0:# if the scroll value is less than 0
            self.scrollvalue = 0
        elif self.scrollvalue > len(self.texts)*self.polyheight - self.polyheight:# if the scroll value is greater than the most it should be
            self.scrollvalue = len(self.texts)*self.polyheight - self.polyheight# set it to the most it should be
        if self.scrollvalue != svalue:# if the scroll value changed
            self.updatetexts = 0# update the texts next frame

    def draw_polys(self,screen,coords,wh,mousebuttons,selected_value,drawbottom,*args):
        """Draws the polygons to the screen, and returns the value of the polygon that is selected"""
        # Selected value is a index

        self.scrollcontrols(mousebuttons,coords,wh)
        for numdrawn,(text_renders,points) in enumerate(zip(self.renderedtexts,self.polycoords)):
            
            # check if the mouse is hovering over the polygon
            if (hover:=point_in_polygon(pygame.mouse.get_pos(),points)):
                if mousebuttons == 1:
                    if numdrawn+self.omittedstocks[0] == selected_value:
                        selected_value = None
                    else:
                        selected_value = numdrawn+self.omittedstocks[0]
                    soundEffects['clickbutton2'].play()
            
            # draw the polygon
            # gfxdraw.filled_polygon(screen, points, (60,60,60,150) if hover or numdrawn == selected_value else (25,25,25,150 ))

            # get bottom coords
            if drawbottom:
                bottom_polygon = self.get_bottompoints(points)
                # draw the bottom of the polygon
                bottomargument = None if len(args) <= numdrawn else args[numdrawn]
                bottomcolor = self.decidebottomcolor(hover,selected_value,numdrawn+self.omittedstocks[0],bottomargument)       
                gfxdraw.filled_polygon(screen,bottom_polygon,bottomcolor)  

             # draw all the texts for each polygon
            for i,render in enumerate(text_renders):
                # self.get_textcoord(self.textcoords[i],points[0],self.texts[numdrawn])
                screen.blit(render,(points[0][0]+self.textcoords[numdrawn][i][0],points[0][1]+self.textcoords[numdrawn][i][1]))
            pygame.draw.polygon(screen, (0, 0, 1), points, 5)
        # screen.blit(self.surf,coords)
        return selected_value
    

class PortfolioLatter(LatterScroll):
    def __init__(self, polysdisplayed=5):
        super().__init__(polysdisplayed)
    
    def draw_stockgraph(self,screen,stocks):

        for i,stock in enumerate(stocks):
            
            x,y,height = self.coords_height[i]
            addedx = self.texts[i][list(self.texts[i])[0]].get_width()+45
            stock[0].baredraw(screen, (x+130+addedx, y), (x+addedx, y+height-9), '1D')

    def decidebottomcolor(self,hover,selected_value,numdrawn,percent):
        percentchange = percent

        bright,dull = 175,100
        if hover or selected_value == numdrawn:
            if percentchange > 0:bottomcolor = (0, bright, 0)
            elif percentchange == 0:bottomcolor = (bright, bright, bright)
            else:bottomcolor = (bright, 0, 0)
        else:
            if percentchange > 0: bottomcolor = (0, dull, 0)
            elif percentchange == 0: bottomcolor = (dull, dull, dull)
            else: bottomcolor = (dull, 0, 0)
        return bottomcolor
            