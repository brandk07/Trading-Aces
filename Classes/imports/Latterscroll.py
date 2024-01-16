from Defs import *
import pygame,pygame.gfxdraw

class LatterScroll():
    def __init__(self,polysdisplayed=5):
        self.pdis = polysdisplayed# number of polygons displayed at once
        self.texts = []# list of dicts, each dict is {(x,y):text}, each is for a different polygon
        self.totalwidth = []# the total width of the box, each item is a int for each polygon

        # the coords and heights of each polygon drawn in the last call of draw_polys, Not used in this class, but may be used in child classes
        self.coords_height = []

    def storeTexts(self,extraspace=0,resetlist=False,**kwargs):
        """Kwargs should be 'text:str':(relativex,relativey,fontsize,fontcolor))"""
        """Relative coords are relative to the top left of the box"""
        """This function should be called for each polygon in the latter"""
        if resetlist:# if it is the first time in a new frame
            self.texts = []
            self.totalwidth = []
        
        self.texts.append({(x,y):s_render(text,size,color) for text,(x,y,size,color) in kwargs.items()})
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
        texts = {text:s_render(text,size,color) for text,(x,y,size,color) in kwargs.items()}# creating a dict of texts for the polygon
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
        return ((80,80,80),(200,200,200)) if hover or numdrawn == selected_value else ((50,50,50),(150,150,150))
    
    def draw_polys(self,screen:pygame.Surface,coords:tuple,maxy:int,polyheight:tuple,mousebuttons,selected_value,xshift=0,showbottom=True,*args):
        """This function is called once after all the texts have been stored and draws the polygons to the screen
        args is a list of arguments that will be passed to decidebottomcolor"""

        x,y = coords
        numdrawn = 0 
        self.coords_height = []
        while y < maxy and numdrawn < len(self.texts):
            
            height = polyheight*.85 if numdrawn == selected_value else polyheight*.65
            self.coords_height.append((x,y,height))
            points = [(x, y), (x + 15, y + height), (x + 25 + self.totalwidth[numdrawn], y + height), (x + 10 + self.totalwidth[numdrawn], y)]
            gfxdraw.filled_polygon(screen, points, (15, 15, 15, 150))
            pygame.draw.polygon(screen, (0, 0, 0), points, 5)

            for (xoffset,yoffset),text in self.texts[numdrawn].items():
                screen.blit(text, (x+xoffset, y+yoffset))
            
            if (hover:=point_in_polygon(pygame.mouse.get_pos(),points)):
                if mousebuttons == 1:
                    selected_value = numdrawn
                    soundEffects['clickbutton2'].play()
            
            bottom_polygon = [[points[0][0]+18, points[0][1] + height - 7],
                            [points[1][0]+5, points[1][1]],
                            [points[2][0], points[2][1]],
                            [points[3][0], points[3][1]],
                            [points[3][0]-7, points[3][1]],
                            [points[3][0]+5, points[3][1] + height - 7],
                            ]
            if showbottom:
                bottomcolor = self.decidebottomcolor(hover,selected_value,numdrawn,args[numdrawn])         
                # bottomcolor = self.decidebottomcolor(hover,selected_value,numdrawn,*[arg[numdrawn] for arg in args])         
                gfxdraw.filled_polygon(screen,bottom_polygon,bottomcolor)

            if numdrawn == selected_value:
                y += polyheight; x += xshift; numdrawn += 1
            else:
                y += polyheight*.8; x += xshift*.85; numdrawn += 1

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

        if hover or selected_value == numdrawn:
            if percentchange > 0:bottomcolor = (0, 200, 0)
            elif percentchange == 0:bottomcolor = (200, 200, 200)
            else:bottomcolor = (200, 0, 0)
        else:
            if percentchange > 0: bottomcolor = (0, 80, 0)
            elif percentchange == 0: bottomcolor = (80, 80, 80)
            else: bottomcolor = (80, 0, 0)
        return bottomcolor

    