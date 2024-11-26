import pygame
from Defs import *
from pygame import gfxdraw

def barpos(points:list,wh:int,xy:int,maxspeed:int,gamespeed:int,barwh:int,horizontal=True,reverse=False):
    """wh is width or height of the bar, xy is the x or y position of the bar"""
    mousex,mousey = pygame.mouse.get_pos()
    if point_in_polygon((mousex,mousey),points):
        seclength = (wh-(barwh/2))/maxspeed# minus 10 for bar width / 2
         
        if horizontal:
            mouselength = int((mousex-xy)/seclength)# finding how many sections the mouse is away from the slider [0,0]
        else:
            mouselength = int(((mousey-(barwh/2))-xy)/seclength)
        mouselength = maxspeed if mouselength > maxspeed else mouselength
        mouselength = 0 if mouselength < 0 else mouselength

        if mouselength == maxspeed:
            return [int(mouselength*seclength)+xy,mouselength,True]
        # the code below is to make it snap to the closest bar - before it would always go to the top bar because of the int truncate
        next_mouselength = mouselength + 1# the next bar
        next_barpos = int(next_mouselength * seclength) + xy# the next bar position
        current_barpos = int(mouselength * seclength) + xy# the current bar position
        comparingvar = mousex if horizontal else mousey# the mouse x or y position depending on the orientation of the bar
        
        if abs(comparingvar - next_barpos) < abs(comparingvar - current_barpos):# if the next bar is closer to the mouse than the current bar
            return [next_barpos, next_mouselength, True]
        else:
            return [current_barpos, mouselength, True]

        # return [int(mouselength*seclength)+xy,mouselength,True]
   
    seclength = (wh-(barwh * (0.5 if reverse else 1)))/maxspeed# minus 10 for bar width / 2

    return [int(gamespeed*seclength)+xy,gamespeed,False]

class SliderBar():
    def __init__(self,maxvalue:int,color:list,minvalue=0,barcolor=((150,150,150),(210,210,210))) -> None:
        """Max value must be less than the slider width-20, or height-20 if vertical, color = [(colorstart),(colorend)]"""
        self.value = 0
        self.maxvalue = maxvalue; self.minvalue = minvalue
        self.gamevaluetexts = [fontlist[40].render(f'x{value}',(0,0,0))[0] for value in range(self.maxvalue+1)]
        self.barcolors = barcolor
        self.orientation = 'horizontal'
        self.sliderwh = self.sliderxy = self.barwh = self.barxy = self.shift = [0, 0]
        self.color = color
        self.reversedscroll = False
        # below is the slider offset, gives a bit more space for the mouse to get to 0 and max speed - conditional statement later for no errors
        # self.slider_rect = pygame.Rect(0,0,0,0)
        # the points for the slider polygon
        self.slider_points = []

    def getValue(self):
        return self.value
    
    def changeMaxValue(self,maxvalue):
        if maxvalue != self.maxvalue:
            self.maxvalue = maxvalue
            if self.maxvalue > len(self.gamevaluetexts)-1:
                for i in range(1,self.maxvalue-len(self.gamevaluetexts)+3):
                    self.gamevaluetexts.append(fontlist[40].render(f'x{len(self.gamevaluetexts)}',(0,0,0))[0])

            self.value = self.value if self.value < self.maxvalue else self.maxvalue
    def set_currentvalue(self,newvalue,overridemax=False):
        self.value = newvalue
        if not overridemax and self.value > self.maxvalue:
            self.changeMaxValue(self.value)
    
        self.value = self.maxvalue if self.value > self.maxvalue else self.value
        self.value = 0 if self.value < 0 else self.value
        if self.sliderxy != [0,0]:
            self.updatebarxy(self.reversedscroll)

    def changecurrentvalue(self,offset,overridemax=False):
        """changes the current value by the offset"""
        self.value += offset
        if not overridemax and self.value > self.maxvalue:
            self.changeMaxValue(self.value)
    
        self.value = self.maxvalue if self.value > self.maxvalue else self.value
        self.value = 0 if self.value < 0 else self.value
        self.updatebarxy(self.reversedscroll)

    def scroll(self,mousebuttons):
        """changes the current value by the offset"""
        if mousebuttons == 4:
            self.changecurrentvalue(-1)
        elif mousebuttons == 5:
            self.changecurrentvalue(1)

    def creategradient(self):
        """creates the gradient for the slider, then blits it to the sliderpoly surface"""""
        gradient_start = pygame.Color(self.color[0]) if self.orientation == 'vertical' else pygame.Color(self.color[1])
        gradient_end = pygame.Color(self.color[1]) if self.orientation == 'vertical' else pygame.Color(self.color[0])
        
        self.sliderpoly = pygame.Surface((self.sliderwh[0]+self.shift[0],self.sliderwh[1]+self.shift[1]))

        self.sliderpoly.fill((0,0,0))
        self.sliderpoly.set_colorkey((0,0,0))
        # Calculate the number of lines in the gradient
        num_lines = self.sliderwh[0] if self.orientation == 'horizontal' else self.sliderwh[1]
        
        # Draw each line in the gradient
        for i in range(num_lines):
            color = (
                gradient_start.r + (gradient_end.r - gradient_start.r) * i / num_lines,
                gradient_start.g + (gradient_end.g - gradient_start.g) * i / num_lines,
                gradient_start.b + (gradient_end.b - gradient_start.b) * i / num_lines
            )
            if self.orientation == 'vertical':
                offset = ((self.shift[0]/self.sliderwh[1])*i)
                pygame.draw.line(self.sliderpoly, color, (0+offset, i), (self.sliderwh[0]+offset, i))
            elif self.orientation == 'horizontal':
                offset = ((self.shift[1]/self.sliderwh[0]))*i
                pygame.draw.line(self.sliderpoly, color, (i, 0+offset),(i, self.sliderwh[1]+offset))

    def setpoints(self,sliderxy,sliderwh,orientation,barwh):
        self.orientation = orientation
        if barwh != None:
            self.barwh = barwh
        else:
            self.barwh = [sliderwh[0]//19,sliderwh[1]] if orientation == 'horizontal' else [sliderwh[0],sliderwh[1]//19]
        self.sliderwh = sliderwh
        self.sliderxy = [sliderxy[0],sliderxy[1]]
        self.barxy = self.sliderxy.copy() if orientation == 'horizontal' else [self.sliderxy[0],self.sliderxy[1]+self.sliderwh[1]-self.barwh[1]]

        # soff = [-20,0,40,0] if orientation == 'horizontal' else [0,-20,0,40]
        # self.slider_rect = pygame.Rect(self.sliderxy[0]+soff[0],self.sliderxy[1]+soff[1],self.sliderwh[0]+soff[2],self.sliderwh[1]+soff[3])
        # self.slider_rect = pygame.Rect(self.sliderxy[0],self.sliderxy[1],self.sliderwh[0],self.sliderwh[1])


        self.slider_points = [
            (self.sliderxy[0], self.sliderxy[1]),
            (self.sliderxy[0]+self.sliderwh[0], self.sliderxy[1]+self.shift[1]),
            (self.sliderxy[0]+self.sliderwh[0]+self.shift[0], self.sliderxy[1]+self.sliderwh[1]+self.shift[1]),
            (self.sliderxy[0]+self.shift[0], self.sliderxy[1]+self.sliderwh[1])
        ]# top left, top right, bottom right, bottom left
        self.creategradient()
    def updatebarxy(self,reversedscroll):
        """updates the barxy based on the gameplay speed"""
        if self.orientation == 'vertical':
            if self.barwh[1] < self.sliderwh[1]:
                if reversedscroll:
                        self.barxy[1],self.value,mouseover = barpos(self.slider_points,self.sliderwh[1]-(self.barwh[1]/2),self.sliderxy[1],self.maxvalue,self.value,self.barwh[1],horizontal=False,reverse=True)
                else:
                    self.barxy[1],self.value,mouseover = barpos(self.slider_points,-self.sliderwh[1]+(self.barwh[1]*2),self.sliderxy[1]+self.sliderwh[1]-self.barwh[1],self.maxvalue,self.value,self.barwh[1],False)
            else: raise ValueError(f'Bar height must be less than the slider height bh{self.barwh[1]} sh{self.sliderwh[1]}')
        elif self.orientation == 'horizontal':
            if self.barwh[0] < self.sliderwh[0]:
                if reversedscroll:
                    self.barxy[0],self.value,mouseover = barpos(self.slider_points,self.sliderwh[0]-(self.barwh[0]/2),self.sliderxy[0],self.maxvalue,self.value,self.barwh[0],horizontal=True,reverse=True)
                else:
                    self.barxy[0],self.value,mouseover = barpos(self.slider_points,-self.sliderwh[0]+(self.barwh[0]*2),self.sliderxy[0]+self.sliderwh[0]-self.barwh[0],self.maxvalue,self.value,self.barwh[0],True)
            else: raise ValueError(f'Bar width must be less than the slider width bw{self.barwh[0]} sw{self.sliderwh[0]}')
        return mouseover
    def draw_bar(self,screen:pygame.Surface,sliderxy,sliderwh,orientation,barwh=None,shift=0,reversedscroll=False,text=True):
        """sliderxy [startx,starty], 
        sliderwh [width,height], 
        orientation ['horizontal','vertical'], 
        shift is the offset for the bottom two points to make a trapezoid (Must be positive)"""

        if self.sliderxy != sliderxy or self.sliderwh != sliderwh or shift != max(self.shift) or self.reversedscroll != reversedscroll:# if the slider has moved, then recreate the gradient and the slider_rect
            self.reversedscroll = reversedscroll
            self.shift = [0,0]
            self.shift[0] = shift if orientation == 'vertical' else 0
            self.shift[1] = shift if orientation == 'horizontal' else 0

            self.setpoints(sliderxy,sliderwh,orientation,barwh)
            self.updatebarxy(reversedscroll)

        # blit the sliderpoly surface to the screen first
        screen.blit(self.sliderpoly,self.sliderxy)

        color = self.barcolors[0]
        # Calculates the bar position and the gameplay speed based on the mouse coords
        if pygame.mouse.get_pressed()[0]:
            if self.updatebarxy(reversedscroll):
                color = self.barcolors[1]

            

        if max(self.shift) != 0:
            # the height of the barxy to the top of the slider
            subheight = self.sliderwh[1]-self.barxy[1]+self.sliderxy[1]
            # the offset for the bar to make a trapezoid - only needs part of the shift for the bar based on the bar's y position
            xoffset = self.shift[0]*(1-(subheight/self.sliderwh[1])) if self.orientation == 'vertical' else 0
            # the width of the barxy to the left of the slider
            subwidth = self.sliderwh[0]-self.barxy[0]+self.sliderxy[0]
            # the offset for the bar to make a trapezoid - only needs part of the shift for the bar based on the bar's x position
            yoffset = (self.shift[1] * (1 - (subwidth / self.sliderwh[0]))) - self.shift[1] if self.orientation == 'horizontal' else 0
        else:
            xoffset = 0
            yoffset = 0


        ratio = self.sliderwh[0]/self.barwh[0] if self.orientation == 'horizontal' else self.sliderwh[1]/(self.barwh[1])# ratio of the slider to the bar
        
        # The bar that the mouse drags across the slider
        gfxdraw.filled_polygon(screen, [
                    (self.barxy[0] + xoffset+ self.barwh[0], self.barxy[1] + self.shift[1] + yoffset),
                    (self.barxy[0]  + xoffset , self.barxy[1] + (self.shift[1]) + yoffset),
                    (self.barxy[0] + xoffset + (self.shift[0]/ratio), self.barxy[1] + self.barwh[1] + (self.shift[1]) + yoffset),
                    (self.barxy[0] + self.barwh[0] + xoffset + (self.shift[0]/ratio), self.barxy[1] + self.barwh[1]+self.shift[1] + yoffset),
                    ], color)
            
        # Box around the slider
        pygame.draw.polygon(screen,(0,0,0),self.slider_points,5)
        
        if type(text) == bool and text:
            # Draw the text that displays the gameplay speed
            textx = (self.sliderwh[0]//2 if self.orientation == 'horizontal' else self.sliderwh[0]//2) - (self.gamevaluetexts[self.value].get_width()/2)
            texty = self.gamevaluetexts[self.value].get_height()
            screen.blit(self.gamevaluetexts[self.value], (self.sliderxy[0]+textx, self.sliderxy[1]+self.sliderwh[1]//2-texty//2))
        elif type(text) == str:
            text = s_render(text,40,(0,0,0))
            width = text.get_width()
            textx = ((self.sliderwh[0]/2)-(width/2) if self.orientation == 'horizontal' else (self.sliderwh[0]/2)-(width/2))
            texty = text.get_height()
            screen.blit(text, (self.sliderxy[0]+textx, self.sliderxy[1]+self.sliderwh[1]//2-texty//2))
        if self.value < self.minvalue:
            self.value = self.minvalue
        if self.value <= 2:
            self.value = 0
        return self.value