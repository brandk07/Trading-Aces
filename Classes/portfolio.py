import pygame
import timeit
from Defs import fontlist,point_in_polygon,closest_point
from Classes.imports.Menu import Menu
from pygame import gfxdraw
from Classes.imports.Bar import SliderBar
import math

DX = 300
DY = 200
DH = 120
class Portfolio(Menu):
    def __init__(self):
        super().__init__(r'Assets\Portfolio\portfolio.png',(30,340))
        # self.icon = pygame.image.load(r'Assets\Portfolio\portfolio2.png').convert_alpha()
        self.icon = pygame.transform.scale(self.icon,(140,100))
        # remove all the white from the image
        self.bar = SliderBar((0,0),50,[(0,120,0),(110,110,110)])
        self.bar.value = 0
        self.icon.set_colorkey((255,255,255))
        self.portfoliotext = fontlist[36].render('Portfolio',(255,255,255))[0]
        self.menudrawn = True

        
    def getpoints(self, w1, w2, w3, x, y):
        """returns the points for the polygon of the portfolio menu""" 
        # top left, top right, bottom right, bottom left
        p1 = ((DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + x + w1 + 25, DY + DH + y), (DX + x + w1 + 10, DY + y))
        p2 = [(DX + 10 + x + w1, DY + y), (DX + 25 + x +w1, DY + DH + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 10 + w1 + w2 + x, DY + y)]
        p3 = [(DX + 10 + w1 + w2 + x, DY + y), (DX + 25 + w1 + w2 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]
        total = [(DX + x, DY + y), (DX + 15 + x, DY + DH + y), (DX + 25 + w1 + w2 + w3 + x, DY + DH + y), (DX + 10 + w1 + w2 + w3 + x, DY + y)]

        return [p1, p2, p3, total]

    def draw_pie_chart(self, screen: pygame.Surface, values:list, radius, coords):
        """Draws the pie chart for the portfolio menu. value is (value, name)"""

        # get the total value of the stocks
        # totalvalue = sum([stock[0].price * stock[2] for stock in player.stocks])
        # get the percentage of each stock
        # print(values)
        total = sum([v[0] for v in values])
        percentages = [[round((value[0]) / total,4)*100,value[1]] for value in values]
        

        other = [0,'Other']
        # print(percentages,'percentages1')
        for i,percent in enumerate(percentages):
            if percent[0] < 5:
                other[0] += percent[0]
                percentages.remove(percent)
                values.remove(values[i])

        if other[0] > 0:
            percentages.append(other)
            values.append(other)
        percentages.sort(key=lambda x:x[0],reverse=True)

        percentindex = math.radians(0)
        # print(percentages,'percentages2')
        angles = []
        for i,percent in enumerate(percentages):
            angles.append([math.radians(percentindex)])
            percentindex += (percent[0]/100)*360
            angles[i].append(math.radians(percentindex))
            angles[i].append(percent[1])
        # print(angles,'angles')
        # points = [[(radius * math.acos(a1), radius * math.asin(a1)), (radius * math.acos(a2), radius * math.asin(a2))] for a1, a2 in angles]
        corners = [coords, (coords[0] + radius*2, coords[1]), (coords[0] + radius*2, coords[1] + radius*2), (coords[0], coords[1] + radius*2)]
        
        # points = [[(coords[0] + radius * math.cos(a1), coords[1] + radius * math.sin(a1)), 
        #            (coords[0] + radius * math.cos(a2), coords[1] + radius * math.sin(a2)), 
        #            corners[closest_point()]] for a1, a2 in angles]
        points = []
       
        colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255),(255,255,255),(0,0,0)]
        for colornum, (a1, a2,name) in enumerate(angles):
            p0 = (coords[0] + radius, coords[1]+radius)
            p1 = (coords[0] + radius + radius * math.cos(a1), radius + coords[1] + (radius * math.sin(a1) * -1))# the first point on the circle
            p2 = (coords[0] + radius + radius * math.cos(a2), radius + coords[1] + (radius * math.sin(a2) * -1))# the second point on the circle - drawn after the corner points
            points = [p0, p1, p2, p0]# put the first points in the list, more points will be added in between p1 and p2
            # points.append(p0, p1, p2, p0)# put the first points in the list, more points will be added in between p1 and p2

            degrees = [0,90,180,270]
            
            angle = math.degrees(a2)-math.degrees(a1)
            # print(angle,'angle')a
            addedcorners = set()
            a1 = int(math.degrees(a1))
            a2 = int(math.degrees(a2))

            num = int((a1//90)*90)
            modifieddegrees = [(degree+num if degree+num < 360 else degree+num-360) for degree in degrees]# the degrees but shifted so that the first degree (relative to a1) is 0
            # print(modifieddegrees)
            for i,degree in enumerate(modifieddegrees):
                # first case is for when both a1 and a2 are in the same quadrant as the degree
                # if a1 >= degree and a2 <= modifieddegrees[i+1 if i <= 2 else 360]:# if the angle is between the two degrees (in one of the quadrants)
                #     addedcorners.add(degree)
                # # Next case is for when neither a1 or a2 are in the same quadrant as the degree, but the angle is still between the two angles
                # if a1 <= degree and a2 >= modifieddegrees[i+1 if i <= 2 else 0]:# if a1 is less than the degree and a2 is greater than the next degree
                #     addedcorners.add(degree)
                # # Next case is for when a2 is in the same quadrant as the degree, but a1 is not
                # if a2 >= degree and a2 <= modifieddegrees[i+1 if i <= 2 else 0]:# if a2 is between the degree and the next degree
                #     addedcorners.add(degree)

                # first case is for when both a1 and a2 are in the same quadrant as the degree
                    if a1 >= degree:
                        if a2 <= modifieddegrees[i+1 if i <= 2 else 0]:
                            addedcorners.add(degree)
                        elif modifieddegrees[i+1 if i <= 2 else 0] == 0 and a2 <= 360:
                            addedcorners.add(degree)
                    if a1 >= degree and a1 < degree+90:
                        # if a2 <= modifieddegrees[i+2 if i <= 1 else i+2-4]:
                        #     addedcorners.add(degree)
                        # elif modifieddegrees[i+2 if i <= 1 else i+2-4] == 0 and a2 <= 360:
                            addedcorners.add(degree)
                    # Next case is for when neither a1 or a2 are in the same quadrant as the degree, but the angle is still between the two angles
                    if a1 <= degree:
                        if i != 3 and a2 >= modifieddegrees[i+1 if i <= 2 else 0]:
                            addedcorners.add(degree)

                    # Next case is for when a2 is in the same quadrant as the degree, but a1 is not
                    if a2 >= degree:
                        if a2 <= modifieddegrees[i+1 if i <= 2 else 0]:
                            addedcorners.add(degree)
                        elif modifieddegrees[i+1 if i <= 2 else 0] == 0 and a2 <= 360:
                            addedcorners.add(degree)

            # the corners start at the top left and go clockwise
            # the list below [90,0,270,180] has the corresponding index of the degrees list to the corners list
            # I had to do the degrees.index because the modifieddegrees might not be the same as degrees since the list is shifted where the first degree inline with a1
            # dto_corner = lambda degree : corners[[90,0,270,180].index(degrees.index(degree))]

            dto_corner = lambda degree : corners[[90,0,270,180].index(degree)]
            for degree in addedcorners:
                points.insert(-2,dto_corner(degree))
            print(points,len(points))
            print(a1,a2,degrees,modifieddegrees,addedcorners,[[90,0,270,180].index(degree) for degree in addedcorners],'a1,a2,degrees,modifieddegrees,addedcorners')
            pygame.draw.polygon(screen, colors[colornum], points)

            

        surface = pygame.Surface((radius*2+10,radius*2+10))
        surface.fill((40,40,40))
        pygame.draw.circle(surface,(255,255,255),(radius,radius),radius)
        surface.set_colorkey((255,255,255))
        screen.blit(surface,coords)

        for colornum, (a1, a2,name) in enumerate(angles):
            p2 = (coords[0] + radius + radius * math.cos(a2), radius + coords[1] + (radius * math.sin(a2) * -1))# the second point on the circle - drawn after the corner points
            text = fontlist[35].render(f'{name}',(255,255,255))[0]
            screen.blit(text,(p2))

            # if angle <= 90:
            #     for i,degree in enumerate(degrees):
            #         # if a1 >= degree and a1 <= degrees[i+1 if i <= 2 else 0]:# if the angle is between the two degrees (in one of the quadrants)
            #         #     addedcorners.add(degree)
            #         # if a2 >= degree and a2 <= degrees[i+1 if i <= 2 else 0]:# if the angle is between the two degrees (in one of the quadrants)
            #         #     addedcorners.add(degree)


            # if p1[0] in [corner[0] for corner in corners]:# if the x value of p1 is the same as one of the corners
            #     # get the corners that have the same x value as p1, and get the one that is closest to p4
            #     in1 = [[corner[0],corner[1],abs(corner[0]-p2[0])] for corner in corners if corner[0] == p1[0]]#description above

            #     if in1[0][2] > in1[1][2]:# if the first corner is further away from p4 than the second corner
            #         in1 = in1[0]
            #     if in1[0][2] < in1[1][2]:
            #         in1 = in1[1]
            #     if in1[0][2] == in1[1][2]:
            #         in1 = in1[0] if p1[1] == in1[0][1] else in1[1]
            #     in1 = in1[0] if in1[0] > in1[1] else in1[1]

            # if p1[1] in [corner[1] for corner in corners]:  
                
                
            # in1 = corners.index(closest_point(p1, corners))
            # in2 = corners.index(closest_point(p2, corners))

            # print(in1,in2)

            # # for i in range(abs(in1-in2)):

            # #     points[-1].insert(i+2,corners[in1-i if in1+i > 0 else 3])
           
            # p3 = corners[corners.index(closest_point(p4, corners))]
            # p3 = corners[corners.index(closest_point(p1, corners)) - 1 if corners.index(closest_point(p1, corners)) > 0 else 3]

        # [[(850, 500), (950.0, 500.0), (950, 400), (750, 400), (759.4105706274706, 542.3503870815782), (850, 500)],
        #  [(850, 500), (759.4105706274706, 542.3503870815782), (750, 600), (950, 600), (950, 400), (846.9845282379142, 400.04547568993155), (850, 500)],
        #  [(850, 500), (846.9845282379142, 400.04547568993155), (750, 600), (950.0, 500.0), (850, 500)]] points
        # print(points,'points')
        


        
        # [(850, 500), (846.9845282379142, 400.04547568993155), (750, 400), (750, 600), (950.0, 500.0), (850, 500)]

        
        

    def draw_menu_content(self, screen: pygame.Surface, Mousebuttons: int, stocklist: list, player):
        mousex, mousey = pygame.mouse.get_pos()
        xshift = 14
        yshift = 150    

        self.bar.changemaxvalue(len(player.stocks))

        barheight = 520//len(player.stocks) if len(player.stocks) > 0 else 1

        self.bar.draw_bar(screen, [225, DY], [45, DY + (yshift*4) - 80], 'vertical', barwh=[42, barheight], shift=80, reversedscroll=True, text=True)
        
        

        for i,stock in enumerate([(stock) for i,stock in enumerate(player.stocks) if i >= self.bar.value and i < self.bar.value+5]):# draws the stock graph bar
            
            percentchange = ((stock[0].price - stock[1]) / stock[1]) * 100
            if percentchange > 0:
                grcolor = (0, 200, 0)
            elif percentchange == 0:
                grcolor = (200, 200, 200)
            else:
                grcolor = (225, 0, 0)

            # Rendering all the text
            nametext = fontlist[45].render(f'{stock[0]} X {stock[2]}', (190, 190, 190))[0]
            twidth = nametext.get_width() + 25

            boughttext = fontlist[35].render(f'Paid Price: ${stock[1]*stock[2]:,.2f}', grcolor)[0]
            pricetext = fontlist[35].render(f'Price: ${stock[0].price*stock[2]:,.2f}', grcolor)[0]
            twidth2 = max(boughttext.get_width(), pricetext.get_width()) + 30

            profittext = fontlist[35].render(f'Profit/Loss: ${(stock[0].price - stock[1])*stock[2]:,.2f}', grcolor)[0]
            percenttext = fontlist[35].render(f'Change %: {percentchange:,.2f}%', grcolor)[0]
            twidth3 = max(profittext.get_width(), percenttext.get_width()) + 45
            
            # find the points for the polygons
            points,points2,points3,totalpolyon = self.getpoints(twidth, twidth2, twidth3, (i * xshift), (i * yshift))

            # check if the mouse is hovering over the polygon
            hover = False
            if point_in_polygon((mousex, mousey), totalpolyon):  # check if mouse is inside the polygon
                hover = True

            polycolor = (30, 30, 30) if not hover else (60, 60, 60)

            # ----------draw the polygons----------
            gfxdraw.filled_polygon(screen, points, polycolor)  # draws the first polygon with the name of the stock
            gfxdraw.filled_polygon(screen, points2, (polycolor))  # draws the second polygon with the price of the stock
            gfxdraw.filled_polygon(screen, points3, (polycolor))  # draws the third polygon with the profit of the stock


            # ----------Draw the text----------
            screen.blit(nametext, (320 + (i * xshift), 235 + (i * yshift)))  # display name of stock
            screen.blit(boughttext, (330 + (i * xshift) + twidth, 210 + (i * yshift)))# display bought price of stock
            screen.blit(pricetext, (345 + (i * xshift) + twidth, 265 + (i * yshift)))# display current price of stock
            screen.blit(profittext, (330 + twidth + twidth2 + (i * xshift), 210 + (i * yshift)))# display profit of stock
            screen.blit(percenttext, (345 + twidth + twidth2 + (i * xshift), 265 + (i * yshift)))# display percent change of stock
            
            # top left, top right, bottom right, bottom left
            bottom_polygon = [[totalpolyon[0][0]+12, totalpolyon[0][1] + DH - 15], 
                                [totalpolyon[1][0], totalpolyon[1][1]], 
                                [totalpolyon[2][0], totalpolyon[2][1]], 
                                [totalpolyon[3][0], totalpolyon[3][1]],
                                [totalpolyon[3][0]-15, totalpolyon[3][1]],
                                [totalpolyon[3][0]-3, totalpolyon[3][1] + DH - 15],
                              ]
            if hover:
                if percentchange > 0:
                    bottomcolor = (0, 200, 0)
                elif percentchange == 0:
                    bottomcolor = (200, 200, 200)
                else:
                    bottomcolor = (200, 0, 0)
            else:
                if percentchange > 0:
                    bottomcolor = (0, 80, 0)
                elif percentchange == 0:
                    bottomcolor = (110, 110, 110)
                else:
                    bottomcolor = (80, 0, 0)

            pygame.draw.polygon(screen, bottomcolor, bottom_polygon)

            pygame.draw.polygon(screen, (0, 0, 0), points, 5)  # draw the outline of the polygon
            pygame.draw.polygon(screen, (0, 0, 0), points2, 5)  # draw the outline of the second polygon
            pygame.draw.polygon(screen, (0, 0, 0), points3, 5)  # draw the outline of the third polygon

        values = [(stock[0].price * stock[2], stock[0].name) for stock in player.stocks]
        names = set([stock[0].name for stock in player.stocks])
        values = [[sum([v[0] for v in values if v[1] == name]), name] for name in names]
        # print(values)
        self.draw_pie_chart(screen, values, 200,(1100, 200))
