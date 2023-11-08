import pygame
from Defs import *
from pygame import gfxdraw

class UI_controls():
    def __init__(self,windowoffset,maxspeed) -> None:
        self.winset = windowoffset
        self.gameplay_speed = 0
        self.maxspeed = maxspeed
        self.gamespeedtexts = [fontlist[40].render(f'x{speed}',(0,0,0))[0] for speed in range(self.maxspeed+1)]
        self.barxy = [700+self.winset[0],1000+self.winset[1]]
        self.barwh = [60,373]
        self.sliderxy = [702+self.winset[0],1003+self.winset[1]]
        self.sliderwh = [60,373]
        # slider and bar wh is really fucked up - need to dive into it
        
    def draw(self,screen,mousebuttons:int,menudrawn:bool, orientation='horizontal'):
        # draw a polygon starting at pauseplayxy, then fastwardxy, then fastwardxy+70, then pauseplayxy+70
        # use numbers rather than variables
        if orientation == 'vertical':
            slider_points = [(self.barxy[0]-2,self.barxy[1]-3),(self.barxy[0]-2,self.barxy[1]+self.barwh[1]+3),(self.barxy[0]+self.barwh[0]+2,self.barxy[1]+self.barwh[1]+3),(self.barxy[0]+self.barwh[0]+2,self.barxy[1]-3)]
            gradient_start = pygame.Color(110, 110, 110)
            gradient_end = pygame.Color(255, 0, 0)
            bar_rect = pygame.Rect(self.barxy[0]-2,self.barxy[1]-2,self.barwh[0],self.barwh[1])
        elif orientation == 'horizontal':
            slider_points = [(self.barxy[0]-3,self.barxy[1]-2),(self.barxy[0]+self.barwh[0]+3,self.barxy[1]-2),(self.barxy[0]+self.barwh[0]+3,self.barxy[1]+self.barwh[1]+2),(self.barxy[0]-3,self.barxy[1]+self.barwh[1]+2)]
            gradient_start = pygame.Color(255, 0, 0)
            gradient_end = pygame.Color(110, 110, 110)
            bar_rect = pygame.Rect(self.barxy[0]-2,self.barxy[1]-2,self.barwh[1],self.barwh[0])
            

        pygame.draw.polygon(screen,(110,110,110),slider_points)
        
        # make a gradient of color going from grey to red within the polygon
        # Define the polygon points
        points = slider_points
        # Calculate the number of lines in the gradient
        num_lines = points[2][1] - points[1][1]

        # Draw each line in the gradient
        for i in range(num_lines):
            color = (
                gradient_start.r + (gradient_end.r - gradient_start.r) * i / num_lines,
                gradient_start.g + (gradient_end.g - gradient_start.g) * i / num_lines,
                gradient_start.b + (gradient_end.b - gradient_start.b) * i / num_lines
            )
            if orientation == 'vertical':
                pygame.draw.line(screen, color, (points[0][0], points[0][1] + i), (points[3][0], points[3][1] + i))
            elif orientation == 'horizontal':
                pygame.draw.line(screen, color, (points[0][0] + i, points[0][1]), (points[3][0] + i, points[3][1]))

        # put a box around the polygon with a width of 5 colored black
        if orientation == 'vertical':
            gfxdraw.filled_polygon(screen,[self.sliderxy,(self.sliderxy[0]+self.sliderwh[0]-5,self.sliderxy[1]),(self.sliderxy[0]+self.sliderwh[0]-5,self.sliderxy[1]+15),(self.sliderxy[0],self.sliderxy[1]+15)],(60,60,60))
            pygame.draw.polygon(screen,(0,0,0),slider_points,5)
        elif orientation == 'horizontal':
            gfxdraw.filled_polygon(screen,[self.sliderxy,(self.sliderxy[0],self.sliderxy[1]+self.sliderwh[0]-5),(self.sliderxy[0]+15,self.sliderxy[1]+self.sliderwh[0]-5),(self.sliderxy[0]+15,self.sliderxy[1])],(60,60,60))
            pygame.draw.polygon(screen,(0,0,0),slider_points,5)

        mousex,mousey = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if orientation == 'vertical':
                if bar_rect.collidepoint(mousex,mousey):
                    if (((mousey-7)-self.barxy[1])//((self.barwh[1]-15)//(self.maxspeed+1))) < len(self.gamespeedtexts):
                        self.sliderxy[1] = mousey-7
                        # (current slider - original slider) // (width of polygon // 16) = speed of game
                        
                        self.gameplay_speed = (((self.sliderxy[1])-self.barxy[1])//((self.barwh[1]-15)//(self.maxspeed+1)))#get the speed of the game from the slider position
            elif orientation == 'horizontal':
                if bar_rect.collidepoint(mousex,mousey):
                    if (((mousex-7)-self.barxy[0])//((self.barwh[0]-15)//(self.maxspeed+1))) < len(self.gamespeedtexts):
                        self.sliderxy[0] = mousex-7
                        # (current slider - original slider) // (width of polygon // 16) = speed of game
                        
                        self.gameplay_speed = (((self.sliderxy[0])-self.barxy[0])//((self.barwh[0]-15)//(self.maxspeed+1)))#get the speed of the game from the slider position

        # draws the text in the middle of the polygon that indicates the speed of the game
        # text_x = self.sliderxy[0] + (self.sliderwh[0] - self.gamespeedtexts[self.gameplay_speed].get_width()) // 2
        # text_y = self.sliderxy[1] + (self.sliderwh[1] - self.gamespeedtexts[self.gameplay_speed].get_height()) // 2
        # if orientation == 'vertical':
        #     screen.blit(self.gamespeedtexts[self.gameplay_speed], (text_x, text_y))
        # elif orientation == 'horizontal':
        #     rotated_text = pygame.transform.rotate(self.gamespeedtexts[self.gameplay_speed], 90)
        #     screen.blit(rotated_text, (text_x, text_y))

        screen.blit(self.gamespeedtexts[self.gameplay_speed], (self.barxy[0]+self.barwh[0]//2, self.barxy[1]+self.barwh[1]//2))