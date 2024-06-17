import pygame, math
from pygame import gfxdraw
from functools import lru_cache 
from Defs import *
from Classes.imports.Latterscroll import LatterScroll


@lru_cache(maxsize=10)
def createbacksurf(radius):
    backsurface = pygame.Surface((radius * 2 + 10, radius * 2 + 10))
    backsurface.fill((0, 0, 0))
    pygame.draw.circle(backsurface, (255, 255, 255), (radius, radius), radius)
    backsurface.set_colorkey((255, 255, 255))
    return backsurface

class PieChart:
    def __init__(s,radius,coords,menuList):
        s.data = []
        s.menuList = menuList
        s.radius = radius
        s.coords = coords
        # s.menuIcons = [pygame.image.load(f'Assets/Menu_Icons/{icon}.png').convert_alpha() for icon in ['stockbook','portfolio','option3']]# the icons for the menu
        s.menuIcons = [menu.icon for menu in menuList]
        for i in range(len(s.menuIcons)):
            s.menuIcons[i] = pygame.transform.scale(s.menuIcons[i],(70,40))
        s.pieSegments = []#[[color,points,value]...]
        s.angles = []
        s.lscroll = LatterScroll()
        s.selectedAssetIndex = 0
    def checkMenuList(s):
        """Unfortuanly menulist isn't always complete when the init is called, so this function is used to update the menuIcons list"""
        if len(s.menuList) != len(s.menuIcons):
            s.menuIcons = [menu.icon for menu in s.menuList]
            for i in range(len(s.menuIcons)):
                s.menuIcons[i] = pygame.transform.scale(s.menuIcons[i],(50,50))
    
    def updateData(s, data, coords=None, radius=None):
        """
        Updates the Data for the pie chart
        Data is a list of tuples, each tuple is (value, name, color)
        Should Usually just use the original coords and radius, but the coords and radius parameters can be used
        """
        s.checkMenuList()# check if the menuIcons list is up to date

        s.coords = s.coords if coords == None else coords# if coords is None, then keep the original coords
        s.radius = s.radius if radius == None else radius# if radius is None, then keep the original radius

        s.data = data
        s.pieSegments.clear()

        total = sum([v[0] for v in s.data])# get the total value of the stocks

        # percentages is a list of lists, each list is [percentage, name, color, actual value]
        percentages = [[round((value[0]) / total,4)*100,value[1],value[2],value[0]] for value in s.data]

        other = [0,'Other',(255,255,0),0]

        for i in range(len(percentages)-1,-1,-1):
            if percentages[i][0] < 3:# if the percentage is less than 5%, then add it to the ""other"" category
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

        for a1, a2, value, name, color in s.angles:# loop through the angles
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
            s.pieSegments.append([color,[(x[0]-s.coords[0],x[1]-s.coords[1]) for x in points],value,name])
    

    def draw(s,screen:pygame.Surface):
        """"""        
        totalValue = sum([v[0] for v in s.data])# originally the displayed value is the total value of the stocks - might change if mouseover

        wholesurf = pygame.Surface((s.radius*2,s.radius*2))

        mousex,mousey = pygame.mouse.get_pos()


        def drawInfoBox(pieSegment):
            """Draws the information box to the right of the pie chart"""	
            color,points,value,name = pieSegment
            corners = [s.coords, (s.coords[0] + s.radius*2, s.coords[1]), (s.coords[0] + s.radius*2, s.coords[1] + s.radius*2), (s.coords[0], s.coords[1] + s.radius*2)]
        
            # Displaying the information in the box to the right of the pie chart
            boxRect = pygame.rect.Rect(corners[0][0]+s.radius*2+10,corners[0][1],s.radius*1.75,s.radius*2)
            pygame.draw.rect(screen, (0,0,0), boxRect, 5, 10)

            nameText,percentText = s_render(name,45,color), s_render(f'{limit_digits((value/totalValue)*100,16)}% of Portfolio',40,(110,110,110))
            nameH,nameW = nameText.get_height(),nameText.get_width()
            
            screen.blit(nameText, (boxRect.centerx-(nameW/2), boxRect.y+10))
            pygame.draw.rect(screen, (0,0,0), (boxRect.x,boxRect.y+nameH+15,boxRect.width,5))# draw the line under the name
            screen.blit(percentText, (boxRect.centerx-(percentText.get_width()/2), boxRect.y+20+nameH+10))
            if name == "Cash" or name == "Other":
                return
            nameList = ["Buy","Sell","Speculate"]
            for i,image in enumerate(s.menuIcons):
                y = boxRect.y+nameH+percentText.get_height()+40+(i*65)
                screen.blit(image, (boxRect.x+15, y+5))
                screen.blit(s_render(nameList[i],50,(1,1,1)), (boxRect.x+85, y+10))
                myRect = pygame.rect.Rect(boxRect.x+10,y,boxRect.width-20,60)
                if myRect.collidepoint(mousex,mousey):
                    pygame.draw.rect(screen, (0,0,0), myRect, 3, 5)
                    if pygame.mouse.get_pressed()[0]:
                        # menulist is stockbook,portfolio,optiontrade
                        for menu in s.menuList:
                            menu.menudrawn = False
                        s.menuList[i].menudrawn = True
                        if i == 0:# if the stockbook is clicked, then set the selected asset to the one the mouse is over
                            s.menuList[0].changeSelectedStock(name=name[:4])
                        if i == 1:# if the portfolio is clicked, then set the selected asset to the one the mouse is over
                            s.menuList[1].selectedAsset = s.menuList[1].findAsset(value,name)

        
        if pygame.Rect(s.coords[0],s.coords[1],s.radius*2,s.radius*2).collidepoint(mousex,mousey):# if the mouse is in the pie chart
            collided = False
            for i,(color,points,value,name) in enumerate(s.pieSegments):# loop through the pie segments
                if point_in_polygon((mousex-s.coords[0],mousey-s.coords[1]),points):# set collided to the one the mouse is over
                    collided = i
                    if pygame.mouse.get_pressed()[0]:# if the mouse is clicked, then set the selected asset to the one the mouse is over
                        s.selectedAssetIndex = i

            for i,(color,points,value,name) in enumerate(s.pieSegments):# draws all the segments darker except the one the mouse is over
                newcolor = (color[0]//2,color[1]//2,color[2]//2) if i != collided else color
                gfxdraw.filled_polygon(wholesurf,points,newcolor)#draws the none selected polygon darker


            value = s.pieSegments[collided][2]# the value of the stock the mouse is over
            drawBoxedText(wholesurf, f'${limit_digits(value,16)}',50,s.pieSegments[collided][0],(1,1,1),(s.radius,s.radius))# blit the value of the mouseover segement to the screen

        else:
            for color,points,value,name in s.pieSegments: 
                gfxdraw.filled_polygon(wholesurf,points,color)

            # if the mouse isn't over any of the segments, then display the total value    
            drawBoxedText(wholesurf, f'${limit_digits(totalValue,16)}',50,(0,170,0),(1,1,1),(s.radius,s.radius))# blit the value of the mouseover segement to the screen    

        if s.selectedAssetIndex != None:
            if s.selectedAssetIndex >= len(s.pieSegments):
                s.selectedAssetIndex = 0
            drawInfoBox(s.pieSegments[s.selectedAssetIndex])# draw the information box to the right of the pie chart
        wholesurf.blit(createbacksurf(s.radius), (0,0))  # blit the backsurface to the screen
        wholesurf.set_colorkey((0,0,0))
        screen.blit(wholesurf, s.coords)
        
        pygame.draw.circle(screen, (0, 0, 0), (s.coords[0]+s.radius,s.coords[1]+s.radius), s.radius, 10)
