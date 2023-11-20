import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.Bar import Bar

# [20,60] [60,20]
# [700,1000] [1000,650]

class UI_Controls(Bar):
    def __init__(self,windowoffset:list,maxvalue:int,pos:list,wh:list,orientation='horizontal') -> None:
        super().__init__(windowoffset,maxvalue,pos,wh,orientation)
# def barpos(rect:pygame.Rect,wh:int,xy:int,maxspeed:int,gamespeed:int,horizontal=True):
#     """wh is width or height of the bar, xy is the x or y position of the bar"""
#     mousex,mousey = pygame.mouse.get_pos()
#     if rect.collidepoint(mousex,mousey):
#         seclength = (wh-10)//maxspeed# minus 10 for bar width / 2

#         if horizontal:
#             mouselength = (mousex-xy)//seclength# finding how many sections the mouse is away from the slider [0,0]
#         else:
#             mouselength = (mousey-xy)//seclength
        
#         mouselength = maxspeed if mouselength > maxspeed else mouselength
#         mouselength = 0 if mouselength < 0 else mouselength

#         return [(mouselength*seclength)+xy,mouselength]
#     return [xy,gamespeed]
# class UI_controls():
#     def __init__(self,windowoffset,maxspeed,) -> None:
#         self.winset = windowoffset
#         self.gameplay_speed = 0
#         self.maxspeed = maxspeed
#         self.gamespeedtexts = [fontlist[40].render(f'x{speed}',(0,0,0))[0] for speed in range(self.maxspeed+1)]
        
#         self.barwh = [60,373]
#         self.sliderxy = [700+self.winset[0],1000+self.winset[1]]
#         self.barxy = self.sliderxy.copy()
#         self.sliderwh = [380,60]#width,height

#         # move more stuff to the init function, like the barxy and sliderxy and all the orientation stuff
    
#     def draw(self,screen,mousebuttons:int,menudrawn:bool, orientation='vertical'):
#         # draw a polygon starting at pauseplayxy, then fastwardxy, then fastwardxy+70, then pauseplayxy+70
#         # use numbers rather than variables

#         self.barwh = [20,60] if orientation == 'horizontal' else [60,20]
#         self.sliderwh = [380,60] if orientation == 'horizontal' else [60,380]
#         self.sliderxy = [700+self.winset[0],1000+self.winset[1]] if orientation == 'horizontal' else [1000+self.winset[0],650+self.winset[1]]
#         self.barxy = self.sliderxy.copy()

#         topleft = (self.sliderxy[0],self.sliderxy[1])
#         topright = (self.sliderxy[0]+self.sliderwh[0],self.sliderxy[1])
#         bottomleft = (self.sliderxy[0],self.sliderxy[1]+self.sliderwh[1])
#         bottomright = (self.sliderxy[0]+self.sliderwh[0],self.sliderxy[1]+self.sliderwh[1])
#         slider_points = [topleft,topright,bottomright,bottomleft]
    
#         gradient_start = pygame.Color(255, 0, 0) if orientation == 'vertical' else pygame.Color(110, 110, 110)
#         gradient_end = pygame.Color(110, 110, 110) if orientation == 'vertical' else pygame.Color(255, 0, 0)

#         soff = [-20,0,40,0] if orientation == 'horizontal' else [0,-20,0,40]# slider offset, gives a bit more space for the mouse to get to 0 and max speed - conditional statement later for no errors
#         slider_rect = pygame.Rect(self.sliderxy[0]+soff[0],self.sliderxy[1]+soff[1],self.sliderwh[0]+soff[2],self.sliderwh[1]+soff[3])
       
            

#         points = slider_points#[topleft,topright,bottomright,bottomleft]

#         # Calculate the number of lines in the gradient
#         num_lines = self.sliderwh[0] if orientation == 'horizontal' else self.sliderwh[1]

#         # Draw each line in the gradient
#         for i in range(num_lines):
#             color = (
#                 gradient_start.r + (gradient_end.r - gradient_start.r) * i / num_lines,
#                 gradient_start.g + (gradient_end.g - gradient_start.g) * i / num_lines,
#                 gradient_start.b + (gradient_end.b - gradient_start.b) * i / num_lines
#             )
#             if orientation == 'vertical':
#                 pygame.draw.line(screen, color, (points[0][0], points[0][1] + i), (points[1][0], points[1][1] + i))
#             elif orientation == 'horizontal':
#                 pygame.draw.line(screen, color, (points[3][0] + i, points[3][1]),(points[0][0] + i, points[0][1]))

#         # The bar that the mouse drags across the slider
#         topleft = self.barxy
#         topright = (self.barxy[0]+self.barwh[0],self.barxy[1])
#         bottomleft = (self.barxy[0],self.barxy[1]+self.barwh[1])
#         bottomright = (self.barxy[0]+self.barwh[0],self.barxy[1]+self.barwh[1])
#         gfxdraw.filled_polygon(screen,[topleft,topright,bottomright,bottomleft],(225,225,225))
    
#         # Box around the slider
#         pygame.draw.polygon(screen,(0,0,0),slider_points,5)

       
#         if pygame.mouse.get_pressed()[0]:
#             # if orientation == 'vertical':
#             #     if slider_rect.collidepoint(mousex,mousey):
#             #         if (((mousey-7)-self.barxy[1])//((self.barwh[1]-19)//(self.maxspeed+1))) < len(self.gamespeedtexts):
#             #             self.barxy[1] = mousey-7
#             #             # (current slider - original slider) // (width of polygon // 16) = speed of game
                        
#             #             self.gameplay_speed = (((self.sliderxy[1])-self.barxy[1])//((self.barwh[1]-15)//(self.maxspeed+1)))#get the speed of the game from the slider position
#             # elif orientation == 'horizontal':
#             #     if slider_rect.collidepoint(mousex,mousey):
#             #         seclength = (self.sliderwh[0]-10)//self.maxspeed# minus 10 for bar width / 2 
#             #         mousexlength = (mousex-self.sliderxy[0])//seclength# finding how many sections the mouse is away from the slider [0,0]

#             #         mousexlength = self.maxspeed if mousexlength > self.maxspeed else mousexlength
#             #         mousexlength = 0 if mousexlength < 0 else mousexlength

#             #         self.barxy[0] = (mousexlength*seclength)+self.sliderxy[0]# finding the x position of the bar
#             #         self.gameplay_speed = mousexlength

#             print(slider_rect.collidepoint(pygame.mouse.get_pos()))
#             if orientation == 'vertical':
#                 self.barxy[1],self.gameplay_speed = barpos(slider_rect,self.sliderwh[1],self.sliderxy[1],self.maxspeed,self.gameplay_speed,False)
#             elif orientation == 'horizontal':
#                 self.barxy[0],self.gameplay_speed = barpos(slider_rect,self.sliderwh[0],self.sliderxy[0],self.maxspeed,self.gameplay_speed)

#         print(self.barxy[1])
#         textwidth = self.gamespeedtexts[self.gameplay_speed].get_width()
#         textheight = self.gamespeedtexts[self.gameplay_speed].get_height()
#         screen.blit(self.gamespeedtexts[self.gameplay_speed], (self.sliderxy[0]+self.sliderwh[0]//2-textwidth, self.sliderxy[1]+self.sliderwh[1]//2-textheight//2))

