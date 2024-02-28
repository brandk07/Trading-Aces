import pygame
from pygame import gfxdraw
from Defs import *
import numpy as np

class Graph:
    def __init__(self) -> None:
        self.graphpoints = np.array([],dtype=object)

    def setPoints(self, points,):
        """Points can be a list or a numpy array"""
        if type(points) == list:
            points = np.array(points,dtype=object)

        self.graphpoints = points

    def draw_graph(self,screen,coords,wh,graphcolor):
        """Draws the graph to the screen"""
        x,y = coords[0],coords[1]+15
        width,height = wh[0],wh[1]-30


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
            gfxdraw.filled_polygon(screen,points,graphcolor)#draws the graphed points of the graph
            
            for i,value in enumerate(self.graphpoints):
                if i >= graphpointlen-1:
                    pass#if last one in list or i is too great then don't draw line
                else:
                    nextvalue = self.graphpoints[i+1]
                    xpos = x
                    gfxdraw.line(screen,xpos+int(i*spacing),int(value),xpos+int((i+1)*spacing),int(nextvalue),(255,255,255))
            
        else:
            minmaxsame = True
            gfxdraw.line(screen,x,int(y+height),x+width-5,int(y+height),(255,255,255))#draws a line across the graph
            spacing = width/len(self.graphpoints)#the spacing between each point
            self.graphpoints = [y+height]*(width)#makes the graphingpoints a list of the same y value
        return self.graphpoints,spacing,minmaxsame