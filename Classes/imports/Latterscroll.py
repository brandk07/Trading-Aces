from Defs import *
import pygame,pygame.gfxdraw

class LaterScroll():
    def __init__(self):
        pass
    
    def draw(self,screen,coords:tuple,values):
        """"values is list of strings [main text,below name text, right side text]"""
        # for stocks, values is [stock name,#shares,$price]
        x,y = coords
        drawnstocks = 0

        if self.selected_stock != None:
            if self.bar.value > sortedstocks.index(self.selected_stock) and self.bar.value < len(sortedstocks):# if the selected stock is above what is displayed
                self.selected_stock = sortedstocks[self.bar.value]# select the highest stock being displayed
            elif self.bar.value+4 < sortedstocks.index(self.selected_stock) and self.bar.value+4 < len(sortedstocks):# if the selected stock is below what is displayed
                self.selected_stock = sortedstocks[self.bar.value+4]# select the lowest stock being displayed

        while y < 830 and self.bar.value+drawnstocks < len(player.stocks):
            stock = sortedstocks[self.bar.value+drawnstocks]

            percentchange = ((stock[0].price - stock[1]) / stock[1]) * 100

            height = coords[1] if self.selected_stock == stock else coords[1]*.85
            nametext = s_render(f'{stock[0]} ', 50, stock[0].color)
            # nametext = fontlist[50].render(f'{stock[0]} ', stock[0].color)[0]
            sharetext = s_render(f"{limit_digits(stock[2],10,False)} Share{'' if stock[2] == 1 else 's'}", 35, (190, 190, 190))
            # sharetext = fontlist[35].render(f"{limit_digits(stock[2],10,False)} Share{'' if stock[2] == 1 else 's'}", (190, 190, 190))[0]
            pricetext = s_render(f'${limit_digits(stock[0].price*stock[2],15)}', 45, (190, 190, 190))
            # pricetext = fontlist[45].render(f'${limit_digits(stock[0].price*stock[2],15)}', (190, 190, 190))[0]
            addedx = 0 if sharetext.get_width() < 85 else round(sharetext.get_width()-85,-1)
            width = nametext.get_width() + pricetext.get_width() + 180 + addedx 

            points = [(x, y), (x + 15, y + height), (x + 25 + width, y + height), (x + 10 + width, y)]
            gfxdraw.filled_polygon(screen, points, (15, 15, 15))
            pygame.draw.polygon(screen, (0, 0, 0), points, 5)
            
            screen.blit(nametext, (x+20, y+15))
            screen.blit(sharetext, (x+25, y+60))
            
            stock[0].baredraw(screen, (x+230+addedx, y), (x+120+addedx, y+height-7), 'hour')
            
            screen.blit(pricetext, (x+250+addedx, y+30))

            if (hover:=point_in_polygon((mousex,mousey),points)):
                if mousebuttons == 1:
                    self.selected_stock = stock
                    soundEffects['clickbutton2'].play()
            
            bottom_polygon = [[points[0][0]+18, points[0][1] + height - 7], 
                            [points[1][0]+5, points[1][1]], 
                            [points[2][0], points[2][1]], 
                            [points[3][0], points[3][1]],
                            [points[3][0]-7, points[3][1]],
                            [points[3][0]+5, points[3][1] + height - 7],
                            ]
            if hover or self.selected_stock == stock:
                if percentchange > 0:bottomcolor = (0, 200, 0)
                elif percentchange == 0:bottomcolor = (200, 200, 200)
                else:bottomcolor = (200, 0, 0)
            else:
                if percentchange > 0: bottomcolor = (0, 80, 0)
                elif percentchange == 0: bottomcolor = (80, 80, 80)
                else: bottomcolor = (80, 0, 0)
            gfxdraw.filled_polygon(screen,bottom_polygon,bottomcolor)

            if self.selected_stock == stock:
                y += yshift; x += xshift; drawnstocks += 1
            else:
                y += yshift*.85; x += xshift*.85; drawnstocks += 1