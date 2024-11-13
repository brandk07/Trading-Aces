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
from Classes.imports.PieChart import PieChart
from Classes.imports.Latterscroll import LinedLatter
from Classes.AssetTypes.LoanAsset import LoanAsset
import datetime
from Classes.imports.SideScroll import SideScroll,RunCard


class GameModeMenu(Menu):
    def __init__(self,stocklist,player,pastRuns:dict,currentRun) -> None:
        """Gets the past runs {'Blitz':[BlitzRun : obj],'Career':[],'Goal':[]}"""
        self.icon = pygame.image.load(r'Assets\Menu_Icons\gamemode.jpg').convert_alpha()
        self.icon = pygame.transform.scale(self.icon,(140,100))
        super().__init__(self.icon)
        self.loadRuns(pastRuns)# loads the runs from the save file
        self.currentRun = currentRun

        self.blitz : Blitz = Blitz(self.blitzReports,self.currentRun)
        self.career = Career()
        self.goal = Goal()
        self.player = player
        self.stocklist = stocklist
    

        self.gameMode = 'blitz'# career, goal, or blitz

        self.menudrawn = False
    def loadRuns(self,pastRuns:dict):
        self.blitzReports = pastRuns['Blitz']# full of BlitzRun objects
        self.careerReports = pastRuns['Career']# full of CareerRun objects
        self.goalReports = pastRuns['Goal']# full of GoalRun objects

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player, gametime):

        match self.gameMode:
            case 'blitz':
                self.blitz.draw(screen,mousebuttons)
            case 'career':
                self.draw()
            case 'goal':
                self.draw()
class GameRun:
    def __init__(self,name:str,networth:float,loans:float,assetSpread:list,gameMode,startTime:str=None) -> None:
        self.name = name
        self.startTime = datetime.datetime.now() if startTime == None else datetime.datetime.strptime(startTime,"%m/%d/%Y %I:%M:%S %p")
        self.networth = networth
        self.assetSpread = assetSpread# end value of all in each category [stocks, options, indexFunds]
        self.loans = loans
        self.gameMode : str = gameMode
        self.screenShotDir = r"Assets\GameRuns\Screenshots" + f"\{self.name}.png"
        if not os.path.exists(self.screenShotDir):
            self.screenShot = pygame.image.load(r"Assets\GameRuns\Screenshots\default.png").convert_alpha()
        else:
            self.screenShot = pygame.image.load(self.screenShotDir).convert_alpha()
        self.screenShot = pygame.transform.scale(self.screenShot,(190,190))

class BlitzRun(GameRun):
    def __init__(self,name:str,Networth:float,loans:float,assetSpread:list,startTime:str=None,endTime:str=None) -> None:

        super().__init__(name,Networth,loans,assetSpread,'Blitz',startTime=startTime)

        self.endTime = None if endTime == None else datetime.datetime.strptime(endTime,"%m/%d/%Y %I:%M:%S %p")


    def savingInputs(self):
        pass
    
    def setEndTime(self,time):
        """Sets the end time of the run"""
        self.endTime = time

    def getStarRating(self):
        """Returns the star rating of the run"""
        return min(5,int((self.networth/10_000)*5))



class Blitz:
    def __init__(self,pastRuns:list[BlitzRun],curentRun:BlitzRun) -> None:
        self.pastRuns : list[BlitzRun] = pastRuns# PAST RUNS DOESNT INCLUDE THE CURRENT RUN
        self.pastRuns.remove(curentRun)

        self.currentRun : BlitzRun = curentRun
        self.currRunPieChart = PieChart((195,105),(300,440))
        self.selecRunPieChart = PieChart((505,105),(300,440))
        self.sideScroll = SideScroll((195,555),(1240,415),(380,370))
        self.sideScrollCards = {}

        for run in self.pastRuns:
            self.sideScrollCards[run.name] = (RunCard(self.sideScroll,run))
        self.sideScroll.loadCards(list(self.sideScrollCards.values()))

        self.selectedRun : BlitzRun = None
        run = max(self.pastRuns,key=lambda x:x.networth)# gets the best run to start
        self.sideScroll.setCard(obj=self.sideScrollCards[run.name])# sets the card to the best run

    def drawPieCharts(self,screen,mousebuttons,run:BlitzRun=None):
        colors = [(46, 139, 87),(255, 69, 0), (65, 105, 225)]
        names = ['Stocks','Options','Index Funds']
        if run != None:
            values = [(val,name,color) for (val,name,color) in zip(run.assetSpread,names,colors)]
            self.selecRunPieChart.updateData(values)
            txt = "Selected Run" if self.selectedRun != None else "Best Run"
            self.selecRunPieChart.draw(screen,txt,mousebuttons)

        values = [(val,name,color) for (val,name,color) in zip(self.currentRun.assetSpread,names,colors)]
        self.currRunPieChart.updateData(values)
        self.currRunPieChart.draw(screen,"Current Run",mousebuttons,txtSize=35)

    def draw(self,screen,mousebuttons):
        
        
        if len(self.pastRuns) > 1:# if there are more than just the current run
            self.selectedRun = None if self.sideScroll.getCard() == None else self.sideScroll.getCard().runObj# gets the selected run
            run = self.selectedRun if self.selectedRun != None else max(self.pastRuns,key=lambda x:x.networth)# if the run is None then make it the best run
            if self.selectedRun == None:# if the selected run was None then set the card to the best run
                self.sideScroll.setCard(obj=self.sideScrollCards[run.name])
                
            
            # self.drawPastRuns()'
            
            self.sideScroll.draw(screen,mousebuttons)
            self.drawPieCharts(screen,mousebuttons,run)
            self.selectedRun = run

        else:
            self.sideScroll.setCard(None)
            self.drawPieCharts(screen,mousebuttons)
        # pass
        

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