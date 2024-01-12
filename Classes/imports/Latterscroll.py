from Defs import *
import pygame,pygame.gfxdraw

class LaterScroll():
    def __init__(self):
        self.texts = []
        self.totalwidth = 0

    def storeTexts(self,extraspace=0,**kwargs):
        """Kwargs should be 'text:str':(relativex,relativey,fontsize,fontcolor))"""
        """Relative coords are relative to the top left of the box"""
        self.texts = []
        
        self.texts = {(x,y):s_render(text,size,color) for i,text,(x,y,size,color) in enumerate(kwargs.items())}
        furthest  = max(self.texts.keys(),key=lambda x:x[0])
        self.totalwidth = furthest[0]+self.texts[furthest].get_width()+extraspace

    def storeTextsVariable(self,extraspace=0,**kwargs):
        """Allows for text width to be based on the width of another text"""
        """Kwargs should be 'text:str':((text,x),relativey,fontsize,fontcolor))"""
        # an input could be {'VIXEL':(50,100,fontsize,color),'QWIRE':(('VIXEL',30),y,fontsize,color)}
        # the x value of QWIRE will be the width of VIXEL + 30

        texts = {text:s_render(text,size,color) for i,text,(x,y,size,color) in enumerate(kwargs.items())}
        textwidths = {text:texts[text].get_width() for text in texts}
        self.texts.clear()
        for text,(x,y,*_) in kwargs.items():
            if type(x) == tuple:
                x = textwidths[x[0]]+x[1]
            self.texts[(x,y)] = texts[text]

    def draw_polys(self,screen:pygame.Surface,coords:tuple,maxy:int,polywh:tuple,mousebuttons,selected_value,xshift=0):
        x,y = coords
        numdrawn = 0 
        
        while y < maxy and numdrawn < len(self.texts):
            
            height = polywh[1] if numdrawn == selected_value else polywh[1]*.85

            points = [(x, y), (x + 15, y + height), (x + 25 + self.totalwidth, y + height), (x + 10 + self.totalwidth, y)]
            gfxdraw.filled_polygon(screen, points, (15, 15, 15))
            pygame.draw.polygon(screen, (0, 0, 0), points, 5)

            for (xoffset,yoffset),text in self.texts.items():
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
            bottomcolor = ((80,80,80),(200,200,200)) if hover or numdrawn == selected_value else ((50,50,50),(150,150,150))
            gfxdraw.filled_polygon(screen,bottom_polygon,bottomcolor[1])

            if numdrawn == selected_value:
                y += height; x += xshift; numdrawn += 1
            else:
                y += height*.85; x += xshift*.85; numdrawn += 1
        






    # def draw(self,screen,coords:tuple,wh:tuple,values,mousebuttons,valueindex,xshift=0,bottomcolors=None):
    #     """"values is list of strings [main text,below name text, right side text]
    #     wh is (width,height) of the box
    #     valueindex is self.bar.value"""

    #     # for stocks, values is [(stock name,size,stockcolor),(#shares,size,color),($price,size,color)]
    #     mousex,mousey = pygame.mouse.get_pos()
    #     x,y = coords
    #     drawnstocks = 0

    #     if self.selected_stock != None:
    #         if valueindex > values.index(self.selected_stock) and valueindex < len(values):# if the selected stock is above what is displayed
    #             self.selected_stock = values[valueindex]# select the highest stock being displayed
    #         elif valueindex+4 < values.index(self.selected_stock) and valueindex+4 < len(values):# if the selected stock is below what is displayed
    #             self.selected_stock = values[valueindex+4]# select the lowest stock being displayed

    #     while y < 830 and valueindex+drawnstocks < len(player.stocks):
    #         currentind = valueindex+drawnstocks

    #         height = wh[1] if self.selected_stock == stock else wh[1]*.85
    #         # nametext = s_render(f'{stock[0]} ', 50, stock[0].color)
    #         # # nametext = fontlist[50].render(f'{stock[0]} ', stock[0].color)[0]
    #         # sharetext = s_render(f"{limit_digits(stock[2],10,False)} Share{'' if stock[2] == 1 else 's'}", 35, (190, 190, 190))
    #         # # sharetext = fontlist[35].render(f"{limit_digits(stock[2],10,False)} Share{'' if stock[2] == 1 else 's'}", (190, 190, 190))[0]
    #         # pricetext = s_render(f'${limit_digits(stock[0].price*stock[2],15)}', 45, (190, 190, 190))
    #         # pricetext = fontlist[45].render(f'${limit_digits(stock[0].price*stock[2],15)}', (190, 190, 190))[0]
    #         texts = [s_render(value) for value in values[currentind]]# nametext,sharetext,pricetext

    #         addedx = 0 if texts[1].get_width() < 85 else round(texts[1].get_width()-85,-1)
    #         width = texts[0].get_width() + texts[2].get_width() + 180 + addedx 

    #         points = [(x, y), (x + 15, y + height), (x + 25 + width, y + height), (x + 10 + width, y)]
    #         gfxdraw.filled_polygon(screen, points, (15, 15, 15))
    #         pygame.draw.polygon(screen, (0, 0, 0), points, 5)
            

    #         screen.blit(nametext, (x+20, y+15))
    #         screen.blit(sharetext, (x+25, y+60))
            
    #         # stock[0].baredraw(screen, (x+230+addedx, y), (x+120+addedx, y+height-7), 'hour')
            
    #         screen.blit(pricetext, (x+250+addedx, y+30))

    #         if (hover:=point_in_polygon((mousex,mousey),points)):
    #             if mousebuttons == 1:
    #                 self.selected_stock = stock
    #                 soundEffects['clickbutton2'].play()
            
    #         bottom_polygon = [[points[0][0]+18, points[0][1] + height - 7], 
    #                         [points[1][0]+5, points[1][1]], 
    #                         [points[2][0], points[2][1]], 
    #                         [points[3][0], points[3][1]],
    #                         [points[3][0]-7, points[3][1]],
    #                         [points[3][0]+5, points[3][1] + height - 7],
    #                         ]
    #         if bottomcolors != None:
    #             bottomcolor = bottomcolors[currentind]
    #         else:
    #             bottomcolor = ((80,80,80),(200,200,200))

    #         bottomcolor = bottomcolor[1] if hover or self.selected_stock == stock else bottomcolor[0]

    #         gfxdraw.filled_polygon(screen,bottom_polygon,bottomcolor)

    #         if self.selected_stock == stock:
    #             y += wh[1]; x += xshift; drawnstocks += 1
    #         else:
    #             y += wh[1]*.85; x += xshift*.85; drawnstocks += 1