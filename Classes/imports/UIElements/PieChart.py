import pygame, math
from pygame import gfxdraw
from functools import lru_cache 
from Defs import *
from Classes.imports.UIElements.Latterscroll import LatterScroll


@lru_cache(maxsize=10)
def createbacksurf(radius):
    backsurface = pygame.Surface((radius * 2 + 10, radius * 2 + 10))
    backsurface.fill((0, 0, 0))
    pygame.draw.circle(backsurface, (255, 255, 255), (radius, radius), radius)
    backsurface.set_colorkey((255, 255, 255))
    return backsurface
import pygame, math
from pygame import gfxdraw
from functools import lru_cache 
from Defs import *
from Classes.imports.UIElements.Latterscroll import LatterScroll


@lru_cache(maxsize=10)
def createbacksurf(radius):
    backsurface = pygame.Surface((radius * 2 + 10, radius * 2 + 10))
    backsurface.fill((0, 0, 0))
    pygame.draw.circle(backsurface, (255, 255, 255), (radius, radius), radius)
    backsurface.set_colorkey((255, 255, 255))
    return backsurface

class PieChart:
    def __init__(self,coords,wh):
        """The wh will calculate the max radius that won't go out of wh"""
        self.data = []
        self.wh = wh
        self.radius = min(self.wh[0]//2,(self.wh[1]-115)//2)# Starts with the radius based on 1 line of bottom text (If there are too many elements then it will be decreased by updateRadius method)
        self.coords = coords
        self.numlines = 1
        self.pieSegments = []#[[color,points,value]...]
        self.angles = []
        self.lscroll = LatterScroll()
        self.selectedAssetIndex = None
        self.boxtextsize = int(getTSizeNums(f'50.00% of Portfolio',self.radius*1.75)*.9)

    def updateRadius(self,NumBottomLines):
        """Updates the radius of the pie chart"""
        extraAmt = 50*NumBottomLines
        self.radius = min(self.wh[0]//2,(self.wh[1]-60-extraAmt)//2)
        


    def updateData(self, data, coords=None, radius=None):
        """
        Updates the Data for the pie chart
        Data is a list of tuples, each tuple is (value, name, color)
        Should Usually just use the original coords and radius, but the coords and radius parameters can be used
        """

        self.coords = self.coords if coords == None else coords# if coords is None, then keep the original coords
        self.radius = self.radius if radius == None else radius# if radius is None, then keep the original radius

        self.data = data
        self.pieSegments.clear()

        total = sum([v[0] for v in self.data])# get the total value of the stocks

        # percentages is a list of lists, each list is [percentage, name, color, actual value]
        percentages = [[round((value[0]) / total,4)*100,value[1],value[2],value[0]] for value in self.data]

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
        
        self.angles.clear()
        for i,percent in enumerate(percentages):# loop through the percentages and get the angles
            self.angles.append([math.radians(percentindex)])# the first angle is the previous angle
            percentindex += (percent[0]/100)*360
            self.angles[i].append(math.radians(percentindex))# the second angle is the current angle
            self.angles[i].extend([percent[3], percent[1],percent[2]])# the value, name and color
            
        corners = [self.coords, (self.coords[0] + self.radius*2, self.coords[1]), (self.coords[0] + self.radius*2, self.coords[1] + self.radius*2), (self.coords[0], self.coords[1] + self.radius*2)]
        
        points = []

        for a1, a2, value, name, color in self.angles:# loop through the angles
            p0 = (self.coords[0] + self.radius, self.coords[1]+self.radius)
            p1 = (self.coords[0] + self.radius + self.radius * math.cos(a1), self.radius + self.coords[1] + (self.radius * math.sin(a1) * -1))# the first point on the circle
            p2 = (self.coords[0] + self.radius + self.radius * math.cos(a2), self.radius + self.coords[1] + (self.radius * math.sin(a2) * -1))# the second point on the circle - drawn after the corner points
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
            self.pieSegments.append([color,[(x[0]-self.coords[0],x[1]-self.coords[1]) for x in points],value,name])
    
    def getClickedAsset(self,mousebuttons):
        """Gets the asset that the mouse is over"""
        mousex,mousey = pygame.mouse.get_pos()

        collided = False
        for i,(color,points,value,name) in enumerate(self.pieSegments):# loop through the pie segments
            if point_in_polygon((mousex-self.coords[0],mousey-self.coords[1]-60),points):# set collided to the one the mouse is over
                collided = i
                if mousebuttons == 1:# if the mouse is clicked, then set the selected asset to the one the mouse is over
                    if self.selectedAssetIndex == i:
                        self.selectedAssetIndex = None
                    else:
                        self.selectedAssetIndex = i
                return collided
        return collided

    def drawOutline(self,pieSurf:pygame.Surface):
        for color,points,value,name in self.pieSegments:
            pygame.draw.line(pieSurf,(1,1,1),(self.radius,self.radius),points[1],5)

    def drawBottomNames(self,wholeSurf:pygame.Surface,mousebuttons:int,txtSize):
        numNames = len(self.pieSegments)
        nameRenders = [s_render(name, txtSize, color) for i,(color,points,value,name) in enumerate(self.pieSegments)]
        numLines = 0
        spaceings = []
        lastXOffset = 0# The offset for the last line- if it has less than qtyPerLine
        # print('numNames:',numNames,self.pieSegments)
        while not spaceings or max(spaceings) < 10:
            # print(spaceings)
            numLines += 1
            qtyPerLine = math.ceil(numNames/numLines)
            lastXOffset = 0
            spaceings.clear()
            # print('numLines:',numLines)
            if numLines > numNames:
                self.updateRadius(0)
                return
            for i in range(numLines):
                
                start,stop = i*qtyPerLine,(((i+1)*qtyPerLine) if (i+1)*qtyPerLine < numNames else numNames)
                # print('start,stop:',start,stop,i,qtyPerLine,numNames)
                totalWidth = (sum([render.get_width() for render in nameRenders[start:stop]])+(15*(stop-start)))# technically qtyperline isn't right since it could be less for last one if I want to fix it
                
                spaceings.append(((self.radius*2)-totalWidth-10)/(stop-start))
                
                if (stop-start) != qtyPerLine:# Only for last line if it has less qtyPerLine
                    spaceings[-1] = spaceings[-2]
                    lastXOffset = ((self.radius*2)-(totalWidth+(spaceings[-1]*(stop-start))-10))//2
            


            
        currentWidth = 5

        if self.numlines != numLines:
            self.numlines = numLines
            self.updateRadius(numLines)
    
        place = 0
        for i in range(numLines):
            ylevel = self.radius*2+100+((nameRenders[0].get_height()+15)*i)
            xOff = lastXOffset if i == numLines-1 else 0
            for _ in range(qtyPerLine):
                if place >= numNames: break
                w,h = nameRenders[place].get_width(),nameRenders[place].get_height()
                pygame.draw.rect(wholeSurf,self.pieSegments[place][0],(xOff+currentWidth,ylevel,10,10))

                drawCenterRendered(wholeSurf, nameRenders[place], (xOff+currentWidth+15, ylevel), centerX=False, centerY=True)
                rect = pygame.Rect(xOff+self.coords[0]+currentWidth-3,self.coords[1]+ylevel-10,23+w,h+4)

                if (n:=rect.collidepoint(*pygame.mouse.get_pos())) or place == self.selectedAssetIndex:
                    pygame.draw.line(wholeSurf,(255,255,255),(xOff+currentWidth,ylevel+15),(xOff+currentWidth+23+w,ylevel+15),3)
                    if n and mousebuttons == 1:
                        if self.selectedAssetIndex == place:
                            self.selectedAssetIndex = None
                        else:
                            self.selectedAssetIndex = place

                place += 1
                currentWidth += w+spaceings[i]+15
            currentWidth = 5

            
        #     for j in range(len(nameRenders[i])):
        #         pygame.draw.rect(wholeSurf,self.pieSegments[i],(currentWidth,self.radius*2+100,10,10))

        #         drawCenterRendered(wholeSurf, nameRenders[i], (currentWidth+15, self.radius*2+100), centerX=False, centerY=True)
        #         rect = pygame.Rect(self.coords[0]+currentWidth-3,self.coords[1]+self.radius*2+90,23+nameRenders[i].get_width(),nameRenders[i].get_height()+4)

        #         if (n:=rect.collidepoint(*pygame.mouse.get_pos())) or i == self.selectedAssetIndex:
        #             pygame.draw.line(wholeSurf,(255,255,255),(currentWidth,self.radius*2+120),(currentWidth+23+nameRenders[i].get_width(),self.radius*2+120),3)
        #             if n and mousebuttons == 1:
        #                 self.selectedAssetIndex = i                

        #         currentWidth += nameRenders[i].get_width()+spaceing+15

    def draw(self,screen:pygame.Surface,title:str,mousebuttons:int,txtSize=35):
        """"""        
        totalValue = sum([v[0] for v in self.data])# originally the displayed value is the total value of the stocks - might change if mouseover

        
        wholeSurf = pygame.Surface((self.wh[0],self.wh[1]))
        self.drawBottomNames(wholeSurf,mousebuttons,txtSize)
        pieSurf = pygame.Surface((self.radius*2,self.radius*2))

       
        
        if pointInCircle(pygame.mouse.get_pos(),(self.coords[0]+self.radius,self.coords[1]+60+self.radius),self.radius-10):# if the mouse is in the pie chart
            collided = self.getClickedAsset(mousebuttons)# get the asset that the mouse is over

            for i,(color,points,value,name) in enumerate(self.pieSegments):# draws all the segments darker except the one the mouse is over
                newcolor = brightenCol(color,0.5) if i != collided else brightenCol(color,1.5)
                gfxdraw.filled_polygon(pieSurf,points,newcolor)#draws the none selected polygon darker
            self.drawOutline(pieSurf)

            value = self.pieSegments[collided][2]# the value of the stock the mouse is over
            drawBoxedText(pieSurf, f'${limit_digits(value,16)}',50,self.pieSegments[collided][0],(1,1,1),(self.radius,self.radius))# blit the value of the mouseover segement to the screen

        else:
            if self.selectedAssetIndex != None:
                if self.selectedAssetIndex >= len(self.pieSegments):
                    self.selectedAssetIndex = None
                else:
                    for i,(color,points,value,name) in enumerate(self.pieSegments):# draws all the segments darker except the one the mouse is over
                        newcolor = brightenCol(color,0.5) if i != self.selectedAssetIndex else brightenCol(color,1.5)
                        gfxdraw.filled_polygon(pieSurf,points,newcolor)#draws the none selected polygon darker
                    self.drawOutline(pieSurf)
                    drawBoxedText(pieSurf, f'${limit_digits(self.pieSegments[self.selectedAssetIndex][2],16)}',50,self.pieSegments[self.selectedAssetIndex][0],(1,1,1),(self.radius,self.radius))# blit the value of the mouseover segement to the screen                
            
            else:# if the mouse isn't over any of the segments, then display the total value
                for color,points,value,name in self.pieSegments: 
                    gfxdraw.filled_polygon(pieSurf,points,color)
                self.drawOutline(pieSurf)
                drawBoxedText(pieSurf, f'${limit_digits(totalValue,16)}',50,(90,90,90),(1,1,1),(self.radius,self.radius))# blit the value of the mouseover segement to the screen

        
        

        titleText = s_render(title, 65, (200, 200, 200))
        drawCenterRendered(wholeSurf,  titleText, (self.radius, 0), centerX=True, centerY=False)# Blit the title to the screen
        # draw the line under the title
        pygame.draw.line(wholeSurf, (200, 200, 200), (self.radius - titleText.get_width()//2, titleText.get_height()+5), (self.radius + titleText.get_width()//2, titleText.get_height()+5), 4)

        pieSurf.blit(createbacksurf(self.radius), (0,0))  # blit the backsurface to the screen
        pieSurf.set_colorkey((0,0,0))
        pygame.draw.circle(pieSurf, (1, 1, 1), (self.radius,self.radius), self.radius, 10)
        # screen.blit(pieSurf, self.coords)
        wholeSurf.blit(pieSurf,(0,70))
        wholeSurf.set_colorkey((0,0,0))
        
        

        screen.blit(wholeSurf,self.coords)
        


class PieChartSideInfo:

    def __init__(self,radius,coords):
        self.data = []
        # self.menuDict = menuDict
        self.radius = radius
        self.coords = coords
        # self.menuIcons = [pygame.image.load(f'Assets/Menu_Icons/{icon}.png').convert_alpha() for icon in ['stockbook','portfolio','option3']]# the icons for the menu
        self.menuIcons = {}# needs to be updated in the checkmenuDict method

        self.pieSegments = []#[[color,points,value]...]
        self.angles = []
        self.lscroll = LatterScroll()
        self.selectedAssetIndex = 0
    # def checkmenuDict(self):
    #     """Unfortunately menuDict isn't always complete when the init is called, so this function is used to update the menuIcons list"""
    #     if len(self.menuIcons) != 4:
            
    #         self.menuIcons = {name:menu.icon for (name,menu) in self.menuDict.items() if name in ['Stockbook','Options','Portfolio','Bank']}# get the icons for the menu

    #         # for  in range(len(self.menuIcons)):
    #         for name in list(self.menuIcons):
    #             self.menuIcons[name] = pygame.transform.scale(self.menuIcons[name],(50,50))
    
    def updateData(self, data, coords=None, radius=None):
        """
        Updates the Data for the pie chart
        Data is a list of tuples, each tuple is (value, name, color)
        Should Usually just use the original coords and radius, but the coords and radius parameters can be used
        """
        # self.checkmenuDict()# check if the menuIcons list is up to date

        self.coords = self.coords if coords == None else coords# if coords is None, then keep the original coords
        self.radius = self.radius if radius == None else radius# if radius is None, then keep the original radius

        self.data = data
        self.pieSegments.clear()

        total = sum([v[0] for v in self.data])# get the total value of the stocks

        # percentages is a list of lists, each list is [percentage, name, color, actual value]
        percentages = [[round((value[0]) / total,4)*100,value[1],value[2],value[0]] for value in self.data]

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
        
        self.angles.clear()
        for i,percent in enumerate(percentages):# loop through the percentages and get the angles
            self.angles.append([math.radians(percentindex)])# the first angle is the previous angle
            percentindex += (percent[0]/100)*360
            self.angles[i].append(math.radians(percentindex))# the second angle is the current angle
            self.angles[i].extend([percent[3], percent[1],percent[2]])# the value, name and color
            
        corners = [self.coords, (self.coords[0] + self.radius*2, self.coords[1]), (self.coords[0] + self.radius*2, self.coords[1] + self.radius*2), (self.coords[0], self.coords[1] + self.radius*2)]
        
        points = []

        for a1, a2, value, name, color in self.angles:# loop through the angles
            p0 = (self.coords[0] + self.radius, self.coords[1]+self.radius)
            p1 = (self.coords[0] + self.radius + self.radius * math.cos(a1), self.radius + self.coords[1] + (self.radius * math.sin(a1) * -1))# the first point on the circle
            p2 = (self.coords[0] + self.radius + self.radius * math.cos(a2), self.radius + self.coords[1] + (self.radius * math.sin(a2) * -1))# the second point on the circle - drawn after the corner points
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
            self.pieSegments.append([color,[(x[0]-self.coords[0],x[1]-self.coords[1]) for x in points],value,name])
    

    def draw(self,screen:pygame.Surface,mousebuttons:int,screenManager):
        """"""        
        totalValue = sum([v[0] for v in self.data])# originally the displayed value is the total value of the stocks - might change if mouseover

        wholesurf = pygame.Surface((self.radius*2,self.radius*2))

        mousex,mousey = pygame.mouse.get_pos()


        def drawInfoBox(pieSegment,mousebuttons):
            """Draws the information box to the right of the pie chart"""	
            color,points,value,name = pieSegment
            corners = [self.coords, (self.coords[0] + self.radius*2, self.coords[1]), (self.coords[0] + self.radius*2, self.coords[1] + self.radius*2), (self.coords[0], self.coords[1] + self.radius*2)]
        
            # Displaying the information in the box to the right of the pie chart
            boxRect = pygame.rect.Rect(corners[0][0]+self.radius*2+10,corners[0][1],self.radius*1.75,self.radius*2)
            pygame.draw.rect(screen, (0,0,0), boxRect, 5, 10)

            nameText,percentText = s_render(name,45,color), s_render(f'{limit_digits((value/totalValue)*100,16)}% of Portfolio',40,(110,110,110))
            nameH,nameW = nameText.get_height(),nameText.get_width()
            
            screen.blit(nameText, (boxRect.centerx-(nameW/2), boxRect.y+10))
            pygame.draw.rect(screen, (0,0,0), (boxRect.x,boxRect.y+nameH+15,boxRect.width,5))# draw the line under the name
            screen.blit(percentText, (boxRect.centerx-(percentText.get_width()/2), boxRect.y+20+nameH+10))
            if name == "Cash" or name == "Other":
                return
            nameList = ["Sell","Buy","Speculate"]
            
            menuDict = screenManager.screens  
            iconsNames = ['Portfolio','Stockbook','Options'] if name in menuDict['Stockbook'].stocknames else ['Portfolio','Bank','Options']
            for i in range(3):
                iconName = iconsNames[i]                

                y = boxRect.y+nameH+percentText.get_height()+40+(i*65)

                drawCenterTxt(screen, nameList[i], 50, (1,1,1), (boxRect.centerx, y+10),centerY=False)
                myRect = pygame.rect.Rect(boxRect.x+10,y,boxRect.width-20,60)
                pygame.draw.rect(screen, (0,0,0), myRect, 3, 5)
                if myRect.collidepoint(mousex,mousey):
                    pygame.draw.rect(screen, (220,220,220), myRect, 5, 5)
                    if mousebuttons == 1:
                        screenManager.setScreen(iconName)

                        if iconName == 'Stockbook':# if the stockbook is clicked, then set the selected asset to the one the mouse is over
                            menuDict['Stockbook'].changeSelectedStock(name=name[:4])
                            
                        elif iconName == 'Portfolio':# if the portfolio is clicked, then set the selected asset to the one the mouse is over
                            menuDict['Portfolio'].selectedAsset = menuDict['Portfolio'].findAsset(value,name)
                        elif iconName == 'Options':
                            menuDict['Options'].setSelectedAsset(menuDict['Portfolio'].findAsset(value,name))
                        elif iconName == 'Bank':
                            menuDict['Bank'].menuSelection.setSelected("Investments")
                            menuDict['Bank'].investScreen.fundSelection.setSelected(name)
                            
                    
                
                            
                            

        
        if pygame.Rect(self.coords[0],self.coords[1],self.radius*2,self.radius*2).collidepoint(mousex,mousey):# if the mouse is in the pie chart
            collided = False
            for i,(color,points,value,name) in enumerate(self.pieSegments):# loop through the pie segments
                if point_in_polygon((mousex-self.coords[0],mousey-self.coords[1]),points):# set collided to the one the mouse is over
                    collided = i
                    if pygame.mouse.get_pressed()[0]:# if the mouse is clicked, then set the selected asset to the one the mouse is over
                        self.selectedAssetIndex = i

            for i,(color,points,value,name) in enumerate(self.pieSegments):# draws all the segments darker except the one the mouse is over
                newcolor = (color[0]//2,color[1]//2,color[2]//2) if i != collided else color
                gfxdraw.filled_polygon(wholesurf,points,newcolor)#draws the none selected polygon darker


            value = self.pieSegments[collided][2]# the value of the stock the mouse is over
            drawBoxedText(wholesurf, f'${limit_digits(value,16)}',50,self.pieSegments[collided][0],(1,1,1),(self.radius,self.radius))# blit the value of the mouseover segement to the screen

        else:
            for color,points,value,name in self.pieSegments: 
                gfxdraw.filled_polygon(wholesurf,points,color)

            # if the mouse isn't over any of the segments, then display the total value    
            drawBoxedText(wholesurf, f'${limit_digits(totalValue,16)}',50,(0,170,0),(1,1,1),(self.radius,self.radius))# blit the value of the mouseover segement to the screen    

        if self.selectedAssetIndex != None:
            if self.selectedAssetIndex >= len(self.pieSegments):
                self.selectedAssetIndex = 0
            drawInfoBox(self.pieSegments[self.selectedAssetIndex],mousebuttons)# draw the information box to the right of the pie chart
        wholesurf.blit(createbacksurf(self.radius), (0,0))  # blit the backsurface to the screen
        wholesurf.set_colorkey((0,0,0))
        screen.blit(wholesurf, self.coords)
        
        pygame.draw.circle(screen, (0, 0, 0), (self.coords[0]+self.radius,self.coords[1]+self.radius), self.radius, 10)
