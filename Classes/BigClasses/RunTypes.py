from datetime import datetime
import pygame
from Defs import *
import shutil
from dateutil.relativedelta import relativedelta
TIME_PERIODS = {
    '1M': relativedelta(months=1),
    '3M': relativedelta(months=3),
    '6M': relativedelta(months=6),
    '1Y': relativedelta(years=1),
    '3Y': relativedelta(years=3),
    '5Y': relativedelta(years=5) }

class GameRun:
    def __init__(self,name:str,assetSpread:list,gameMode,gameDate,iconIndex,runManager,startTime:str=None,lastPlayed:str=None) -> None:
        """Start time is real time (no relation to the game time) that is why the gameDate is needed"""
        assert type(assetSpread) == list, "The asset spread must be a list"# [stocks, options, indexFunds, cash, loans]
        # assert len(assetSpread) == 5, "The asset spread must have 5 values"
        assert gameMode in ['Blitz','Career','Goal'], "The game mode must be either 'Blitz', 'Career', or 'Goal'"
        assert (type(gameDate) == str or gameDate == None), "The game date must be a string"
        assert startTime == None or type(startTime) == str, "The start time must be a string"
        assert lastPlayed == None or type(lastPlayed) == str, "The last played time must be a string"
        
        self.name = name
        self.startTime = datetime.now() if startTime == None else datetime.strptime(startTime,"%m/%d/%Y %I:%M:%S %p")
        self.lastPlayed = datetime.now() if lastPlayed == None else datetime.strptime(lastPlayed,"%m/%d/%Y %I:%M:%S %p")
        self.runManager = runManager
        self.assetSpread = assetSpread if len(assetSpread) == 5 else [0,0,0,STARTCASH,0]# end value of all in each category [stocks, options, indexFunds, cash, loans]
        self.iconIndex = iconIndex
        self.runIcon = pygame.image.load(rf'Classes\BigClasses\RunIcons\image ({self.iconIndex}).png').convert_alpha()
        self.gameMode : str = gameMode.capitalize()# the mode of the game (Blitz, Career, Goal)
        if gameDate == None:
            self.gameDate = DEFAULTSTARTDATE# default start date
        else:
            self.gameDate = datetime.strptime(gameDate,"%m/%d/%Y %I:%M:%S %p")# the date the game started
        # self.networth = sum(self.assetSpread[:-1]) - self.assetSpread[-1]# the net worth of the player

        if not os.path.exists(self.getFileDir()):# if the run does not exist create the files
            self.massFileCreation(self.getFileDir())# moves/creates all the files for the new run 
            self.createCustomFile() # creates the mode specific file      
        
    def getNetworth(self):
        return sum(self.assetSpread[:-1]) - self.assetSpread[-1]
    def getLoans(self):
        return self.assetSpread[-1]
    def getFormattedStartTime(self):
        """Returns the start time in a formatted string"""
        return self.startTime.strftime("%m/%d/%Y") 
    def getRankInt(self) -> int:
        """Returns the rank of the run"""
        return self.runManager.getRanking(self)
    def getRankStr(self) -> str:
        """Returns the rank of the run"""
        return ordinal(self.runManager.getRanking(self))
    def getAssets(self):
        """Returns all the assets of the run"""
        return self.assetSpread# [stocks, options, indexFunds, cash, loans]
    def massFileCreation(self,save_dir):
        """Creates the files for the new game"""
        basicInfo = {"name": self.name,"assetSpread": [],"gameMode": self.gameMode,"gameDate": self.gameDate.strftime(DFORMAT),"iconIndex":self.iconIndex,"startTime":self.startTime.strftime(DFORMAT),"lastPlayed":datetime.now().strftime(DFORMAT)}

        os.makedirs(save_dir, exist_ok=True)

        with open(os.path.join(save_dir, "BasicInfo.json"), "w") as f:
            json.dump(basicInfo, f)        

        os.makedirs(os.path.join("Saves", self.gameMode, self.name, "ScreenShots"), exist_ok=True)# create the screenshot folder

        with open(os.path.join(save_dir, "ExtraData.json"), "w+") as f:
            json.dump([], f)

        with open(os.path.join(save_dir, "Transactions.json"), "w+") as f:
            json.dump([], f)
        
        stockDataDir = os.path.join(save_dir, "StockData")
        os.makedirs(stockDataDir, exist_ok=True)

        for name in STOCKNAMES+["Net Worth"]:# create the data files for each stock
            # file_path = f"{stockDataDir}/{name}/data.json"
            file_path = os.path.join(stockDataDir, name, "data.json")

            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w+") as f:
                # f.seek(0)  # go to the start of the file
                # f.truncate()  # clear the file
                for i in range(len(GRAPHRANGES+["trends"])+1):
                    json_item = json.dumps([])  # Convert the list to a JSON string
                    f.write(json_item + '\n') 
        print('Created files for new run')

    def getFileDir(self):
        return f"Saves/{self.gameMode}/{self.name}/"
    def createCustomFile(self):
        raise NotImplementedError
    def getModeSpecificInfo(self):
        raise NotImplementedError
    def saveRun(self):
        """Saves the run to the file"""
        save_dir = self.getFileDir()
        basicInfo = {"name": self.name,"assetSpread": self.assetSpread,"gameMode": self.gameMode,"gameDate": self.gameDate.strftime(DFORMAT),"iconIndex":self.iconIndex,"startTime":self.startTime.strftime(DFORMAT),"lastPlayed":datetime.now().strftime(DFORMAT)}
        with open(os.path.join(save_dir, "BasicInfo.json"), "w") as f:
            # f.seek(0)  # go to the start of the file
            # f.truncate()  # clear the file
            json.dump(basicInfo, f)
        with open(os.path.join(save_dir, "ModeSpecificInfo.json"), "w+") as f:
            # f.seek(0)  # go to the start of the file
            # f.truncate()  # clear the file
            json.dump(self.getModeSpecificInfo(), f)


class BlitzRun(GameRun):

    def __init__(self,name:str,assetSpread:list,gameDate,iconIndex,gameDuration:str,runManager,endGameDate=None,startTime:str=None,realWrldEndTime:str=None,lastPlayed:str=None) -> None:
        """Being Clear, the gameDate and endGameDate are the dates in the game not the real time
        and the startTime and realWrldEndTime are the real-life time that the player created and ended the run"""

        # These below need to be set before the super call since CreateCustomFile is called in the super call
        self.gameDuration = gameDuration# 1M, 3M, 6M, 1Y, 3Y, 5Y
        self.realWrldEndTime = None if realWrldEndTime == None else datetime.strptime(realWrldEndTime,"%m/%d/%Y %I:%M:%S %p")# the time when the run ended/was completed
        self.endGameDate = endGameDate# temporary until the createCustomFile is called - need endGameDate cause we don't track how many days have gone by so when gameDate reaches this then game over

        super().__init__(name,assetSpread,'Blitz',gameDate,iconIndex,runManager,startTime=startTime,lastPlayed=lastPlayed)

        if type(self.endGameDate) == str:# in case the createCustomFile isn't called since it wasn't just created
            # In theory it shouldn't need the if == None cause it should have been set when it was originally created, but just in case
            self.endGameDate = self.gameDate + TIME_PERIODS[self.gameDuration] if self.endGameDate == None else datetime.strptime(self.endGameDate,"%m/%d/%Y %I:%M:%S %p")


    def createCustomFile(self):
        self.endGameDate = datetime.strptime(self.endGameDate,"%m/%d/%Y %I:%M:%S %p") if self.endGameDate != None else self.gameDate + TIME_PERIODS[self.gameDuration]# the date the game ends
        save_dir = os.path.join("Saves", "Blitz", self.name)
        # os.makedirs(save_dir, exist_ok=True)
        info_path = os.path.join(save_dir, "ModeSpecificInfo.json")
        
        game_info = self.getModeSpecificInfo()
        with open(info_path, 'w') as f:
            json.dump(game_info, f) 

    def getModeSpecificInfo(self):
        """Returns the mode specific info for the run"""
        endTimestr = None if self.realWrldEndTime == None else self.realWrldEndTime.strftime(DFORMAT)# the time when the run ended/was completed
        return {"duration": self.gameDuration,"endGameDate": self.endGameDate.strftime(DFORMAT),"endTime":endTimestr} 
    
    def getTimeLeftInt(self,gametime):
        """Returns the time left in days"""
        return (self.endGameDate - gametime.time).days
    
    def getRemainingTimeStr(self,gametime):
        """Returns the remaining time in a string format"""
        timeleft = self.getTimeLeftInt(gametime)
        return f"{timeleft} days"
    # def getStarRating(self):
    #     """Returns the star rating of the run"""
    #     return min(5,int((self.getNetworth()/20_000)*5))
    

class CareerRun(GameRun):
    def __init__(self, name, assetSpread, gameMode, gameDate, startTime = None):
        super().__init__(name, assetSpread, gameMode, gameDate, startTime)

    def createCustomFile(self):
        save_dir = os.path.join("Saves", "Career", self.name)
        os.makedirs(save_dir, exist_ok=True)
        info_path = os.path.join(save_dir, "GameModeInfo.json")
        game_info = {"duration": time}# change for career mode
        with open(info_path, 'w') as f:
            json.dump(game_info, f) 
        
class GoalRun(GameRun):
    def __init__(self,name:str,assetSpread:list,gameDate,iconIndex,goalNetworth:int,runManager,startTime:str=None,realWrldEndTime:str=None,lastPlayed:str=None) -> None:
        """Being Clear, the gameDate is the date in the game not the real time
        and the startTime and realWrldEndTime are the real-life time that the player created and ended the run"""
        try:
            self.goalNetworth = int(goalNetworth)# the net worth the player needs to reach
        except:
            raise ValueError("The goal networth must be an integer or a string that can be converted to an integer")
        
        self.realWrldEndTime = None if realWrldEndTime == None else datetime.strptime(realWrldEndTime,"%m/%d/%Y %I:%M:%S %p")# the time when the run ended/was completed
        super().__init__(name,assetSpread,'Goal',gameDate,iconIndex,runManager,startTime=startTime,lastPlayed=lastPlayed)

    def getModeSpecificInfo(self):
        """Returns the mode specific info for the run"""
        endTimestr = None if self.realWrldEndTime == None else self.realWrldEndTime.strftime(DFORMAT)# the time when the run ended/was completed
        return {"duration": self.goalNetworth,"endTime":endTimestr,"goalNetworth":self.goalNetworth}
    def getGoalNetworth(self):
        return self.goalNetworth
    def getNetworthDelta(self):
        return self.goalNetworth - self.getNetworth()
    def createCustomFile(self):
        save_dir = os.path.join("Saves", "Goal", self.name)
        os.makedirs(save_dir, exist_ok=True)
        info_path = os.path.join(save_dir, "ModeSpecificInfo.json")
        game_info = self.getModeSpecificInfo()
        with open(info_path, 'w') as f:
            json.dump(game_info, f) 

class RunManager():
    """This class Manages all the runs in one convenient place"""
    def __init__(self):
        self.pastRuns : dict[str:list[GameRun]] = {'Career':[],'Blitz':[],'Goal':[]}# the past runs that the player has done
        self.loadPastRuns()
    def getRuns(self,mode:str):
        """Returns the runs of the mode"""
        return self.pastRuns[mode]
    def getAllRuns(self,inList=False):
        """Returns all the runs in a dictionary or list if inList is True"""
        if inList:
            return [run for mode in self.pastRuns for run in self.pastRuns[mode]]
        return self.pastRuns
    def addRun(self,run:GameRun):
        """Adds the run to the past runs"""
        self.pastRuns[run.gameMode].append(run)
    def getRanking(self,run:GameRun):
        """Returns the ranking of the runs in the mode"""
        runs = self.pastRuns[run.gameMode]
        # runs.append(run)
        runs.sort(key=lambda x:x.getNetworth(),reverse=True)
        return runs.index(run)+1
        # return "1"
    def loadPastRuns(self):
        for mode in self.pastRuns:
            print(os.listdir(os.path.join("Saves",mode)))
            for runName in os.listdir(os.path.join("Saves",mode)):
                with open(os.path.join("Saves",mode,runName,"BasicInfo.json"),"r") as f:
                    basicInfo = json.load(f)
                with open(os.path.join("Saves",mode,runName,"ModeSpecificInfo.json"),"r") as f:
                    modeSpecificInfo = json.load(f)
                if mode == 'Career':
                    pass
                elif mode == 'Blitz':
                    run = BlitzRun(basicInfo['name'],basicInfo['assetSpread'],basicInfo['gameDate'],basicInfo['iconIndex'],modeSpecificInfo['duration'],self,endGameDate=modeSpecificInfo['endGameDate'],startTime=basicInfo['startTime'],realWrldEndTime=modeSpecificInfo['endTime'],lastPlayed=basicInfo['lastPlayed'])
                elif mode == 'Goal':
                    run = GoalRun(basicInfo['name'],basicInfo['assetSpread'],basicInfo['gameDate'],basicInfo['iconIndex'],modeSpecificInfo['goalNetworth'],self,startTime=basicInfo['startTime'],realWrldEndTime=modeSpecificInfo['endTime'],lastPlayed=basicInfo['lastPlayed'])
                self.pastRuns[mode].append(run)
    def validName(self,name:str):
        """returns True if the name is valid"""
        if len(name) < 3:
            return "-Name must be at least 3 characters long"
        if name.isspace():
            return "-Name cannot be all spaces"
        for mode in self.pastRuns:
            for run in self.pastRuns[mode]:
                if run.name == name:
                    return "-Name already exists"
        return True