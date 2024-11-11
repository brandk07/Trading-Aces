import pygame
from pygame import gfxdraw
from Defs import *
import numpy as np

class Graph:
    """SHOULD NOT BE USED TO DRAW A GRAPH, USE THE STOCKVISUALIZER CLASS INSTEAD
    This class is used BY stock visualizer as an in-between for the stock object and the screen"""
    def __init__(self) -> None:
        
        self.graphpoints = np.array([],dtype=object)
        self.surface = pygame.Surface((500,500))

        self.needToUpdate = False
        self.lastSpacing = 0
        self.lastPoints = np.array([],dtype=object)
        self.lastMinMaxSame = False
        

    def setPoints(self, points):
        """Points can be a list or a numpy array"""
        if type(points) != np.ndarray:
            points = np.array(points, dtype=object)
        
        # Ensure both arrays have the same dtype before comparison
        # if points.dtype != self.graphpoints.dtype:
        # points = points.astype(self.graphpoints.dtype)
        
        # print(np.array_equal(points, self.graphpoints), "is it false")
        # print("point are", points, "graphpoints are", self.graphpoints, "are they equal?", np.array_equal(points, self.graphpoints))
        if np.array_equal(points, self.lastPoints):
            self.needToUpdate = False
            # print("Not updating")
        else:
            self.needToUpdate = True
            self.graphpoints,self.lastPoints = points,points

    def draw_graph(self,screen,coords,wh,underLineColor,backColor):
        """Draws the graph to the screen"""
        x,y = coords[0],coords[1]
        width,height = wh[0],wh[1]
        if not self.needToUpdate and self.surface.get_width() == width and self.surface.get_height() == height:#if the graph doesn't need to be updated then return the graphpoints
            screen.blit(self.surface,(x,y))
            # print("Returning")
            return self.graphpoints,self.lastSpacing,self.lastMinMaxSame
        
        
        if self.surface.get_width() != width or self.surface.get_height() != height:
            self.surface = pygame.Surface((width,height))
        self.surface.fill(backColor)
        # print("DRAWING THE GRAPH LOOOK HERE --------------SDFSDFJL")

        width,height = wh[0],wh[1]-30
        x,y = 0,15
        minpoint = (np.amin(self.graphpoints))
        maxpoint = (np.amax(self.graphpoints))     

        minmaxsame = False   

        if minpoint != maxpoint:#prevents divide by zero error
            yScale = (height*.75)/(maxpoint-minpoint)#the amount of pixels per point with the y axis

            self.graphpoints = (((height*0.75)-((self.graphpoints - minpoint)) * yScale)) + y+height*.25# Doing the math to make the points fit on the graph 

            spacing = width/len(self.graphpoints)#the spacing between each point

            graphpointlen = len(self.graphpoints)# doing this before the iteration to save time

            points = [(x,y+height+15)]
            points.extend([(x+int(i*spacing),int(value)) for i,value in enumerate(self.graphpoints)])
            points.append((x+width,y+height+15))
            gfxdraw.filled_polygon(self.surface,points,underLineColor)#draws the graphed points of the graph
            
            for i,value in enumerate(self.graphpoints):
                if i >= graphpointlen-1:
                    pass#if last one in list or i is too great then don't draw line
                else:
                    nextvalue = self.graphpoints[i+1]
                    xpos = x
                    gfxdraw.line(self.surface,xpos+int(i*spacing),int(value),xpos+int((i+1)*spacing),int(nextvalue),(255,255,255))
            
        else:
            minmaxsame = True
            gfxdraw.line(self.surface,x,int(y+height),x+width-5,int(y+height),(255,255,255))#draws a line across the graph
            spacing = width/len(self.graphpoints)#the spacing between each point
            self.graphpoints = [y+height]*(width)#makes the graphingpoints a list of the same y value\
        for i in range(len(self.graphpoints)):
            self.graphpoints[i] = self.graphpoints[i]+coords[1]
        self.lastSpacing,self.lastMinMaxSame = spacing,minmaxsame
        screen.blit(self.surface,(coords[0],coords[1]))
        return self.graphpoints,spacing,minmaxsame