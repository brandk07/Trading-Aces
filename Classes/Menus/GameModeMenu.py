import pygame
from Defs import *
from Classes.Menus.Menu import Menu
from Classes.imports.UIElements.PieChart import PieChart
from Classes.imports.UIElements.SideScroll import SideScroll,RunCard
from Classes.BigClasses.RunTypes import *

class GameModeMenu(Menu):
    def __init__(self,stocklist,player,pastRuns:dict,currentRun) -> None:
        """Gets the past runs {'Blitz':[BlitzRun : obj],'Career':[],'Goal':[]}"""
        super().__init__()
        self.loadRuns(pastRuns)# loads the runs from the save file
        self.currentRun = currentRun

        self.blitz : Blitz = Blitz(self.blitzReports,self.currentRun)
        self.career = Career()
        self.goal = Goal()
        self.player = player
        self.stocklist = stocklist
    

        self.gameMode = 'blitz'# career, goal, or blitz

        self.menudrawn = True
    def loadRuns(self,pastRuns:dict):
        self.blitzReports = pastRuns['Blitz']# full of BlitzRun objects
        self.careerReports = pastRuns['Career']# full of CareerRun objects
        self.goalReports = pastRuns['Goal']# full of GoalRun objects

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player, gametime):

        match self.gameMode:
            case 'blitz':
                self.blitz.draw(screen,mousebuttons,gametime)
            case 'career':
                self.draw()
            case 'goal':
                self.draw()


class Blitz:
    def __init__(self,pastRuns:list[BlitzRun],curentRun:BlitzRun) -> None:
        self.pastRuns : list[BlitzRun] = pastRuns# PAST RUNS DOESNT INCLUDE THE CURRENT RUN
        self.pastRuns.remove(curentRun)

        self.currentRun : BlitzRun = curentRun
        self.currRunPieChart = PieChart((580,105),(410,440))
        self.selecRunPieChart = PieChart((1120,105),(410,440))
        self.sideScroll = SideScroll((195,555),(1240,415),(380,370))
        self.sideScrollCards = {}

        for run in self.pastRuns:
            self.sideScrollCards[run.name] = (RunCard(self.sideScroll,run))
        self.sideScroll.loadCards(list(self.sideScrollCards.values()))

        self.selectedRun : BlitzRun = None
        if len(self.pastRuns) > 0:
            run = max(self.pastRuns,key=lambda x:x.getNetworth())# gets the best run to start
            self.sideScroll.setCard(obj=self.sideScrollCards[run.name])# sets the card to the best run


    def drawPieCharts(self,screen,mousebuttons,run:BlitzRun=None,maxRun=False):
        colors = [(0, 150, 136),(255, 69, 0), (65, 105, 225),(12, 89, 27)]
        
        names = ['Stocks','Options','Index Funds','Cash']
        if run != None:
            values = [(val,name,color) for (val,name,color) in zip(run.assetSpread[:-1],names,colors)]
            self.selecRunPieChart.updateData(values)
            txt = "Selected Run" if not maxRun else "Best Run"
            self.selecRunPieChart.draw(screen,txt,mousebuttons)

        values = [(val,name,color) for (val,name,color) in zip(self.currentRun.assetSpread[:-1],names,colors)]
        self.currRunPieChart.updateData(values)
        self.currRunPieChart.draw(screen,"Current Run",mousebuttons,txtSize=35)
    
    def drawBlitzInfo(self,screen,mousebuttons,gametime):
        """Draws the information for the blitz run"""

        blitzTxt = s_render("Blitz",85,(200,200,200))
        drawCenterRendered(screen,blitzTxt,(215,105),centerX=False,centerY=False)
        # line under the title
        pygame.draw.line(screen,(200,200,200),(210,170),(220+blitzTxt.get_width(),170),4)
        pygame.draw.rect(screen,(0,0,0),(195,180,350,360),5,10)

        txt = "Compete for the highest networth with limited time! Heightened market volatility will make investments more risky, but also rewarding..."
        for i,t in enumerate(separate_strings(txt,5)):
            drawCenterTxt(screen,t,30,(200,200,200),(370,190+i*45),centerY=False)
        
        pygame.draw.rect(screen,(0,0,0),(205,405,320,60),5,10)# displays the starting duration

        txt = "Blitz Duration : " + self.currentRun.gameDuration
        drawCenterTxt(screen,txt,35,(200,200,200),(365,420),centerY=False)


        pygame.draw.rect(screen,(0,0,0),(205,470,320,60),5,10)# displays the time remaining
        timeleft = self.currentRun.endGameDate - gametime.time

        txt = "Remaining : " + str(timeleft.days) + " days"
        drawCenterTxt(screen,txt,35,(200,200,200),(365,485),centerY=False)
        

    def drawRunsInfo(self,screen,mousebuttons,gametime,run:BlitzRun=None,maxRun=False):
        """Draws the information for the past runs"""
        drawCenterTxt(screen,"Current Run",65,(0,200,0),(1662,105),centerY=False)
        pygame.draw.rect(screen,(0,0,0),(1445,155,455,380),5,10)# draws box for current run info
        info = [
            (f"Name",f"{self.currentRun.name}"),
            (f"Start Time",f"{self.currentRun.getFormattedStartTime()}"),
            (f"End Time",f"{self.currentRun.getRealEndTimeTxt()}"),
            (f"Liabilities (Loans)",f"${limit_digits(self.currentRun.getLoans(),25,True)}"),

        ]
        drawLinedInfo(screen,(1450,160),(450,375),info,40,(180,180,180))
        
        
        if run != None:
            drawCenterTxt(screen,"Selected Run" if not maxRun else "Best Run",65,(200,200,200),(1662,540),centerY=False)
            pygame.draw.rect(screen,(0,0,0),(1445,590,455,380),5,10)# draws box for current run info
            info = [
                (f"Name",f"{run.name}"),
                (f"Start Time",f"{run.getFormattedStartTime()}"),
                (f"End Time",f"{run.getRealEndTimeTxt()}"),
                (f"Liabilities (Loans)",f"${limit_digits(run.getLoans(),25,True)}"),
            ]
            drawLinedInfo(screen,(1450,600),(450,375),info,40,(180,180,180))

    def draw(self,screen,mousebuttons,gametime):
        
        self.drawBlitzInfo(screen,mousebuttons,gametime)
        if len(self.pastRuns) > 0:# if there are more than just the current run
            self.selectedRun = None if self.sideScroll.getCard() == None else self.sideScroll.getCard().runObj# gets the selected run
            maxRun = max(self.pastRuns,key=lambda x:x.getNetworth())
            run = self.selectedRun if self.selectedRun != None else maxRun# if the run is None then make it the best run
            if self.selectedRun == None:# if the selected run was None then set the card to the best run
                self.sideScroll.setCard(obj=self.sideScrollCards[run.name])

            self.sideScroll.getCard().dataConfig(run); self.sideScroll.getCard().updateSurf()
                
            
            # self.drawPastRuns()'

            self.selectedRun = run
            self.sideScroll.draw(screen,mousebuttons)
            self.drawPieCharts(screen,mousebuttons,run,maxRun=self.selectedRun == maxRun)
            self.drawRunsInfo(screen,mousebuttons,gametime,run,maxRun=self.selectedRun == maxRun)

            

        else:
            # self.sideScroll.setCard(None)
            self.drawPieCharts(screen,mousebuttons)
            self.drawRunsInfo(screen,mousebuttons,gametime)
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