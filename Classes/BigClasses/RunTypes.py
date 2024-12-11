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
    '5Y': relativedelta(years=5)}


class GameRun:
    def __init__(self,name:str,assetSpread:list,gameMode,gameDate,iconIndex,startTime:str=None) -> None:
        """Start time is real time (no relation to the game time) that is why the gameDate is needed"""
        assert type(assetSpread) == list, "The asset spread must be a list"
        # assert len(assetSpread) == 5, "The asset spread must have 5 values"
        assert gameMode in ['Blitz','Career','Goal'], "The game mode must be either 'Blitz', 'Career', or 'Goal'"
        assert (type(gameDate) == str or gameDate == None), "The game date must be a string"
        assert startTime == None or type(startTime) == str, "The start time must be a string"
        
        self.name = name
        self.startTime = datetime.now() if startTime == None else datetime.strptime(startTime,"%m/%d/%Y %I:%M:%S %p")
        
        self.assetSpread = assetSpread if len(assetSpread) == 5 else [0,0,0,STARTCASH,0]# end value of all in each category [stocks, options, indexFunds, cash, loans]
        self.iconIndex = iconIndex
        self.loans = self.assetSpread[-1]
        self.gameMode : str = gameMode
        if gameDate == None:
            self.gameDate = DEFAULTSTARTDATE# default start date
        else:
            self.gameDate = datetime.strptime(gameDate,"%m/%d/%Y %I:%M:%S %p")# the date the game started
        self.networth = sum(self.assetSpread[:-1]) - self.loans

        if not os.path.exists(self.getFileDir()):# if the run does not exist create the files
            self.massFileCreation(self.getFileDir())# moves/creates all the files for the new run        

    def massFileCreation(self,save_dir):
        """Creates the files for the new game"""
        basicInfo = {"name": self.name,"assetSpread": [],"gameMode": self.gameMode,"gameDate": self.gameDate.strftime(DFORMAT)}
        # os.makedirs(os.path.join(save_dir, "BasicInfo.json"), exist_ok=True)
        # with open(os.path.join(save_dir, "BasicInfo.json"), "w") as f:
        #     json.dump(basicInfo, f)
        os.makedirs(os.path.join(save_dir, "BasicInfo.json"), exist_ok=True)
        # info_path = os.path.join(save_dir, "BasicInfo.json")
        with open(r"Saves\Blitz\Game Name\BasicInfo.json", "w") as f:
            json.dump(basicInfo, f)
        
        source = os.path.join("Assets", "RunIcons", f"image {self.iconIndex}.png")# copy the game icon to the save folder
        dest = os.path.join(save_dir, "RunIcon.png")
        shutil.copy2(source, dest)

        os.makedirs(os.path.join("Saves", "Blitz", self.name, "ScreenShots"), exist_ok=True)# create the screenshot folder

        with open(os.path.join(save_dir, "ExtraData.json"), "w+") as f:
            json.dump([], f)

        with open(os.path.join(save_dir, "Transactions.json"), "w+") as f:
            json.dump([], f)
        
        stockDataDir = os.path.join("Assets", "StockData")
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

class BlitzRun(GameRun):
    def __init__(self,name:str,assetSpread:list,gameDate,iconIndex,gameDuration:str,endGameDate=None,startTime:str=None,endTime:str=None) -> None:
        """Being Clear, the gameDate and endGameDate are the dates in the game not the real time
        and the startTime and endTime are the real-life time that the player created and ended the run"""
        super().__init__(name,assetSpread,'Blitz',gameDate,iconIndex,startTime=startTime)
        self.gameDuration = gameDuration# 1M, 3M, 6M, 1Y, 3Y, 5Y

        self.endTime = None if endTime == None else datetime.strptime(endTime,"%m/%d/%Y %I:%M:%S %p")
        self.endGameDate = self.endGameDate if endGameDate != None else self.gameDate + TIME_PERIODS[self.gameDuration]# the date the game ends
        
        self.runIcon = pygame.image.load(os.path.join(self.getFileDir(),'RunIcon.png')).convert_alpha()

    def createCustomFile(self):
        save_dir = os.path.join("Saves", "Blitz", self.name)
        os.makedirs(save_dir, exist_ok=True)
        info_path = os.path.join(save_dir, "GameModeInfo.json")
        game_info = {"duration": self.gameDuration}
        with open(info_path, 'w') as f:
            json.dump(game_info, f) 

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

        self.runIcon = pygame.image.load(os.path.join(self.getFileDir(),'RunIcon.png')).convert_alpha()
    def createCustomFile(self):
        save_dir = os.path.join("Saves", "Career", self.name)
        os.makedirs(save_dir, exist_ok=True)
        info_path = os.path.join(save_dir, "GameModeInfo.json")
        game_info = {"duration": time}# change for career mode
        with open(info_path, 'w') as f:
            json.dump(game_info, f) 
class GoalRun(GameRun):
    def __init__(self, name, assetSpread, gameMode, gameDate, startTime = None):
        super().__init__(name, assetSpread, gameMode, gameDate, startTime)

        self.runIcon = pygame.image.load(os.path.join(self.getFileDir(),'RunIcon.png')).convert_alpha()
    
    def createCustomFile(self):
        save_dir = os.path.join("Saves", "Goal", self.name)
        os.makedirs(save_dir, exist_ok=True)
        info_path = os.path.join(save_dir, "GameModeInfo.json")
        game_info = {"duration": time}# change for goal mode
        with open(info_path, 'w') as f:
            json.dump(game_info, f) 