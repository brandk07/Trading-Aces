
import pygame
from Defs import *
from pygame import gfxdraw

class UI_controls():
    def __init__(self,windowoffset,maxspeed) -> None:
        self.winset = windowoffset
        self.gameplay_speed = 0
        self.maxspeed = maxspeed
        self.gamespeedtexts = [fontlist[40].render(f'x{speed}',(0,0,0))[0] for speed in range(self.maxspeed+1)]

        self.sliderxy = [702+self.winset[0],1003+self.winset[1]]
        self.sliderxy = [1700+self.winset[0],700+self.winset[1]]
        self.sliderwh = [55,150]
        
    def draw(self,screen,mousebuttons:int,menudrawn:bool):
        # draw a polygon starting at pauseplayxy, then fastwardxy, then fastwardxy+70, then pauseplayxy+70
        # use numbers rather than variables
        pygame.draw.polygon(screen,(110,110,110),[(700+self.winset[0],1000+self.winset[1]),(700+self.winset[0],1060+self.winset[1]),(760+self.winset[0],1060+self.winset[1]),(760+self.winset[0],1000+self.winset[1])])
        # make a gradient of color going from grey to red within the polygon
        start_color = pygame.Color(110, 110, 110)
        end_color = pygame.Color(255, 0, 0)

        # Define the polygon points
        points = [(700+self.winset[0],1000+self.winset[1]),(700+self.winset[0],1060+self.winset[1]),(760+self.winset[0],1060+self.winset[1]),(760+self.winset[0],1000+self.winset[1])]
        # Calculate the number of lines in the gradient
        num_lines = points[2][1] - points[1][1]

        # Draw each line in the gradient
        for i in range(num_lines):
            color = (
                start_color.r + (end_color.r - start_color.r) * i / num_lines,
                start_color.g + (end_color.g - start_color.g) * i / num_lines,
                start_color.b + (end_color.b - start_color.b) * i / num_lines
            )
            pygame.draw.line(screen, color, (points[0][0], points[0][1] + i), (points[3][0], points[3][1] + i))

        # put a box around the polygon with a width of 5 colored black
        gfxdraw.filled_polygon(screen,[self.sliderxy,(self.sliderxy[0]+55,self.sliderxy[1]),(self.sliderxy[0]+55,self.sliderxy[1]+15),(self.sliderxy[0],self.sliderxy[1]+15)],(60,60,60))
        # the polygon is 388 pixels wide, so each pixel is worth 1/16 of the speed of the game
        pygame.draw.polygon(screen,(0,0,0),[(700+self.winset[0],1000+self.winset[1]),(700+self.winset[0],1060+self.winset[1]),(760+self.winset[0],1060+self.winset[1]),(760+self.winset[0],1000+self.winset[1])],5)
        mousex,mousey = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            rect = pygame.Rect(700+self.winset[0],1009+self.winset[1],60,373)#the rect that the slider can be moved in
            
            if rect.collidepoint(mousex,mousey):
                if (((mousey-7)-1000-self.winset[1])//((1060-1000)//(self.maxspeed+1))) < len(self.gamespeedtexts):
                    self.sliderxy[1] = mousey-7
                    # (current slider - original slider) // (width of polygon // 16) = speed of game
                    self.gameplay_speed = ((self.sliderxy[1]-1000-self.winset[1])//((1060-1000)//(self.maxspeed+1)))#get the speed of the game from the slider position

        # draws the text in the middle of the polygon that indicates the speed of the game
        
        text_x = 700 + (760 - 700) // 2 - self.gamespeedtexts[self.gameplay_speed].get_width() // 2
        text_y = 1000 + (1060 - 1000) // 2 - self.gamespeedtexts[self.gameplay_speed].get_height() // 2
        screen.blit(self.gamespeedtexts[self.gameplay_speed], (text_x, text_y))


        
        