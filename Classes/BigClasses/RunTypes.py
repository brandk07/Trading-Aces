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
        # self.networth = sum(self.assetSpread[:-1]) - self.assetSpread[-1]# the networth of the player

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
    
    def updateAssetSpread(self,assetSpread:list):
        """Updates the asset spread"""
        self.assetSpread = assetSpread.copy()

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

        for name in STOCKNAMES+["Networth"]:# create the data files for each stock
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
    def __init__(self,name:str,assetSpread:list,gameDate,iconIndex,gameUnlocks:dict,sandBox:bool,runManager,startTime:str=None,lastPlayed:str=None) -> None:
        """Being Clear, the gameDate and endGameDate are the dates in the game not the real time
        and the startTime and realWrldEndTime are the real-life time that the player created and ended the run"""
        self.sandBoxMode = sandBox# if the player is in sandbox mode
        # self.verifyGameUnlocks(gameUnlocks)
        self.gameUnlocks = gameUnlocks# temporary until the verifyGameUnlocks is called
        super().__init__(name,assetSpread,'Career',gameDate,iconIndex,runManager,startTime=startTime,lastPlayed=lastPlayed)
        
        self.verifyGameUnlocks(gameUnlocks)


    def verifyGameUnlocks(self,gameUnlocks:dict):
        self.gameUnlocksInd = {
            "Storage Ind" : [6, 8, 10, 12, 14, 16],# index of asset storage unlock (0-5) (6, 8, 10, 12, 14, 16 items)
            "Interest Ind" : [5.5, 4.5, 3.5, 2.5, 1.5, 0.5],# index of interest for loans unlock (0-5)
            "LoanAmt Ind" : [1, 1.2, 1.4, 1.6, 1.8, 2],# index of loan amount unlock (0-5) (up to 200% of networth)
            "Tax Ind" : [15, 12.5, 10, 7.5, 5, 2.5]}# index of tax unlock (0-5) (15, 12.5, 10, 7.5, 5, 2.5% tax rate)
        self.gameUnlockCosts = {
            "Storage Ind" : [0, 25_000, 45_000, 91_000, 175_000, 335_000],# cost of asset storage unlock (0-5) (6, 8, 10, 12, 14, 16 items)
            "Interest Ind" : [0, 50_000, 105_000, 225_000, 475_000, 1_005_000],# cost of interest for loans unlock (0-5) (5.5, 4.5, 3.5, 2.5, 1.5, 0.5% interest)
            "StockReports Enabled" : 250_000,# cost of stock reports unlock
            "Tax Ind" : [0, 105_000, 225_000, 475_000, 1_005_000, 2_125_000]}# cost of tax unlock (0-5) (15, 12.5, 10, 7.5, 5, 2.5% tax rate)
        self.networthReq = {
            "PreMadeOptions Enabled" : 50_000,# if the premade options are enabled
            "CustomOptions Enabled" : 150_000,# if the custom options are enabled 
            "LoanAmt Ind" : [0, 300_000, 600_000, 900_000, 1_200_000, 1_500_000]}# if the loan amount is enabled (0-5) (up to $1,020,000 networth)

        if gameUnlocks != None and len(gameUnlocks) > 0:
            self.gameUnlocks = gameUnlocks# the unlocks the player has unlocked
        else:
            
            # If Gameunlocks hasn't been set then set it to the default values
            self.gameUnlocks = {
                "Storage Ind" : 0,# index of asset storage unlock (0-5) (6, 8, 10, 12, 14, 16 items) [Cost Based]            
                "PreMadeOptions Enabled" : self.getNetworth() >= self.networthReq["PreMadeOptions Enabled"],# if the premade options are enabled [Networth Based]
                "CustomOptions Enabled" : self.getNetworth() >= self.networthReq["CustomOptions Enabled"],# if the custom options are enabled [Networth Based]
                "LoanAmt Ind" : min(5,int(self.getNetworth()//170_000)),# Maxes out at $1,020,000 networth which would be a loan with 200% of networth [Networth Based]
                "Interest Ind" : 0,# index of interest in gameUnlocksInd - costs in gameUnlockCosts [Cost Based]
                "StockReports Enabled" : False,# if the stock reports are enabled - costs 250,000 [Cost Based]
                "Tax Ind" : 0,# index of tax in gameUnlocksInd - costs in gameUnlockCosts [Cost Based]
            }
        if self.sandBoxMode:# if the player is in sandbox mode then unlock everything
            self.gameUnlocks["PreMadeOptions Enabled"] = True
            self.gameUnlocks["CustomOptions Enabled"] = True
            self.gameUnlocks["StockReports Enabled"] = True
            self.gameUnlocks["LoanAmt Ind"] = 5
            self.gameUnlocks["Storage Ind"] = 5
            self.gameUnlocks["Interest Ind"] = 5
            self.gameUnlocks["Tax Ind"] = 5

    def updateGameUnlocks(self):
        if not self.gameUnlocks["PreMadeOptions Enabled"] and self.getNetworth() >= self.networthReq["PreMadeOptions Enabled"]:
            self.gameUnlocks["PreMadeOptions Enabled"] = True
        if not self.gameUnlocks["CustomOptions Enabled"] and self.getNetworth() >= self.networthReq["CustomOptions Enabled"]:
            self.gameUnlocks["CustomOptions Enabled"] = True
        if not self.gameUnlocks["StockReports Enabled"] and self.getNetworth() >= self.gameUnlockCosts["StockReports Enabled"]:
            self.gameUnlocks["StockReports Enabled"] = True
        if self.gameUnlocks["LoanAmt Ind"] < 5:
            self.gameUnlocks["LoanAmt Ind"] = min(5,int(self.getNetworth()//170_000))

    def nextUnlock(self,type:str):
        """Returns the closest unlock for the type (Networth or paid)"""
        if type.lower() == "paid" or type.lower() == "cost":
            # lowest = "Storage Ind"
            lowest = [key for key in ["Storage Ind","Interest Ind","Tax Ind"] if self.gameUnlocks[key] < 5]# finds which of the unlocks are not maxed out
            if lowest == [] and self.gameUnlocks["StockReports Enabled"] == False:# if all the unlocks are maxed out and stock reports are not enabled
                return "StockReports Enabled"
            elif lowest == [] and self.gameUnlocks["StockReports Enabled"]:# if all the unlocks are maxed out and stock reports are enabled
                return None
            lowest = lowest[0]# gets the first unlock that is not maxed out
            for unlock in ["Interest Ind","Tax Ind"]:
                if self.gameUnlocks[unlock] > 5:# if the unlock is maxed out then skip it
                    continue
                index1 = self.gameUnlocks[unlock]+1# index of the next unlock
                index2 = self.gameUnlocks[lowest]+1# index of the (current) lowest unlock
                if self.gameUnlockCosts[unlock][index1] < self.gameUnlockCosts[lowest][index2]:# if the cost of the next unlock is lower than the (current) lowest unlock
                    lowest = unlock
            index = self.gameUnlocks[lowest]+1# index of the next unlock for the current lowest
            if not self.gameUnlocks["StockReports Enabled"] and self.gameUnlockCosts["StockReports Enabled"] < self.gameUnlockCosts[lowest][index]:
                lowest = "StockReports Enabled"
            return lowest
        
        elif type.lower() == "networth":
            lowest = None
            if not self.gameUnlocks["PreMadeOptions Enabled"]:# if the premade options are not enabled
                lowest = "PreMadeOptions Enabled"# the next unlock is the premade options
            elif not self.gameUnlocks["CustomOptions Enabled"]:# if the premade options are enabled but custom options are not enabled
                lowest = "CustomOptions Enabled"# the next unlock is the custom options
            else:
                if self.gameUnlocks["LoanAmt Ind"] <= 5:
                    return "LoanAmt Ind"
                lowest = None

            if self.gameUnlocks["LoanAmt Ind"] > 5:# if the loan amount is maxed out
                return lowest
            index = self.gameUnlocks["LoanAmt Ind"]+1# index of the next unlock
            if self.networthReq[lowest] < self.networthReq["LoanAmt Ind"][index]:# if the next unlock is less than the loan amount unlock
                return lowest
            return "LoanAmt Ind"# the next unlock is the loan amount
        
    
        
    def updateAssetSpread(self, assetSpread):
        """Updates the asset spread and the game unlocks"""
        super().updateAssetSpread(assetSpread)
        self.updateGameUnlocks()

    def getModeSpecificInfo(self):
        """Returns the mode specific info for the run"""
        newDict = self.gameUnlocks.copy()
        newDict["sandBox"] = self.sandBoxMode  
        return newDict

    def createCustomFile(self):
        save_dir = os.path.join("Saves", "Career", self.name)
        os.makedirs(save_dir, exist_ok=True)
        info_path = os.path.join(save_dir, "ModeSpecificInfo.json")
        game_info = self.getModeSpecificInfo()# change for career mode
        with open(info_path, 'w') as f:
            json.dump(game_info, f) 
        
class GoalRun(GameRun):
    def __init__(self,name:str,assetSpread:list,gameDate,iconIndex,goalNetworth:int,runManager,startTime:str=None,realWrldEndTime:str=None,lastPlayed:str=None) -> None:
        """Being Clear, the gameDate is the date in the game not the real time
        and the startTime and realWrldEndTime are the real-life time that the player created and ended the run"""
        try:
            self.goalNetworth = int(goalNetworth)# the networth the player needs to reach
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
                    modeSpecificInfo : dict = json.load(f)
                if mode == 'Career':
                    if len(modeSpecificInfo) > 0:
                        sandBox = modeSpecificInfo.popitem()[1]
                    run = CareerRun(basicInfo['name'],basicInfo['assetSpread'],basicInfo['gameDate'],basicInfo['iconIndex'],modeSpecificInfo,sandBox,self,startTime=basicInfo['startTime'],lastPlayed=basicInfo['lastPlayed'])
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