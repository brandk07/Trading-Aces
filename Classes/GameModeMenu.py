import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.Menu import Menu
import numpy as np
from Classes.imports.Bar import SliderBar
from Classes.StockVisualizer import StockVisualizer
from Classes.imports.Latterscroll import PortfolioLatter,LatterScroll
from Classes.Stock import Stock
from Classes.imports.BarGraph import BarGraph
from Classes.imports.SelectionElements import SelectionBar,MenuSelection
from Classes.imports.PerfChart import PerfChart
from Classes.imports.Numpad import Numpad
from Classes.imports.OrderBox import OrderBox
from Classes.AssetTypes.IndexFundsAsset import IndexFundAsset
from Classes.imports.Latterscroll import LinedLatter
from Classes.AssetTypes.LoanAsset import LoanAsset
import datetime
from Classes.imports.SideScroll import SideScroll,CdCard,LoanCard


class GameModeMenu(Menu):
    def __init__(self,stocklist,player) -> None:
        self.icon = pygame.image.load(r'Assets\Menu_Icons\gamemode.jpg').convert_alpha()
        self.icon = pygame.transform.scale(self.icon,(140,100))
        super().__init__(self.icon)
        self.blitz = Blitz()
        self.career = Career()
        self.goal = Goal()
        self.player = player
        self.stocklist = stocklist


        self.gameMode = 'blitz'# career, goal, or blitz

        self.menudrawn = False

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player, gametime):

        match self.gameMode:
            case 'blitz':
                self.draw()
            case 'career':
                self.draw()
            case 'goal':
                self.draw()
class BlitzRun:
    def __init__(self,startTime:str,endCash:float,assetSpread:list,endTime=None) -> None:
        self.startTime = datetime.datetime.strftime(startTime,'%Y-%m-%d %H:%M:%S')
        self.endTime = endTime if endTime == None else datetime.datetime.strftime(endTime,'%Y-%m-%d %H:%M:%S')
        self.endCash = endCash
        self.assetSpread = assetSpread# list of asset amts [stocks, options, indexfunds]


    def savingInputs(self):
        pass
    
    def setEndTime(self,time):
        """Sets the end time of the run"""
        self.endTime = time

    def getStarRating(self):
        """Returns the star rating of the run"""
        pass



class Blitz:
    def __init__(self) -> None:
        pass
    def draw(self):
        pass

class Career:
    def __init__(self) -> None:
        pass
    def draw(self):
        pass

class Goal:
    def __init__(self) -> None:
        pass
    def draw(self):
        pass