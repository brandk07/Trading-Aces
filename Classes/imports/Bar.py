import pygame
from Defs import fontlist
from pygame import gfxdraw

def barpos(rect:pygame.Rect,wh:int,xy:int,maxspeed:int,gamespeed:int,horizontal=True):
    """wh is width or height of the bar, xy is the x or y position of the bar"""
    mousex,mousey = pygame.mouse.get_pos()
    if rect.collidepoint(mousex,mousey):
        seclength = (wh-20)/maxspeed# minus 10 for bar width / 2
        

        if horizontal:
            mouselength = int((mousex-xy)/seclength)# finding how many sections the mouse is away from the slider [0,0]
        else:
            mouselength = int((mousey-xy)/seclength)
        
        mouselength = maxspeed if mouselength > maxspeed else mouselength
        mouselength = 0 if mouselength < 0 else mouselength
        return [int(mouselength*seclength)+xy,mouselength]
    
    seclength = (wh-20)/maxspeed# minus 10 for bar width / 2
    return [int(gamespeed*seclength)+xy,gamespeed]

class Bar():
    def __init__(self,windowoffset:list,maxvalue:int,pos:list,wh:list,orientation='horizontal') -> None:
        """Max value must be less than the slider width-20, or height-20 if vertical"""
        self.winset = windowoffset
        self.gameplay_speed = 0
        self.maxvalue = maxvalue
        self.gamespeedtexts = [fontlist[40].render(f'x{value}',(0,0,0))[0] for value in range(self.maxvalue+1)]
        
        self.orientation = orientation
        self.barwh = [wh[0]//19,wh[1]] if orientation == 'horizontal' else [wh[0],wh[1]//19]
        self.sliderwh = wh
        self.sliderxy = [pos[0]+self.winset[0],pos[1]+self.winset[1]]
        self.barxy = self.sliderxy.copy()

        # below is the slider offset, gives a bit more space for the mouse to get to 0 and max speed - conditional statement later for no errors
        soff = [-20,0,40,0] if orientation == 'horizontal' else [0,-20,0,40]
        self.slider_rect = pygame.Rect(self.sliderxy[0]+soff[0],self.sliderxy[1]+soff[1],self.sliderwh[0]+soff[2],self.sliderwh[1]+soff[3])
        # move more stuff to the init function, like the barxy and sliderxy and all the orientation stuff

        # the points for the slider polygon
        self.slider_points = [
            (self.sliderxy[0], self.sliderxy[1]),
            (self.sliderxy[0]+self.sliderwh[0], self.sliderxy[1]),
            (self.sliderxy[0]+self.sliderwh[0], self.sliderxy[1]+self.sliderwh[1]),
            (self.sliderxy[0], self.sliderxy[1]+self.sliderwh[1])
        ]
        self.creategradient()

    def creategradient(self):
        """creates the gradient for the slider, then blits it to the sliderpoly surface"""""
        gradient_start = pygame.Color(255, 0, 0) if self.orientation == 'vertical' else pygame.Color(110, 110, 110)
        gradient_end = pygame.Color(110, 110, 110) if self.orientation == 'vertical' else pygame.Color(255, 0, 0)
        self.sliderpoly = pygame.Surface(self.sliderwh)
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
                pygame.draw.line(self.sliderpoly, color, (0, i), (self.sliderwh[0], i))
            elif self.orientation == 'horizontal':
                pygame.draw.line(self.sliderpoly, color, (i, 0),(i, self.sliderwh[1]))


    def draw(self,screen:pygame.Surface):
        # blit the sliderpoly surface to the screen first
        screen.blit(self.sliderpoly,self.sliderxy)

        # Calculates the bar position and the gameplay speed based on the mouse coords
        if pygame.mouse.get_pressed()[0]:
            
            if self.orientation == 'vertical':
                self.barxy[1],self.gameplay_speed = barpos(self.slider_rect,self.sliderwh[1],self.sliderxy[1],self.maxvalue,self.gameplay_speed,False)
            elif self.orientation == 'horizontal':
                self.barxy[0],self.gameplay_speed = barpos(self.slider_rect,self.sliderwh[0],self.sliderxy[0],self.maxvalue,self.gameplay_speed)
                
        # The bar that the mouse drags across the slider
        gfxdraw.filled_polygon(screen, [self.barxy,
                      (self.barxy[0] + self.barwh[0], self.barxy[1]),
                      (self.barxy[0] + self.barwh[0], self.barxy[1] + self.barwh[1]),
                      (self.barxy[0], self.barxy[1] + self.barwh[1])], (225, 225, 225))
        
        # Box around the slider
        pygame.draw.polygon(screen,(0,0,0),self.slider_points,5)
        

        # Draw the text that displays the gameplay speed
        textx = (self.sliderwh[0]//2 if self.orientation == 'horizontal' else self.sliderwh[0]//1.5) - self.gamespeedtexts[self.gameplay_speed].get_width()
        texty = self.gamespeedtexts[self.gameplay_speed].get_height()
        screen.blit(self.gamespeedtexts[self.gameplay_speed], (self.sliderxy[0]+textx, self.sliderxy[1]+self.sliderwh[1]//2-texty//2))

# [20,60] [60,20]
# [700,1000] [1000,650]