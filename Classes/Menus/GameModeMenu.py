import pygame
from Defs import *
from Classes.Menus.Menu import Menu
from Classes.imports.UIElements.PieChart import PieChart
import datetime
from Classes.imports.UIElements.SideScroll import SideScroll,RunCard
from dateutil.relativedelta import relativedelta
TIME_PERIODS = {
    '1M': relativedelta(months=1),
    '3M': relativedelta(months=3),
    '6M': relativedelta(months=6),
    '1Y': relativedelta(years=1),
    '3Y': relativedelta(years=3),
    '5Y': relativedelta(years=5)
}
STARTCASH = 10_000
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
class GameRun:
    def __init__(self,name:str,assetSpread:list,gameMode,gameDate,startTime:str=None) -> None:
        """Start time is real time (no relation to the game time) that is why the gameDate is needed"""
        assert type(assetSpread) == list, "The asset spread must be a list"
        # assert len(assetSpread) == 5, "The asset spread must have 5 values"
        assert gameMode in ['Blitz','Career','Goal'], "The game mode must be either 'Blitz', 'Career', or 'Goal'"
        assert type(gameDate) == str, "The game date must be a string"
        assert startTime == None or type(startTime) == str, "The start time must be a string"
        
        self.name = name
        self.startTime = datetime.datetime.now() if startTime == None else datetime.datetime.strptime(startTime,"%m/%d/%Y %I:%M:%S %p")
        
        self.assetSpread = assetSpread if len(assetSpread) == 5 else [0,0,0,STARTCASH,0]# end value of all in each category [stocks, options, indexFunds, cash, loans]

        self.loans = self.assetSpread[-1]
        self.gameMode : str = gameMode
        self.screenShotDir = r"Assets\GameRuns\Screenshots" + f"\{self.name}.png"
        self.gameDate = datetime.datetime.strptime(gameDate,"%m/%d/%Y %I:%M:%S %p")# the date the game started
        self.networth = sum(self.assetSpread[:-1]) - self.loans

        if not os.path.exists(self.screenShotDir):
            self.screenShot = pygame.image.load(r"Assets\GameRuns\Screenshots\default.png").convert_alpha()
        else:
            self.screenShot = pygame.image.load(self.screenShotDir).convert_alpha()
        self.screenShot = pygame.transform.scale(self.screenShot,(190,190))

class BlitzRun(GameRun):
    def __init__(self,name:str,assetSpread:list,duration:str,gameDate,endGameDate=None,startTime:str=None,endTime:str=None) -> None:
        """Being Clear, the gameDate and endGameDate are the dates in the game not the real time
        and the startTime and endTime are the real-life time that the player created and ended the run"""
        super().__init__(name,assetSpread,'Blitz',gameDate,startTime=startTime)
        self.duration = duration# 1M, 3M, 6M, 1Y, 3Y, 5Y

        self.endTime = None if endTime == None else datetime.datetime.strptime(endTime,"%m/%d/%Y %I:%M:%S %p")
        self.endGameDate = self.endGameDate if endGameDate != None else self.gameDate + TIME_PERIODS[self.duration]# the date the game ends
        
    def savingInputs(self):
        pass
    
    def getRealEndTimeTxt(self):
        """Returns the end time in a string format"""
        return "N/a" if self.endTime == None else self.endTime.strftime("%m/%d/%Y")
    def getFormattedStartTime(self):
        """Returns the start time in a formatted string"""
        return self.startTime.strftime("%m/%d/%Y")

    def getStarRating(self):
        """Returns the star rating of the run"""
        return min(5,int((self.networth/20_000)*5))

class CareerRun(GameRun):
    def __init__(self, name, assetSpread, gameMode, gameDate, startTime = None):
        super().__init__(name, assetSpread, gameMode, gameDate, startTime)

class GoalRun(GameRun):
    def __init__(self, name, assetSpread, gameMode, gameDate, startTime = None):
        super().__init__(name, assetSpread, gameMode, gameDate, startTime)


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
            run = max(self.pastRuns,key=lambda x:x.networth)# gets the best run to start
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

        txt = "Blitz Duration : " + self.currentRun.duration
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
            (f"Final Loan Value",f"${limit_digits(self.currentRun.loans,25,True)}"),

        ]
        drawLinedInfo(screen,(1450,160),(450,375),info,40,(180,180,180))
        
        
        if run != None:
            drawCenterTxt(screen,"Selected Run" if not maxRun else "Best Run",65,(200,200,200),(1662,540),centerY=False)
            pygame.draw.rect(screen,(0,0,0),(1445,590,455,380),5,10)# draws box for current run info
            info = [
                (f"Name",f"{run.name}"),
                (f"Start Time",f"{run.getFormattedStartTime()}"),
                (f"End Time",f"{run.getRealEndTimeTxt()}"),
                (f"Final Loan Value",f"${limit_digits(run.loans,25,True)}"),
            ]
            drawLinedInfo(screen,(1450,600),(450,375),info,40,(180,180,180))
        


    def draw(self,screen,mousebuttons,gametime):
        
        self.drawBlitzInfo(screen,mousebuttons,gametime)
        if len(self.pastRuns) > 1:# if there are more than just the current run
            self.selectedRun = None if self.sideScroll.getCard() == None else self.sideScroll.getCard().runObj# gets the selected run
            maxRun = max(self.pastRuns,key=lambda x:x.networth)
            run = self.selectedRun if self.selectedRun != None else maxRun# if the run is None then make it the best run
            if self.selectedRun == None:# if the selected run was None then set the card to the best run
                self.sideScroll.setCard(obj=self.sideScrollCards[run.name])
                
            
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