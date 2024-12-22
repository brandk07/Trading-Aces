import pygame
from Defs import *
from Classes.Menus.Menu import Menu
from Classes.imports.UIElements.PieChart import PieChart
from Classes.imports.UIElements.SideScroll import VerticalScroll,ModeMenuRunCard
from Classes.BigClasses.RunTypes import *
from Classes.imports.UIElements.BarGraph import BarGraph

class GameModeMenu(Menu):
    def __init__(self,stocklist,player,pastRuns:dict,currentRun) -> None:
        """Gets the past runs {'Blitz':[BlitzRun : obj],'Career':[],'Goal':[]}"""
        super().__init__()
        self.loadRuns(pastRuns)# loads the runs from the save file
        self.currentRun = currentRun

        self.blitz : BlitzScreen = BlitzScreen(self.blitzReports,self.currentRun)
        self.career = CareerScreen(self.careerReports,self.currentRun)
        self.goal = GoalScreen(self.goalReports,self.currentRun)
        self.player = player
        self.stocklist = stocklist
    

        self.gameMode = self.currentRun.gameMode# career, goal, or blitz

        self.menudrawn = True
    def loadRuns(self,pastRuns:dict):
        self.blitzReports = pastRuns['Blitz'].copy()# full of BlitzRun objects
        self.careerReports = pastRuns['Career'].copy()# full of CareerRun objects
        self.goalReports = pastRuns['Goal'].copy()# full of GoalRun objects

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, player, gametime):

        match self.gameMode:
            case 'Blitz':
                self.blitz.draw(screen,gametime)
            case 'Career':
                self.career.draw(screen,gametime)
            case 'Goal':
                self.goal.draw(screen,gametime)

class BlitzAndGoalScreen:
    def __init__(self,pastRuns:list[BlitzRun|GoalRun],curentRun:BlitzRun|GoalRun) -> None:
        self.pastRuns : list[BlitzRun|GoalRun] = pastRuns# PAST RUNS DOESNT INCLUDE THE CURRENT RUN
        self.currentRun : BlitzRun|GoalRun = curentRun
        if self.currentRun in self.pastRuns:
            self.pastRuns.remove(self.currentRun)

        self.currBarGraph = BarGraph(self.currentRun.name,(205,565),(520,300))
        self.selcBarGraph = BarGraph(self.currentRun.name,(750,565),(520,300))
        self.pieChart = PieChart((745,125),(520,430))

        self.sideScrollCards = {}
        self.vertScroll = VerticalScroll((1290,195),(610,770),(570,170))
        for run in self.pastRuns:
            self.sideScrollCards[run.name] = (ModeMenuRunCard(self.vertScroll,run))
        self.vertScroll.loadCards(list(self.sideScrollCards.values()))

        self.selectedRun : BlitzRun|GoalRun = None if len(self.pastRuns) == 0 else self.pastRuns[0]
        if len(self.pastRuns) > 0:
            run = max(self.pastRuns,key=lambda x:x.getNetworth())# gets the best run to start
            self.vertScroll.setCard(obj=self.sideScrollCards[run.name])# sets the card to the best run
    
    def drawBarGraphs(self,screen):
        colors = [(255, 205, 78),(191, 85, 178),(239, 131, 84),(12, 89, 27)]#[stocks, options, indexFunds, cash]
        for i in range(4):
            x = 215+i*300
            pygame.draw.rect(screen,colors[i],(x,930,20,20),border_radius=5)
            drawCenterTxt(screen,['Stocks','Options','Index Funds','Cash'][i],45,(200,200,200),(x+30,940),centerX=False)


        pygame.draw.rect(screen,(0,0,0),(195,560,540,355),5,10)# draws the box for the current run
        maxScale = max(self.currentRun.getAssets()[:-1]) if self.selectedRun == None else max(self.selectedRun.getAssets()[:-1]+self.currentRun.getAssets()[:-1])
        # print(maxScale)
        self.currBarGraph.updateValues(self.currentRun.getAssets()[:-1],colors,['$']*4)
        self.currBarGraph.draw(screen,absoluteScale=maxScale)
        if self.selectedRun != None:
            pygame.draw.rect(screen,(0,0,0),(745,560,540,355),5,10)
            self.selcBarGraph.changeName(self.selectedRun.name)
            self.selcBarGraph.updateValues(self.selectedRun.getAssets()[:-1],colors,['$']*4)
            self.selcBarGraph.draw(screen,absoluteScale=maxScale)
        else:
            drawCenterTxt(screen,"No Selected Run",65,(210, 50, 50),(1015,650),centerY=False)

    def drawPieChart(self,screen):
        colors = [(255, 205, 78),(191, 85, 178),(239, 131, 84),(12, 89, 27)]#[stocks, options, indexFunds, cash]
        names = ['Stocks','Options','Index Funds','Cash']
        values = [(val,name,color) for (val,name,color) in zip(self.currentRun.assetSpread[:-1],names,colors)]
        self.pieChart.updateData(values)
        self.pieChart.draw(screen,"",txtSize=35)

    def drawVertScroll(self,screen):
        drawCenterTxt(screen,"Other Runs",80,(200,200,200),(1595,110),centerY=False)
        pygame.draw.rect(screen,(0,0,0),(1290,195,610,770),5,10)
        if len(self.pastRuns) > 0:
            self.vertScroll.draw(screen)
        else:
            drawCenterTxt(screen,"No Other Runs",65,(210, 50, 50),(1595,220),centerY=False)
            

    def drawRunInfo(self,screen,gametime):
        raise NotImplementedError("drawRunInfo must be implemented in the child class")

    def draw(self,screen,gametime):
        if self.currentRun in self.pastRuns:
            self.pastRuns.remove(self.currentRun)
        self.selectedRun = None if self.vertScroll.getCard() == None else self.vertScroll.getCard().runObj# gets the selected run
        drawCenterTxt(screen,self.currentRun.name,95,(200,200,200),(740,105),centerY=False)
        self.drawPieChart(screen)
        self.drawVertScroll(screen)
        self.drawRunInfo(screen,gametime)
        self.drawBarGraphs(screen)

class BlitzScreen(BlitzAndGoalScreen):
    def __init__(self,pastRuns:list[BlitzRun],curentRun:BlitzRun) -> None:
        super().__init__(pastRuns,curentRun)
        
    def drawRunInfo(self,screen,gametime):
        infoList = [
            (f"Mode",f"{self.currentRun.gameMode}"),
            (f"Rank",f"{self.currentRun.getRankStr()}"),
            (f"Time Left",f"{self.currentRun.getRemainingTimeStr(gametime)}"),
            (f"Start Date",f"{self.currentRun.getFormattedStartTime()}"),
        ]
        
        modeColors = {['Career','Blitz','Goal'][i]:[(19, 133, 100), (199, 114, 44), (196, 22, 62)][i] for i in range(3)}
        
        rankColor = (200,200,200) if self.currentRun.getRankInt() > 3 else [(255, 215, 0), (192, 192, 192),(205, 127, 50)][self.currentRun.getRankInt()-1]
        timeLeftCol = (0, 150, 136) if self.currentRun.getTimeLeftInt(gametime) > 10 else (255, 69, 0)
        colors = [modeColors[self.currentRun.gameMode],rankColor,timeLeftCol,(200,200,200)]
        pygame.draw.rect(screen,(0,0,0),(195,185,500,370),5,10)
        drawLinedInfo(screen,(200,185),(490,380),infoList,45,colors=colors)
    
class GoalScreen(BlitzAndGoalScreen):
    def __init__(self,pastRuns:list[GoalRun],curentRun:GoalRun) -> None:
        super().__init__(pastRuns,curentRun)
    def drawRunInfo(self,screen,gametime):
        infoList = [
            (f"Mode",f"{self.currentRun.gameMode}"),
            (f"Rank",f"{self.currentRun.getRankStr()}"),
            (f"Goal Networth",f"${limit_digits(self.currentRun.getGoalNetworth(),30)}"),
            (f"Start Date",f"{self.currentRun.getFormattedStartTime()}"),
        ]
        
        modeColors = {['Career','Blitz','Goal'][i]:[(19, 133, 100), (199, 114, 44), (196, 22, 62)][i] for i in range(3)}
        
        rankColor = (200,200,200) if self.currentRun.getRankInt() > 3 else [(255, 215, 0), (192, 192, 192),(205, 127, 50)][self.currentRun.getRankInt()-1]
        timeLeftCol = (0, 150, 136) if self.currentRun.getNetworth() > self.currentRun.getGoalNetworth()*.75 else (255, 69, 0)# if the networth is greater than 75% of the goal
        colors = [modeColors[self.currentRun.gameMode],rankColor,timeLeftCol,(200,200,200)]
        pygame.draw.rect(screen,(0,0,0),(195,185,500,370),5,10)
        drawLinedInfo(screen,(200,185),(490,380),infoList,45,colors=colors)

class CareerScreen(BlitzAndGoalScreen):
    def __init__(self,pastRuns:list[CareerRun],curentRun:CareerRun) -> None:

        super().__init__(pastRuns,curentRun)
        self.currentRun : CareerRun = self.currentRun# just for type hinting
    def drawRunInfo(self,screen,gametime):
        infoList = [
            (f"Mode",f"{self.currentRun.gameMode}"),
            (f"Rank",f"{self.currentRun.getRankStr()}"),
            (f"Networth Unlock",f"{self.currentRun.nextUnlock("Networth")}"),
            (f"Paid for Unlock",f"{self.currentRun.nextUnlock("Paid")}"),
            (f"Start Date",f"{self.currentRun.getFormattedStartTime()}"),
        ]
        
        modeColors = {['Career','Blitz','Goal'][i]:[(19, 133, 100), (199, 114, 44), (196, 22, 62)][i] for i in range(3)}
        
        rankColor = (200,200,200) if self.currentRun.getRankInt() > 3 else [(255, 215, 0), (192, 192, 192),(205, 127, 50)][self.currentRun.getRankInt()-1]
        colors = [modeColors[self.currentRun.gameMode],rankColor,(0, 170, 170),(0, 170, 170),(200,200,200)]
        pygame.draw.rect(screen,(0,0,0),(195,185,500,370),5,10)
        drawLinedInfo(screen,(200,185),(490,380),infoList,45,colors=colors)
