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
        self.surf = pygame.Surface((0,0))
        self.omittedstocks = (0,None)#index of the first and last stock omitted from the latter scroll

    def storeTexts(self,extraspace=0,resetlist=False,**kwargs):
        """Kwargs should be 'text:str':(relativex,relativey,fontsize,fontcolor))"""
        """Relative coords are relative to the top left of the box"""
        """This function should be called for each polygon in the latter"""
        if resetlist:# if it is the first time in a new frame
            self.texts = []
            self.totalwidth = []
        
        self.texts.append({(x,y):(text,size,color) for text,(x,y,size,color) in kwargs.items()})
        furthest = max(self.texts[-1].keys(),key=lambda x:x[0])# finding the furthest x value being drawn

        self.totalwidth.append(0)# adding a new item to the list of total widths
        self.totalwidth[-1] = furthest[0]+self.texts[-1][furthest].get_width()+extraspace# adding the width of the furthest text to the total width (used for width of polygon)
        return self.totalwidth, self.texts
    def storeTextsVariable(self,extraspace=0,resetlist=False,**kwargs):
        """Allows for text width to be based on the width of another text"""
        """Kwargs should be 'text:str':((text,x),relativey,fontsize,fontcolor))"""
        # an input could be {'VIXEL':(50,100,fontsize,color),'QWIRE':(('VIXEL',30),y,fontsize,color)}
        # the x value of QWIRE will be the width of VIXEL + 30

        if resetlist:# if it is the first time in a new frame
            self.texts = []
            self.totalwidth = []

        self.texts.append({})
        texts = {text:(text,size,color) for text,(x,y,size,color) in kwargs.items()}# creating a dict of texts for the polygon (text,size,color) which is really easy to use s_render on
        textwidths = {text:texts[text].get_width() for text in texts}# creating a dict of text widths for the polygon

        for text,(x,y,*_) in kwargs.items():# looping through the kwargs (all the texts to be drawn)
            if type(x) == tuple:# if the x value is a tuple, it is a variable width meaning it is based on the width of another text

                x = textwidths[x[0]]+x[1]# the first x value is a string, the second is the offset. They are both added, one from the width of another text
            self.texts[-1][(x,y)] = texts[text]# adding the text to the dict of texts for the polygon
        furthest = max(self.texts[-1].keys(),key=lambda x:x[0])# finding the furthest x value being drawn

        self.totalwidth.append(0)# adding a new item to the list of total widths
        self.totalwidth[-1] = furthest[0]+self.texts[-1][furthest].get_width()+extraspace# adding the width of the furthest text to the total width (used for width of polygon)
        return self.totalwidth, self.texts

    def decidebottomcolor(self,hover,selected_value,numdrawn,*args):
        """This can be overriden in child classes"""
        return (80,80,80) if hover or numdrawn == selected_value else (50,50,50)
    
    def set_textcoords(self,textcoords):
        """textcoords is a list of lists of tuples, each tuple is y the coords for each text drawn [[(x,y),(x2,y2)]] 
        contains a list for each polygon, each list contains the coords for each text drawn in that polygon
        The furthest text to the left should be the last element in the list"""
        self.textcoords = textcoords

    def storetextinfo(self,textinfo):
        """textinfo is a list of lists, each list is (text,size,color)"""
        self.texts = textinfo

    def get_textcoord(self,textcoord:list,strtexts,rendertexts):
        """textcoord is a list of tuples, each tuple is the coords for each text drawn
        strtexts is a list of strings, each string is the text for each text drawn"""
        for i in range(len(textcoord)):
            x,y = textcoord[i]
            if type(x) == tuple:# if the x is ('text',offset) it is a variable width
                x = rendertexts[strtexts.index(x[0])].get_width()+x[1]# the width of the text + the offset
            if type(y) == tuple:
                y = rendertexts[strtexts.index(y[0])].get_height()+y[1]
            
            textcoord[i] = (x,y)

        return textcoord
        
    def store_rendercoords(self,coords:tuple,maxcoords:tuple,polyheight:tuple,xcoordshift:int,polyshift:int):
        
        self.renderedtexts = []
        self.polycoords = []
        self.polyheight = polyheight
        x,y = 0+5,0-self.scrollvalue+5
        ndrawn = 0
        height = polyheight*.9
        maxwidth = 0

        
        for i,text in enumerate(self.texts):
            if y+polyheight >= 0 and y < maxcoords[1]-10:
                # print(i,y,max_y,'i')
                if ndrawn == 0:
                    self.omittedstocks = (i,None)
                    self.textcoords = self.textcoords[i:]
                self.renderedtexts.append([s_render(info[0],info[1],info[2]) for info in text])
                 
                
                # print(self.textcoords,'sdfsdf',ndrawn,'afterndrawn',self.texts)
                self.textcoords[ndrawn] = self.get_textcoord(self.textcoords[ndrawn],[(t[0]) for t in text],self.renderedtexts[-1])      


                self.polycoords.append([(x, y), (x + polyshift, y + height), (x + polyshift + maxcoords[0] -10, y + height), (x + maxcoords[0]-10, y)])
                ndrawn += 1
                x += xcoordshift
            else:# stock isn't being drawn (too high or too low)
                if ndrawn > 0:# Stocks that are too far down to be drawn
                    self.omittedstocks = (self.omittedstocks[0],i)

            y += polyheight
            

        if self.surf.get_size()[1] != maxcoords[1]-coords[1] or self.surf.get_size()[0] != maxcoords[0]:
            self.surf = pygame.Surface((maxcoords[0], maxcoords[1]-coords[1]), pygame.HWSURFACE, 32)
            self.surf.set_colorkey((0,0,0))
        else:
            self.surf.fill((0,0,0))
        

    
    def get_bottompoints(self,points:list):
         return [
                (points[1][0],points[1][1]),
                (points[1][0]+20,points[1][1]-20),
                (points[2][0],points[2][1]-20),
                (points[2][0],points[2][1]),
                (points[1][0],points[1][1]),]
    

    def scrollcontrols(self,mousebuttons):
        if mousebuttons == 4 and self.scrollvalue > 0:
            self.scrollvalue -= 50
        elif mousebuttons == 5 and self.scrollvalue < len(self.polycoords)*self.polyheight-self.polyheight:
            self.scrollvalue += 50

    def draw_polys(self,screen,coords,mousebuttons,selected_value,*args):
        """Draws the polygons to the screen, and returns the value of the polygon that is selected"""
        # Selected value is a index
        self.scrollcontrols(mousebuttons)
        for numdrawn,(text_renders,points) in enumerate(zip(self.renderedtexts,self.polycoords)):
            # draw the polygon
            gfxdraw.filled_polygon(self.surf, points, (30,30,30,180))
            
            # check if the mouse is hovering over the polygon
            if (hover:=point_in_polygon(pygame.mouse.get_pos(),[(point[0]+coords[0],point[1]+coords[1]) for point in points])):
                if mousebuttons == 1:
                    selected_value = numdrawn+self.omittedstocks[0]
                    soundEffects['clickbutton2'].play()
                    
            
            # get bottom coords
            bottom_polygon = self.get_bottompoints(points)
            # draw the bottom of the polygon
            bottomargument = None if len(args) <= numdrawn else args[numdrawn]
            bottomcolor = self.decidebottomcolor(hover,selected_value,numdrawn+self.omittedstocks[0],bottomargument)       
            gfxdraw.filled_polygon(self.surf,bottom_polygon,bottomcolor)  

             # draw all the texts for each polygon
            for i,render in enumerate(text_renders):
                # self.get_textcoord(self.textcoords[i],points[0],self.texts[numdrawn])
                self.surf.blit(render,(points[0][0]+self.textcoords[numdrawn][i][0],points[0][1]+self.textcoords[numdrawn][i][1]))
            pygame.draw.polygon(self.surf, (0, 0, 1), points, 5)
        screen.blit(self.surf,coords)
        return selected_value
    

class PortfolioLatter(LatterScroll):
    def __init__(self, polysdisplayed=5):
        super().__init__(polysdisplayed)
    
    def draw_stockgraph(self,screen,stocks):

        for i,stock in enumerate(stocks):
            
            x,y,height = self.coords_height[i]
            addedx = self.texts[i][list(self.texts[i])[0]].get_width()+45
            stock[0].baredraw(screen, (x+130+addedx, y), (x+addedx, y+height-9), '1D')

    def decidebottomcolor(self,hover,selected_value,numdrawn,stock):
        percentchange = ((stock[0].price - stock[1]) / stock[1]) * 100

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
            
# from Defs import *
# import pygame,pygame.gfxdraw
# from functools import deque

# class LatterScroll():
#     def __init__(self,polysdisplayed=5):
#         self.texts = []# list of dicts, each dict is {(x,y):text}, each is for a different polygon
#         self.totalwidth = []# the total width of the box, each item is a int for each polygon

#         # the coords and heights of each polygon drawn in the last call of draw_polys, Not used in this class, but may be used in child classes
#         self.coords_height = []
#         self.surf = pygame.Surface((0,0))

#     def storeTexts(self,extraspace=0,resetlist=False,**kwargs):
#         """Kwargs should be 'text:str':(relativex,relativey,fontsize,fontcolor))"""
#         """Relative coords are relative to the top left of the box"""
#         """This function should be called for each polygon in the latter"""
#         if resetlist:# if it is the first time in a new frame
#             self.texts = []
#             self.totalwidth = []
        
#         self.texts.append({(x,y):(text,size,color) for text,(x,y,size,color) in kwargs.items()})
#         furthest = max(self.texts[-1].keys(),key=lambda x:x[0])# finding the furthest x value being drawn

#         self.totalwidth.append(0)# adding a new item to the list of total widths
#         self.totalwidth[-1] = furthest[0]+self.texts[-1][furthest].get_width()+extraspace# adding the width of the furthest text to the total width (used for width of polygon)
#         return self.totalwidth, self.texts
#     def storeTextsVariable(self,extraspace=0,resetlist=False,**kwargs):
#         """Allows for text width to be based on the width of another text"""
#         """Kwargs should be 'text:str':((text,x),relativey,fontsize,fontcolor))"""
#         # an input could be {'VIXEL':(50,100,fontsize,color),'QWIRE':(('VIXEL',30),y,fontsize,color)}
#         # the x value of QWIRE will be the width of VIXEL + 30

#         if resetlist:# if it is the first time in a new frame
#             self.texts = []
#             self.totalwidth = []

#         self.texts.append({})
#         texts = {text:(text,size,color) for text,(x,y,size,color) in kwargs.items()}# creating a dict of texts for the polygon (text,size,color) which is really easy to use s_render on
#         textwidths = {text:texts[text].get_width() for text in texts}# creating a dict of text widths for the polygon

#         for text,(x,y,*_) in kwargs.items():# looping through the kwargs (all the texts to be drawn)
#             if type(x) == tuple:# if the x value is a tuple, it is a variable width meaning it is based on the width of another text

#                 x = textwidths[x[0]]+x[1]# the first x value is a string, the second is the offset. They are both added, one from the width of another text
#             self.texts[-1][(x,y)] = texts[text]# adding the text to the dict of texts for the polygon
#         furthest = max(self.texts[-1].keys(),key=lambda x:x[0])# finding the furthest x value being drawn

#         self.totalwidth.append(0)# adding a new item to the list of total widths
#         self.totalwidth[-1] = furthest[0]+self.texts[-1][furthest].get_width()+extraspace# adding the width of the furthest text to the total width (used for width of polygon)
#         return self.totalwidth, self.texts

#     def decidebottomcolor(self,hover,selected_value,numdrawn,*args):
#         """This can be overriden in child classes"""
#         return ((80,80,80),(200,200,200)) if hover or numdrawn == selected_value else ((50,50,50),(150,150,150))
    
#     def set_textcoords(self,textcoords):
#         """textcoords is a list of lists of tuples, each tuple is y the coords for each text drawn [[(x,y),(x2,y2)]] 
#         contains a list for each polygon, each list contains the coords for each text drawn in that polygon
#         The furthest text to the left should be the last element in the list"""
#         self.textcoords = deque(textcoords)

#     def storetextinfo(self,textinfo):
#         """textinfo is a list of lists, each list is (text,size,color)"""
#         self.texts = textinfo



#     def store_rendercoords(self,max_y:int,polyheight:tuple,scrollvalue:int,xcoordshift:int,polyshift:int,extrawidth:int):
        
#         self.renderedtexts = []
#         self.polycoords = []

#         x,y = 0,0-scrollvalue
#         ndrawn = 0
#         height = polyheight*.8

        
#         for i,text in enumerate(self.texts):
#             if y+polyheight >= 0 and y <= max_y:

#                 self.renderedtexts.append([s_render(info[0],info[1],info[2]) for info in text])

#                 ndrawn += 1
#                 width = self.renderedtexts[-1][-1].get_width()+extrawidth+self.textcoords[-1][0]# the width of the last text drawn + the extra width + the xcoord of the last text drawn

#                 self.polycoords.append([(x, y), (x + polyshift, y + height), (x + 10 + polyshift + width, y + height), (x + 10 + width, y)])

#             else:
#                 self.textcoords.pop(i)

#             y += polyheight; x += xcoordshift

    
#     def get_bottompoints(self,points:list):
#          return [
#                 (points[1][0],points[1][1]),
#                 (points[1][0]+20,points[1][1]-20),
#                 (points[2][0],points[2][1]-20),
#                 (points[2][0],points[2][1]),
#                 (points[1][0],points[1][1]),]
#     def finalcoords(self,coords:list):
        
#     def draw_polys(self,screen,mousebuttons,selected_value,*args):

#         for numdrawn,(text_renders,points) in enumerate(zip(self.renderedtexts,self.polycoords)):
#             # draw the polygon
#             gfxdraw.filled_polygon(screen, points, (30, 30, 30, 150))

#             # draw all the texts for each polygon
#             for i,render in enumerate(text_renders):
#                 screen.blit(render,(points[0][0]+self.textcoords[i][0],points[0][1]+self.textcoords[i][1]))

#             # check if the mouse is hovering over the polygon
#             if (hover:=point_in_polygon(pygame.mouse.get_pos(),points)):
#                 if mousebuttons == 1:
#                     selected_value = numdrawn
#                     soundEffects['clickbutton2'].play()
            
#             # get bottom coords
#             bottom_polygon = self.get_bottompoints(points)
#             # draw the bottom of the polygon
#             bottomcolor = self.decidebottomcolor(hover,selected_value,numdrawn,args[numdrawn])       
#             gfxdraw.filled_polygon(screen,bottom_polygon,bottomcolor)          
    
    # def draw_polys(self,screen:pygame.Surface,coords:tuple,max_y:int,polyheight:tuple,mousebuttons,selected_value,xcoordshift=0,polyshift=0,showbottom=True,*args):
    #     """This function is called once after all the texts have been stored and draws the polygons to the screen
    #     args is a list of arguments that will be passed to decidebottomcolor
    #     xcoordshift is applied to the xcoord of each polygon being iterated, 
    #     polyshift is adjusting the shape of the polygon (rectange->trapezoid)"""
    #     if self.surf.get_size()[1] != max_y or self.surf.get_size()[0] != max(self.totalwidth)+(polyshift*len(self.texts)):
    #         self.surf = pygame.Surface((max(self.totalwidth)+(polyshift*len(self.texts)),max_y),pygame.SRCALPHA)
    #     x,y = 0,0

    #     numdrawn = 0 
    #     self.coords_height = []
    #     while y < max_y-coords[1] and numdrawn < len(self.texts):

    #         if 
            
    #         height = polyheight*.85
    #         self.coords_height.append((x,y,height))
    #         points = [(x, y), (x + polyshift, y + height), (x + 10 + polyshift + self.totalwidth[numdrawn], y + height), (x + 10 + self.totalwidth[numdrawn], y)]
    #         gfxdraw.filled_polygon(screen, points, (30, 30, 30, 150))
            

    #         if (hover:=point_in_polygon(pygame.mouse.get_pos(),points)):
    #             if mousebuttons == 1:
    #                 selected_value = numdrawn
    #                 soundEffects['clickbutton2'].play()

    #         bottom_polygon = [
    #             (points[1][0],points[1][1]),
    #             (points[1][0]+20,points[1][1]-20),
    #             (points[2][0],points[2][1]-20),
    #             (points[2][0],points[2][1]),
    #             (points[1][0],points[1][1]),
    #         ]
    #         if showbottom:
    #             bottomcolor = self.decidebottomcolor(hover,selected_value,numdrawn,args[numdrawn])       
    #             gfxdraw.filled_polygon(screen,bottom_polygon,bottomcolor)  
    #             # bottomcolor = self.decidebottomcolor(hover,selected_value,numdrawn,*[arg[numdrawn] for arg in args])         
               

    #         for (xoffset,yoffset),text in self.texts[numdrawn].items():
    #             screen.blit(text, (x+xoffset, y+yoffset))
            
            
            
            # bottom_polygon = [[points[0][0]+18, points[0][1] + height - 7],
            #                 [points[1][0]+5, points[1][1]],
            #                 [points[2][0], points[2][1]],
            #                 [points[3][0], points[3][1]],
            #                 [points[3][0]-7, points[3][1]],
            #                 [points[3][0]+5, points[3][1] + height - 7],
            #                 ]
            
        #     pygame.draw.polygon(screen, (0,0,0), points, 3)

        #     y += polyheight; x += xcoordshift; numdrawn += 1

        # return selected_value
        



# from Defs import *
# import pygame,pygame.gfxdraw

# class LatterScroll():
#     def __init__(self,polysdisplayed=5):
#         self.pdis = polysdisplayed# number of polygons displayed at once
#         self.texts = []# list of dicts, each dict is {(x,y):text}, each is for a different polygon
#         self.totalwidth = []# the total width of the box, each item is a int for each polygon

#         # the coords and heights of each polygon drawn in the last call of draw_polys, Not used in this class, but may be used in child classes
#         self.coords_height = []

#     def storeTexts(self,extraspace=0,resetlist=False,**kwargs):
#         """Kwargs should be 'text:str':(relativex,relativey,fontsize,fontcolor))"""
#         """Relative coords are relative to the top left of the box"""
#         """This function should be called for each polygon in the latter"""
#         if resetlist:# if it is the first time in a new frame
#             self.texts = []
#             self.totalwidth = []
        
#         self.texts.append({(x,y):s_render(text,size,color) for text,(x,y,size,color) in kwargs.items()})
#         furthest = max(self.texts[-1].keys(),key=lambda x:x[0])# finding the furthest x value being drawn

#         self.totalwidth.append(0)# adding a new item to the list of total widths
#         self.totalwidth[-1] = furthest[0]+self.texts[-1][furthest].get_width()+extraspace# adding the width of the furthest text to the total width (used for width of polygon)
#         return self.totalwidth, self.texts
#     def storeTextsVariable(self,extraspace=0,resetlist=False,**kwargs):
#         """Allows for text width to be based on the width of another text"""
#         """Kwargs should be 'text:str':((text,x),relativey,fontsize,fontcolor))"""
#         # an input could be {'VIXEL':(50,100,fontsize,color),'QWIRE':(('VIXEL',30),y,fontsize,color)}
#         # the x value of QWIRE will be the width of VIXEL + 30

#         if resetlist:# if it is the first time in a new frame
#             self.texts = []
#             self.totalwidth = []

#         self.texts.append({})
#         texts = {text:s_render(text,size,color) for text,(x,y,size,color) in kwargs.items()}# creating a dict of texts for the polygon
#         textwidths = {text:texts[text].get_width() for text in texts}# creating a dict of text widths for the polygon

#         for text,(x,y,*_) in kwargs.items():# looping through the kwargs (all the texts to be drawn)
#             if type(x) == tuple:# if the x value is a tuple, it is a variable width meaning it is based on the width of another text

#                 x = textwidths[x[0]]+x[1]# the first x value is a string, the second is the offset. They are both added, one from the width of another text
#             self.texts[-1][(x,y)] = texts[text]# adding the text to the dict of texts for the polygon
#         furthest = max(self.texts[-1].keys(),key=lambda x:x[0])# finding the furthest x value being drawn

#         self.totalwidth.append(0)# adding a new item to the list of total widths
#         self.totalwidth[-1] = furthest[0]+self.texts[-1][furthest].get_width()+extraspace# adding the width of the furthest text to the total width (used for width of polygon)
#         return self.totalwidth, self.texts

#     def decidebottomcolor(self,hover,selected_value,numdrawn,*args):
#         """This can be overriden in child classes"""
#         return ((80,80,80),(200,200,200)) if hover or numdrawn == selected_value else ((50,50,50),(150,150,150))
    
#     def draw_polys(self,screen:pygame.Surface,coords:tuple,maxy:int,polyheight:tuple,mousebuttons,selected_value,xcoordshift=0,polyshift=0,showbottom=True,*args):
#         """This function is called once after all the texts have been stored and draws the polygons to the screen
#         args is a list of arguments that will be passed to decidebottomcolor
#         xcoordshift is applied to the xcoord of each polygon being iterated, polyshift is adjusting the shape of the polygon (rectange->trapezoid)"""

#         x,y = coords
#         numdrawn = 0 
#         self.coords_height = []
#         while y < maxy and numdrawn < len(self.texts):
            
#             height = polyheight*.85
#             self.coords_height.append((x,y,height))
#             points = [(x, y), (x + polyshift, y + height), (x + 10 + polyshift + self.totalwidth[numdrawn], y + height), (x + 10 + self.totalwidth[numdrawn], y)]
#             gfxdraw.filled_polygon(screen, points, (15, 15, 15, 150))
            

#             for (xoffset,yoffset),text in self.texts[numdrawn].items():
#                 screen.blit(text, (x+xoffset, y+yoffset))
            
#             if (hover:=point_in_polygon(pygame.mouse.get_pos(),points)):
#                 if mousebuttons == 1:
#                     selected_value = numdrawn
#                     soundEffects['clickbutton2'].play()
            
#             bottom_polygon = [[points[0][0]+18, points[0][1] + height - 7],
#                             [points[1][0]+5, points[1][1]],
#                             [points[2][0], points[2][1]],
#                             [points[3][0], points[3][1]],
#                             [points[3][0]-7, points[3][1]],
#                             [points[3][0]+5, points[3][1] + height - 7],
#                             ]
#             if showbottom:
#                 bottomcolor = self.decidebottomcolor(hover,selected_value,numdrawn,args[numdrawn])         
#                 # bottomcolor = self.decidebottomcolor(hover,selected_value,numdrawn,*[arg[numdrawn] for arg in args])         
#                 gfxdraw.filled_polygon(screen,bottom_polygon,bottomcolor)
#             pygame.draw.polygon(screen, bottomcolor, points, 5)

#             y += polyheight; x += xcoordshift; numdrawn += 1

#         return selected_value
        

# class PortfolioLatter(LatterScroll):
#     def __init__(self, polysdisplayed=5):
#         super().__init__(polysdisplayed)
    
#     def draw_stockgraph(self,screen,stocks):

#         for i,stock in enumerate(stocks):
            
#             x,y,height = self.coords_height[i]
#             addedx = self.texts[i][list(self.texts[i])[0]].get_width()+45
#             stock[0].baredraw(screen, (x+130+addedx, y), (x+addedx, y+height-9), '1D')

#     def decidebottomcolor(self,hover,selected_value,numdrawn,stock):
#         percentchange = ((stock[0].price - stock[1]) / stock[1]) * 100

#         if hover or selected_value == numdrawn:
#             if percentchange > 0:bottomcolor = (0, 200, 0)
#             elif percentchange == 0:bottomcolor = (200, 200, 200)
#             else:bottomcolor = (200, 0, 0)
#         else:
#             if percentchange > 0: bottomcolor = (0, 80, 0)
#             elif percentchange == 0: bottomcolor = (80, 80, 80)
#             else: bottomcolor = (80, 0, 0)
#         return bottomcolor

    