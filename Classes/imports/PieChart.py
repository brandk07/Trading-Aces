import pygame, math
from pygame import gfxdraw
from functools import lru_cache 
from Defs import s_render, fontlist,point_in_polygon


@lru_cache(maxsize=10)
def createbacksurf(radius):
    backsurface = pygame.Surface((radius * 2 + 10, radius * 2 + 10))
    backsurface.fill((0, 0, 0))
    pygame.draw.circle(backsurface, (255, 255, 255), (radius, radius), radius)
    backsurface.set_colorkey((255, 255, 255))
    return backsurface

class PieChart:
    def __init__(s,radius,coords):
        s.data = []
        s.radius = radius
        s.coords = coords
        s.pieSegments = []#[[color,points,value]...]
        s.angles = []
    
    def updateData(s, data, coords=None, radius=None):
        """
        Updates the Data for the pie chart
        Data is a list of tuples, each tuple is (value, name, color)
        Should Usually just use the original coords and radius, but the coords and radius parameters can be used
        """
        if coords != None:
            s.coords = coords
        if radius != None:
            s.radius = radius
        s.data = data
        s.pieSegments.clear()

        total = sum([v[0] for v in s.data])# get the total value of the stocks

        # percentages is a list of lists, each list is [percentage, name, color, actual value]
        percentages = [[round((value[0]) / total,4)*100,value[1],value[2],value[0]] for value in s.data]

        other = [0,'Other',(255,255,0),0]

        for i in range(len(percentages)-1,-1,-1):
            if percentages[i][0] < 5:# if the percentage is less than 5%, then add it to the ""other"" category
                other[0] += percentages[i][0]
                other[3] += percentages[i][3]
                percentages.remove(percentages[i])

        if other[0] > 0:# if there is an other category, then add it to the list
            percentages.append(other)
        percentages.sort(key=lambda x:x[0],reverse=True)
        percentindex = math.radians(0)
        
        s.angles.clear()
        for i,percent in enumerate(percentages):# loop through the percentages and get the angles
            s.angles.append([math.radians(percentindex)])# the first angle is the previous angle
            percentindex += (percent[0]/100)*360
            s.angles[i].append(math.radians(percentindex))# the second angle is the current angle

            s.angles[i].extend([percent[3], percent[1],percent[2]])# the value, name and color
            

        corners = [s.coords, (s.coords[0] + s.radius*2, s.coords[1]), (s.coords[0] + s.radius*2, s.coords[1] + s.radius*2), (s.coords[0], s.coords[1] + s.radius*2)]
        
        points = []

        for colornum, (a1, a2, value, name, color) in enumerate(s.angles):# loop through the angles
            p0 = (s.coords[0] + s.radius, s.coords[1]+s.radius)
            p1 = (s.coords[0] + s.radius + s.radius * math.cos(a1), s.radius + s.coords[1] + (s.radius * math.sin(a1) * -1))# the first point on the circle
            p2 = (s.coords[0] + s.radius + s.radius * math.cos(a2), s.radius + s.coords[1] + (s.radius * math.sin(a2) * -1))# the second point on the circle - drawn after the corner points
            points = [p0, p1, p2, p0]# put the first points in the list, more points will be added in between p1 and p2

            addedcorners = set()
            a1 = int(math.degrees(a1))
            a2 = int(math.degrees(a2))

            num = int((a1//90)*90)
            modifieddegrees = [(degree+num if degree+num < 360 else degree+num-360) for degree in [0,90,180,270]]# the degrees but shifted so that the first degree (relative to a1) is 0
            for i,degree in enumerate(modifieddegrees):
                # checking the possible cases for when the angle is between the two angles
                if a1 >= degree and a1 < degree+90:
                        addedcorners.add(degree)
                # Next case is for when neither a1 or a2 are in the same quadrant as the degree, but the angle is still between the two angles
                if a1 <= degree:
                    if i != 3 and a2 >= degree+90:
                        addedcorners.add(degree)
                # Next case is for when a2 is in the same quadrant as the degree, but a1 is not
                if a2 >= degree:
                    if a2 <= modifieddegrees[i+1 if i <= 2 else 0]:
                        addedcorners.add(degree)
                    elif modifieddegrees[i+1 if i <= 2 else 0] == 0 and a2 <= 360:
                        addedcorners.add(degree)

            # the corners start at the top left and go clockwise
            # the list below [90,0,270,180] has the corresponding index of the degrees list to the corners list
            dto_corner = lambda degree : corners[[90,0,270,180].index(degree)]
            for degree in addedcorners:
                points.insert(-2,dto_corner(degree))
            # draw the polygon
            # pygame.draw.polygon(wholesurf, color, [(x[0]-coords[0],x[1]-coords[1]) for x in points]) 
            s.pieSegments.append([color,[(x[0]-s.coords[0],x[1]-s.coords[1]) for x in points],value])
    

    def draw(s,screen):
        """"""        
        total = sum([v[0] for v in s.data])# get the total value of the stocks - does this is update too, but I didn't feel the need to make another attribute for it

        wholesurf = pygame.Surface((s.radius*2,s.radius*2))

        mousex,mousey = pygame.mouse.get_pos()

        # for color,points in s.pieSegments:
        #     if point_in_polygon((mousex,mousey),points):
        if pygame.Rect(s.coords[0],s.coords[1],s.radius*2,s.radius*2).collidepoint(mousex,mousey):# if the mouse is in the pie chart
            for color,points,value in s.pieSegments:
                # print(point_in_polygon((mousex-s.coords[0],mousey-s.coords[1]),ps),color, (mousex,mousey))
                if point_in_polygon((mousex-s.coords[0],mousey-s.coords[1]),points):
                    gfxdraw.filled_polygon(wholesurf,points,color)#draws the graphed points of the graph
                    total = value
                else:
                    grayscale = lambda r,g,b : (r+g+b)//3
                    graycolor = (grayscale(*color),grayscale(*color),grayscale(*color))
                    gfxdraw.filled_polygon(wholesurf,points,graycolor)#draws the none selected polygon darker
        else:
            for color,points,value in s.pieSegments:
                gfxdraw.filled_polygon(wholesurf,points,color)

        wholesurf.blit(createbacksurf(s.radius), (0,0))  # blit the backsurface to the screen
        wholesurf.set_colorkey((0,0,0))
        screen.blit(wholesurf, s.coords)
        starpos = s.coords[1]+(((((s.radius*2))-(len(s.angles)*30))//2))

        corners = [s.coords, (s.coords[0] + s.radius*2, s.coords[1]), (s.coords[0] + s.radius*2, s.coords[1] + s.radius*2), (s.coords[0], s.coords[1] + s.radius*2)]
        #  drawing the boxes displaying the colors next to the names
        for i, (a1, a2, value, name,color) in enumerate(s.angles):
            c = corners[1]
            cx = c[0]
            cy = starpos
            box_x = cx + 10
            box_y = cy + (i * 30)
            box_width = 15
            box_height = 15
            gfxdraw.filled_polygon(screen, [(box_x, box_y), (box_x + box_width, box_y), (box_x + box_width, box_y + box_height), (box_x, box_y + box_height)], color)

        # rendering and blitting the text
        renderedtext = [[s_render(f'{name}' if type(name) == str else{f'{name:,.2f}'},35,(255,255,255)),name] for (*_, name,color) in (s.angles)]
        for i,text in enumerate(renderedtext):
            text_x = cx + 30
            text_y = starpos -5 + (i * 30)
            screen.blit(text[0], (text_x, text_y)) 
        # draw a circle in the middle of the pie chart
        pygame.draw.circle(screen, (0, 0, 0), (s.coords[0]+s.radius,s.coords[1]+s.radius), s.radius, 10)
        totaltext = fontlist[45].render(f'${total:,.2f}', (0, 0, 0))[0]
        renderedtext.append([totaltext,f'${total:,.2f}'])
        screen.blit(totaltext, (corners[0][0]+s.radius-(totaltext.get_width()/2), corners[0][1]+s.radius-(totaltext.get_height()/2)))

# @lru_cache(maxsize=10)
# def createbacksurf(radius):
#     backsurface = pygame.Surface((radius * 2 + 10, radius * 2 + 10))
#     backsurface.fill((0, 0, 0))
#     pygame.draw.circle(backsurface, (255, 255, 255), (radius, radius), radius)
#     backsurface.set_colorkey((255, 255, 255))
#     return backsurface
# def draw_pie_chart(screen: pygame.Surface, values:list, radius, coords):
#         """Draws the pie chart for the portfolio menu. value is (value, name, color)"""
#         # the polygons are blit to this, then the backsurface is blit, then the backsurface is turned transparent and wholesurf is blit to the screen
#         wholesurf = pygame.Surface((radius*2,radius*2))

#         total = sum([v[0] for v in values])# get the total value of the stocks
#         percentages = [[round((value[0]) / total,4)*100,value[1],value[2]] for value in values]

#         other = [0,'Other',(255,255,0)]

#         for i in range(len(percentages)-1,-1,-1):
#             if percentages[i][0] < 5:# if the percentage is less than 5%, then add it to the ""other"" category
#                 other[0] += percentages[i][0]
#                 percentages.remove(percentages[i])

#         if other[0] > 0:# if there is an other category, then add it to the list
#             percentages.append(other)
#         percentages.sort(key=lambda x:x[0],reverse=True)
#         percentindex = math.radians(0)
        
#         angles = []
#         for i,percent in enumerate(percentages):# loop through the percentages and get the angles
#             angles.append([math.radians(percentindex)])# the first angle is the previous angle
#             percentindex += (percent[0]/100)*360
#             angles[i].append(math.radians(percentindex))# the second angle is the current angle
#             angles[i].append(percent[1])# the name
#             angles[i].append(percent[2])# the color

#         corners = [coords, (coords[0] + radius*2, coords[1]), (coords[0] + radius*2, coords[1] + radius*2), (coords[0], coords[1] + radius*2)]
        
#         points = []

#         for colornum, (a1, a2,name,color) in enumerate(angles):# loop through the angles
#             p0 = (coords[0] + radius, coords[1]+radius)
#             p1 = (coords[0] + radius + radius * math.cos(a1), radius + coords[1] + (radius * math.sin(a1) * -1))# the first point on the circle
#             p2 = (coords[0] + radius + radius * math.cos(a2), radius + coords[1] + (radius * math.sin(a2) * -1))# the second point on the circle - drawn after the corner points
#             points = [p0, p1, p2, p0]# put the first points in the list, more points will be added in between p1 and p2

#             addedcorners = set()
#             a1 = int(math.degrees(a1))
#             a2 = int(math.degrees(a2))

#             num = int((a1//90)*90)
#             modifieddegrees = [(degree+num if degree+num < 360 else degree+num-360) for degree in [0,90,180,270]]# the degrees but shifted so that the first degree (relative to a1) is 0
#             for i,degree in enumerate(modifieddegrees):
#                 # checking the possible cases for when the angle is between the two angles
#                 if a1 >= degree and a1 < degree+90:
#                         addedcorners.add(degree)
#                 # Next case is for when neither a1 or a2 are in the same quadrant as the degree, but the angle is still between the two angles
#                 if a1 <= degree:
#                     if i != 3 and a2 >= degree+90:
#                         addedcorners.add(degree)
#                 # Next case is for when a2 is in the same quadrant as the degree, but a1 is not
#                 if a2 >= degree:
#                     if a2 <= modifieddegrees[i+1 if i <= 2 else 0]:
#                         addedcorners.add(degree)
#                     elif modifieddegrees[i+1 if i <= 2 else 0] == 0 and a2 <= 360:
#                         addedcorners.add(degree)

#             # the corners start at the top left and go clockwise
#             # the list below [90,0,270,180] has the corresponding index of the degrees list to the corners list
#             dto_corner = lambda degree : corners[[90,0,270,180].index(degree)]
#             for degree in addedcorners:
#                 points.insert(-2,dto_corner(degree))
#             # draw the polygon
#             pygame.draw.polygon(wholesurf, color, [(x[0]-coords[0],x[1]-coords[1]) for x in points])            


#         wholesurf.blit(createbacksurf(radius), (0,0))  # blit the backsurface to the screen
#         wholesurf.set_colorkey((0,0,0))
#         screen.blit(wholesurf, coords)
#         starpos = coords[1]+(((((radius*2))-(len(angles)*30))//2))
#         #  drawing the boxes displaying the colors next to the names
#         for i, (a1, a2, name,color) in enumerate(angles):
#             c = corners[1]
#             cx = c[0]
#             cy = starpos
#             box_x = cx + 10
#             box_y = cy + (i * 30)
#             box_width = 15
#             box_height = 15
#             gfxdraw.filled_polygon(screen, [(box_x, box_y), (box_x + box_width, box_y), (box_x + box_width, box_y + box_height), (box_x, box_y + box_height)], color)

#         # rendering and blitting the text
        
#         renderedtext = [[s_render(f'{name}' if type(name) == str else{f'{name:,.2f}'},35,(255,255,255)),name] for (*_, name,color) in (angles)]
#         for i,text in enumerate(renderedtext):
#             text_x = cx + 30
#             text_y = starpos -5 + (i * 30)
#             screen.blit(text[0], (text_x, text_y)) 
#         # draw a circle in the middle of the pie chart
#         pygame.draw.circle(screen, (0, 0, 0), (coords[0]+radius,coords[1]+radius), radius, 10)
#         totaltext = fontlist[45].render(f'${total:,.2f}', (0, 0, 0))[0]
#         renderedtext.append([totaltext,f'${total:,.2f}'])
#         screen.blit(totaltext, (corners[0][0]+radius-(totaltext.get_width()/2), corners[0][1]+radius-(totaltext.get_height()/2)))
