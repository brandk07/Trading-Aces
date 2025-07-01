from datetime import datetime
import pygame
import os
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
    def __init__(self,name:str,assetSpread:list,gameMode,gameDate,iconIndex,runManager,startTime:str=None,lastPlayed:str=None,state:str="live") -> None:
        """Start time is real time (no relation to the game time) that is why the gameDate is needed"""
        assert type(assetSpread) == list, "The asset spread must be a list"# [stocks, options, indexFunds, cash, loans]
        # assert len(assetSpread) == 5, "The asset spread must have 5 values"
        assert gameMode in ['Blitz','Career','Goal'], "The game mode must be either 'Blitz', 'Career', or 'Goal'"
        assert (type(gameDate) == str or gameDate is None), "The game date must be a string"
        assert startTime is None or type(startTime) == str, "The start time must be a string"
        assert lastPlayed is None or type(lastPlayed) == str, "The last played time must be a string"
        self.state = "live" if state == "live" else "complete"# the state of the run (live or complete)
        self.name = name
        self.startTime = datetime.now() if startTime is None else datetime.strptime(startTime,"%m/%d/%Y %I:%M:%S %p")
        self.lastPlayed = datetime.now() if lastPlayed is None else datetime.strptime(lastPlayed,"%m/%d/%Y %I:%M:%S %p")
        self.runManager = runManager
        self.assetSpread = assetSpread if len(assetSpread) == 5 else [0,0,0,STARTCASH,0]# end value of all in each category [stocks, options, indexFunds, cash, loans]
        self.iconIndex = iconIndex
        self.runIcon = pygame.image.load(os.path.join(os.path.dirname(__file__), 'RunIcons', f'image ({self.iconIndex}).png')).convert_alpha()
        self.gameMode : str = gameMode.capitalize()# the mode of the game (Blitz, Career, Goal)

        if gameDate is None:
            self.gameDate = DEFAULTSTARTDATE# default start date
        else:
            self.gameDate = datetime.strptime(gameDate,"%m/%d/%Y %I:%M:%S %p")# the date the game started
        # self.networth = sum(self.assetSpread[:-1]) - self.assetSpread[-1]# the networth of the player

        if not os.path.exists(self.getFileDir()):# if the run does not exist create the files
            self.massFileCreation(self.getFileDir())# moves/creates all the files for the new run 
            self.createCustomFile() # creates the mode specific file      
    def getCurrValStr(self,uString:str):
        """Returns the current value of the upgrade as a string - by default all will be maxed for blitz and goal, career will override this"""
        valStrs = {"Asset Storage" : f"16 slots","Loan Interest" : f"0.5% interest","Max Loan Amount" : f"200% Networth","Tax Rate" : f"2.5% tax rate","Stock Reports" : "Reports Enabled","Pre-Made Options" : "Trading Enabled","Custom Options" : "Trading Enabled"}
        return valStrs[uString]
    def getCurrVal(self,uString:str):
        """Returns the current value of the upgrade - by default all will be maxed for blitz and goal, career will override this"""
        valStrs = {"Asset Storage" : 16,"Loan Interest" : 0.5,"Max Loan Amount" : 2,"Tax Rate" : 2.5,"Stock Reports" : True,"Pre-Made Options" : True,"Custom Options" : True}
        return valStrs[uString]
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
        return "N/A" if (rank:=self.runManager.getRanking(self)) is None else ordinal(rank)
    def getAssets(self):
        """Returns all the assets of the run"""
        return self.assetSpread# [stocks, options, indexFunds, cash, loans]
    def massFileCreation(self,save_dir):
        """Creates the files for the new game"""
        basicInfo = {"name": self.name,"assetSpread": [],"gameMode": self.gameMode,"gameDate": self.gameDate.strftime(DFORMAT),"iconIndex":self.iconIndex,"startTime":self.startTime.strftime(DFORMAT),"lastPlayed":datetime.now().strftime(DFORMAT)}

        os.makedirs(save_dir, exist_ok=True)

        with open(os.path.join(save_dir, "BasicInfo.json"), "w") as f:
            json.dump(basicInfo, f)        

        os.makedirs(os.path.join(save_dir, "ScreenShots"), exist_ok=True)# create the screenshot folder

        with open(os.path.join(save_dir, "ExtraData.json"), "w+") as f:
            json.dump([], f)

        with open(os.path.join(save_dir, "Transactions.json"), "w+") as f:
            json.dump([], f)
        
        stockDataDir = os.path.join(save_dir, "StockData")
        os.makedirs(stockDataDir, exist_ok=True)

        for name in STOCKNAMES+["Networth","Cash"]:# create the data files for each stock
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
        """Returns the directory of the run"""
        saveDir = f"Saves/Complete/{self.gameMode}/{self.name}/" if self.state == "complete" else f"Saves/{self.gameMode}/{self.name}/"
        return saveDir
    def createCustomFile(self):
        raise NotImplementedError
    def getState(self):
        raise NotImplementedError
    def getModeSpecificInfo(self):
        raise NotImplementedError
    def saveRun(self,gametime:datetime):
        """Saves the run to the file"""
        save_dir = self.getFileDir()
        basicInfo = {"name": self.name,"assetSpread": self.assetSpread,"gameMode": self.gameMode,"gameDate": gametime.strftime(DFORMAT),"iconIndex":self.iconIndex,"startTime":self.startTime.strftime(DFORMAT),"lastPlayed":datetime.now().strftime(DFORMAT)}
        if not os.path.exists(save_dir):# used if the run is being transferred from live to complete (at least right now 2/17/2025)
            os.makedirs(save_dir, exist_ok=True)# create the directory if it doesn't exist
            self.massFileCreation(save_dir)# create the files for the new run
        with open(os.path.join(save_dir, "BasicInfo.json"), "w") as f:
            json.dump(basicInfo, f)
        with open(os.path.join(save_dir, "ModeSpecificInfo.json"), "w+") as f:
            json.dump(self.getModeSpecificInfo(), f)


class BlitzRun(GameRun):

    def __init__(self,name:str,assetSpread:list,gameDate,iconIndex,gameDuration:str,runManager,endGameDate=None,startTime:str=None,realWrldEndTime:str=None,lastPlayed:str=None,state:str="live") -> None:
        """Being Clear, the gameDate and endGameDate are the dates in the game not the real time
        and the startTime and realWrldEndTime are the real-life time that the player created and ended the run"""

        # These below need to be set before the super call since CreateCustomFile is called in the super call
        self.gameDuration = gameDuration# 1M, 3M, 6M, 1Y, 3Y, 5Y
        self.realWrldEndTime = None if realWrldEndTime is None else datetime.strptime(realWrldEndTime,"%m/%d/%Y %I:%M:%S %p")# the time when the run ended/was completed
        self.endGameDate = endGameDate# temporary until the createCustomFile is called - need endGameDate cause we don't track how many days have gone by so when gameDate reaches this then game over

        super().__init__(name,assetSpread,'Blitz',gameDate,iconIndex,runManager,startTime=startTime,lastPlayed=lastPlayed,state=state)

        if type(self.endGameDate) == str:# in case the createCustomFile isn't called since it wasn't just created
            # In theory it shouldn't need the if is None cause it should have been set when it was originally created, but just in case
            self.endGameDate = self.gameDate + TIME_PERIODS[self.gameDuration] if self.endGameDate is None else datetime.strptime(self.endGameDate,"%m/%d/%Y %I:%M:%S %p")


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
        endTimestr = None if self.realWrldEndTime is None else self.realWrldEndTime.strftime(DFORMAT)# the time when the run ended/was completed
        return {"duration": self.gameDuration,"endGameDate": self.endGameDate.strftime(DFORMAT),"endTime":endTimestr} 
    
    def getTimeLeftInt(self,gametime):
        """Returns the time left in days"""
        return (self.endGameDate - gametime.time).days
    def completeRun(self,gametime):
        """Completes the run"""
        self.realWrldEndTime = datetime.now()
        errors.addMessage(f"Out of Time - Run Completed",coords=(960,300),lifeTime=360,txtSize=100)
        errors.addMessage(f'Now in View Mode',coords=(960,480),lifeTime=360)
        self.runManager.completeRun(self,gametime)

    def getState(self,gametime):
        """Returns the state of the run"""
        if self.state == "complete":
            return "complete"
        if self.getTimeLeftInt(gametime) <= 0:# if the time has run out
            if self.state == "live":# if the run is still live
                self.completeRun(gametime)
            return "complete"
        return 'live'
    def getRemainingTimeStr(self,gametime):
        """Returns the remaining time in a string format"""
        timeleft = self.getTimeLeftInt(gametime)
        return f"{timeleft} days"
    # def getStarRating(self):
    #     """Returns the star rating of the run"""
    #     return min(5,int((self.getNetworth()/20_000)*5))
    

class CareerRun(GameRun):
    def __init__(self,name:str,assetSpread:list,gameDate,iconIndex,unlocks:dict,upgrades:dict,sandBox:bool,runManager,startTime:str=None,lastPlayed:str=None,state="live") -> None:
        """Being Clear, the gameDate and endGameDate are the dates in the game not the real time
        and the startTime and realWrldEndTime are the real-life time that the player created and ended the run"""
        self.sandBoxMode = sandBox# if the player is in sandbox mode
        # self.verifyunlocks(unlocks)
        self.unlocks = unlocks# temporary until the verifyunlocks is called
        self.upgrades = upgrades# temporary until the verifyunlocks is called
        super().__init__(name,assetSpread,'Career',gameDate,iconIndex,runManager,startTime=startTime,lastPlayed=lastPlayed,state=state)
        
        self.verifyGameData(unlocks,upgrades)

    def setSandboxMode(self):
        self.unlocks = {"Pre-Made Options" : True,"Custom Options" : True,"Stock Reports" : True}
        self.upgrades = {"Asset Storage" : 5,"Loan Interest" : 5,"Max Loan Amount" : 5,"Tax Rate" : 5}
    def getUpgradeOrUnlock(self,string:str):
        """Returns whether the string (Upgrade or Unlock) is an upgrade or an unlock"""
        assert string in list(self.unlocks.keys())+list(self.upgrades.keys()), "The string must be a key in the unlocks or upgrades"
        if string in list(self.unlocks.keys()):
            return "Unlock"
        return "Upgrade"
    def getNetOrCash(self,string:str):
        """Returns whether the string (Upgrade or Unlock) is based on the networth or the cash"""
        assert string in list(self.unlocks.keys())+list(self.upgrades.keys()), "The string must be a key in the unlocks or upgrades"
        if string in ["Pre-Made Options","Custom Options","Max Loan Amount"]:
            return "Networth"
        return "Cash"

    def advanceUpgradeOrUnlock(self,string:str):
        """Advances the upgrade or gives the unlock"""
        if self.isMaxed(string): return# if the upgrade is maxed out then return
        if self.getUpgradeOrUnlock(string) == "Upgrade":# if the string is an upgrade
            self.upgrades[string] += 1
        else:# if the string is an unlock
            self.unlocks[string] = True
    
    def verifyGameData(self,unlocks:dict,upgrades:dict):
        self.upgradesLevels = {
            "Asset Storage" : [4, 8, 10, 12, 14, 16],# (6, 8, 10, 12, 14, 16 slots)
            "Loan Interest" : [5.5, 4.5, 3.5, 2.5, 1.5, 0.5],# % interest
            "Max Loan Amount" : [0.2, 0.4, 0.5, 0.9, 1.4, 2],# Networth to loan amount ratio
            "Tax Rate" : [15, 12.5, 10, 7.5, 5, 2.5]}# tax rate
        self.gameCosts = {
            "Loan Interest" : [0, 50_000, 105_000, 225_000, 475_000, 1_005_000],
            "Asset Storage" : [0, 25_000, 45_000, 91_000, 175_000, 335_000],            
            "Tax Rate" : [0, 105_000, 225_000, 475_000, 1_005_000, 2_125_000],
            "Stock Reports" : 250_000}
        self.networthReq = {
            "Max Loan Amount" : [0, 300_000, 600_000, 900_000, 1_200_000, 1_500_000],# Networth required for upgrade levels
            "Pre-Made Options" : 50_000,
            "Custom Options" : 150_000,}

        if unlocks != None and len(unlocks) > 0:# if the unlocks has been set
            self.unlocks = unlocks# the unlocks the player has unlocked
        else:
            self.unlocks = {
                "Pre-Made Options" : False,# (bool) [Networth Based]
                "Custom Options" : False,# (bool) [Networth Based]
                "Stock Reports" : False,}# (bool) [Cost Based]
            
        if upgrades != None and len(upgrades) > 0:# if the upgrades has been set
            self.upgrades = upgrades
        else:
            self.upgrades = {
                "Asset Storage" : 0,# (Index) [Cost Based]
                "Loan Interest" : 0,# (Index) [Cost Based]
                "Max Loan Amount" : 0,# (Index) [Networth Based]
                "Tax Rate" : 0}# (Index) [Cost Based]
            
        if self.sandBoxMode:# if the player is in sandbox mode then unlock everything
            self.setSandboxMode()
    def getCurrVal(self,uString:str):
        """Returns the current value of the upgrade"""
        if uString in ["Pre-Made Options","Custom Options","Stock Reports"]:
            return self.unlocks[uString]
        return self.upgradesLevels[uString][self.upgrades[uString]]
    def getCurrValStr(self,uString:str):
        """Returns the current value of the upgrade as a string"""

        valStrs = {"Asset Storage" : f"{self.getCurrVal("Asset Storage")} slots",
                    "Loan Interest" : f"{self.getCurrVal('Loan Interest')}% interest",
                    "Max Loan Amount" : f"{self.getCurrVal('Max Loan Amount')*100}% Networth",
                    "Tax Rate" : f"{self.getCurrVal('Tax Rate')}% tax rate",
                    "Stock Reports" : "Reports Enabled" if self.unlocks['Stock Reports'] else "Reports Disabled",
                    "Pre-Made Options" : "Trading Enabled" if self.unlocks['Pre-Made Options'] else "Trading Disabled",
                    "Custom Options" : "Trading Enabled" if self.unlocks['Custom Options'] else "Trading Disabled",}

        return valStrs[uString]
    
    def isMaxed(self,uString:str):
        """Returns True if the upgrade is maxed out"""
        if self.getNetOrCash(uString) == "Networth":
            if uString == "Max Loan Amount":
                return self.upgrades[uString] == 5
            return self.unlocks[uString]# if the unlock is networth based and not Max Loan Amount
        if uString == "Stock Reports":
            return self.unlocks[uString]
        return self.upgrades[uString] == 5# if the upgrade is cash based and not Stock Reports
    
    def getNextGrantStr(self,uString):
        """Returns the next grant string for the upgrade"""
        if self.isMaxed(uString):
            return None
        extraTxt = {
            "Asset Storage" : f"+2 slots",
            "Loan Interest" : f"-1 loan interest",
            "Max Loan Amount" : f"+20% Max Loan",
            "Tax Rate" : f"-2.5 tax rate",
            "Stock Reports" : "Reports Enabled",
            "Pre-Made Options" : "Trading Enabled",
            "Custom Options" : "Trading Enabled",}
        return extraTxt[uString]
        # if self.getNetOrCash(uString) == "Networth":
        #     if uString == "Max Loan Amount":
        #         return self.upgradesLevels[uString][self.upgrades[uString]+1]
        #     return self.upgradesLevels[uString]
        # if uString == "Stock Reports":
        #     return self.gameCosts[uString]
        # return self.gameCosts[uString][self.upgrades[uString]+1]

    def getAllUStrings(self):
        """Returns all the upgrade strings"""
        return list(self.unlocks.keys())+list(self.upgrades.keys())
    def getNextCost(self,uString:str):
        """Returns the cost of the next upgrade"""
        if self.isMaxed(uString):
            return None
        if self.getNetOrCash(uString) == "Networth":
            if uString == "Max Loan Amount":
                return self.networthReq[uString][self.upgrades[uString]+1]
            return self.networthReq[uString]
        if uString == "Stock Reports":
            return self.gameCosts[uString]
        return self.gameCosts[uString][self.upgrades[uString]+1]
    
    def getProximity(self,uString:str,player):
        """Returns the proximity of the upgrade"""
        netW = player.getNetworth()
        cash = player.getCash()
        if self.isMaxed(uString):
            return 100
        if self.getNetOrCash(uString) == "Networth":
            if uString == "Max Loan Amount":
                cost = self.networthReq[uString][self.upgrades[uString]+1]
                return int(min(100,(1-((cost - netW) / cost)) * 100))
            cost = self.networthReq[uString]
            return int(min(100,(1-((cost - netW) / cost)) * 100))
        if uString == "Stock Reports":
            cost = self.gameCosts[uString]
            return int(min(100,(1-((cost - cash) / cost)) * 100))
        cost = self.gameCosts[uString][self.upgrades[uString]+1]
        return int(min(100,(1-((cost - cash) / cost)) * 100))

    def updateunlocks(self):
        if not self.unlocks["Pre-Made Options"] and self.getNetworth() >= self.networthReq["Pre-Made Options"]:
            self.unlocks["Pre-Made Options"] = True
        if not self.unlocks["Custom Options"] and self.getNetworth() >= self.networthReq["Custom Options"]:
            self.unlocks["Custom Options"] = True
        if not self.unlocks["Stock Reports"] and self.getNetworth() >= self.gameCosts["Stock Reports"]:
            self.unlocks["Stock Reports"] = True
        if self.upgrades["Max Loan Amount"] < 5:
            self.upgrades["Max Loan Amount"] = min(5,int(self.getNetworth()//170_000))
    
    def getState(self,gametime):# always live
        return 'live'

    # def nextUnlock(self,type:str):
    #     """Returns the closest unlock for the type (Networth or paid)"""
    #     if type.lower() == "paid" or type.lower() == "cost":
    #         # lowest = "Asset Storage"
    #         lowest = [key for key in ["Asset Storage","Loan Interest","Tax Rate"] if self.unlocks[key] < 5]# finds which of the unlocks are not maxed out
    #         if lowest == [] and self.unlocks["Stock Reports"] == False:# if all the unlocks are maxed out and Stock Reports are not enabled
    #             return "Stock Reports"
    #         elif lowest == [] and self.unlocks["Stock Reports"]:# if all the unlocks are maxed out and Stock Reports are enabled
    #             return None
    #         lowest = lowest[0]# gets the first unlock that is not maxed out
    #         for unlock in ["Loan Interest","Tax Rate"]:
    #             if self.unlocks[unlock] > 5:# if the unlock is maxed out then skip it
    #                 continue
    #             index1 = self.unlocks[unlock]+1# index of the next unlock
    #             index2 = self.unlocks[lowest]+1# index of the (current) lowest unlock
    #             if self.gameUnlockCosts[unlock][index1] < self.gameUnlockCosts[lowest][index2]:# if the cost of the next unlock is lower than the (current) lowest unlock
    #                 lowest = unlock
    #         index = self.unlocks[lowest]+1# index of the next unlock for the current lowest
    #         if not self.unlocks["Stock Reports"] and self.gameUnlockCosts["Stock Reports"] < self.gameUnlockCosts[lowest][index]:
    #             lowest = "Stock Reports"
    #         return lowest
        
    #     elif type.lower() == "networth":
    #         lowest = None
    #         if not self.unlocks["Pre-Made Options"]:# if the premade options are not enabled
    #             lowest = "Pre-Made Options"# the next unlock is the premade options
    #         elif not self.unlocks["Custom Options"]:# if the premade options are enabled but custom options are not enabled
    #             lowest = "Custom Options"# the next unlock is the custom options
    #         else:
    #             if self.unlocks["Max Loan Amount"] <= 5:
    #                 return "Max Loan Amount"
    #             lowest = None

    #         if self.unlocks["Max Loan Amount"] > 5:# if the loan amount is maxed out
    #             return lowest
    #         index = self.unlocks["Max Loan Amount"]+1# index of the next unlock
    #         if self.networthReq[lowest] < self.networthReq["Max Loan Amount"][index]:# if the next unlock is less than the loan amount unlock
    #             return lowest
    #         return "Max Loan Amount"# the next unlock is the loan amount
        
    
        
    def updateAssetSpread(self, assetSpread):
        """Updates the asset spread and the game unlocks"""
        super().updateAssetSpread(assetSpread)
        self.updateunlocks()

    def getModeSpecificInfo(self):
        """Returns the mode specific info for the run"""
        newDict = self.unlocks.copy()
        newDict.update(self.upgrades)
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
    def __init__(self,name:str,assetSpread:list,gameDate,iconIndex,goalNetworth:int,runManager,startTime:str=None,realWrldEndTime:str=None,lastPlayed:str=None,state:str="live") -> None:
        """Being Clear, the gameDate is the date in the game not the real time
        and the startTime and realWrldEndTime are the real-life time that the player created and ended the run"""
        try:
            self.goalNetworth = int(goalNetworth)# the networth the player needs to reach
        except:
            raise ValueError("The goal networth must be an integer or a string that can be converted to an integer")
        
        self.realWrldEndTime = None if realWrldEndTime is None else datetime.strptime(realWrldEndTime,"%m/%d/%Y %I:%M:%S %p")# the time when the run ended/was completed
        super().__init__(name,assetSpread,'Goal',gameDate,iconIndex,runManager,startTime=startTime,lastPlayed=lastPlayed,state=state)

    def getModeSpecificInfo(self):
        """Returns the mode specific info for the run"""
        endTimestr = None if self.realWrldEndTime is None else self.realWrldEndTime.strftime(DFORMAT)# the time when the run ended/was completed
        return {"duration": self.goalNetworth,"endTime":endTimestr,"goalNetworth":self.goalNetworth}
    def getGoalNetworth(self):
        return self.goalNetworth
    def getNetworthDelta(self):
        return self.goalNetworth - self.getNetworth()
    def completeRun(self,gametime):
        """Completes the run"""
        self.realWrldEndTime = datetime.now()
        errors.addMessage(f"Goal Reached - Run Completed",coords=(960,300),lifeTime=360,txtSize=100)
        errors.addMessage(f'Now in View Mode',coords=(960,480),lifeTime=360)
        self.runManager.completeRun(self,gametime)
    def getState(self,gametime):
        """Returns the state of the run"""
        if self.state == "complete":
            return "complete"
        if self.getNetworthDelta() <= 0:# if the networth has been reached
            if self.state == "live":# if the run is still live
                self.completeRun(gametime)
            return "complete"
        return 'live'
    def getTimeToComplete(self):
        """Returns the amount of time it took to complete the goal"""
        if self.realWrldEndTime is None:
            return None
        return (self.realWrldEndTime - self.startTime).days
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
        self.completedRuns : dict[str:list[GameRun]] = {'Career':[],'Blitz':[],'Goal':[]}# the complete runs that the player has don
        self.loadPastRuns()
    def reset(self):
        self.pastRuns = {'Career':[],'Blitz':[],'Goal':[]}
        self.completedRuns = {'Career':[],'Blitz':[],'Goal':[]}
        self.loadPastRuns()
    def getRuns(self,mode:str):
        """Returns the runs of the mode"""
        return self.pastRuns[mode]
    def getRunsCompleted(self,mode:str):
        """Returns the completedRuns runs of the mode"""
        return self.completedRuns[mode]
    
    def getAllRuns(self,inList=False):
        """Returns all the runs in a dictionary or list if inList is True"""
        if inList:
            return [run for mode in self.pastRuns for run in self.pastRuns[mode]]
        return self.pastRuns
    def getAllCompletedRuns(self,inList=False):
        """Returns all the complete runs in a dictionary or list if inList is True"""
        if inList:
            return [run for mode in self.completedRuns for run in self.completedRuns[mode]]
        return self.completedRuns
    def completeRun(self,run:GoalRun|BlitzRun,gametime):
        """Completes the run"""
        self.completedRuns[run.gameMode].append(run)
        self.removeRun(run)
        run.state = "complete"
        run.saveRun(gametime.time)# saves the run to the file
    def removeRun(self,run:GameRun):
        """Removes the run from either the past or complete runs"""
        if run in self.pastRuns[run.gameMode]:
            self.pastRuns[run.gameMode].remove(run)
            # os.remove(run.getFileDir())
            shutil.rmtree(run.getFileDir())

        elif run in self.completedRuns[run.gameMode]:
            self.completedRuns[run.gameMode].remove(run)
            os.remove(run.getFileDir())
    def addRun(self,run:GameRun):
        """Adds the run to the past runs"""
        self.pastRuns[run.gameMode].append(run)
    def getRanking(self,run:GameRun):
        """Returns the ranking of the runs in the mode"""
        runs = self.pastRuns[run.gameMode]+self.completedRuns[run.gameMode]
        if isinstance(run, GoalRun):
            runs = [run for run in runs if run.getTimeToComplete() != None]
            runs.sort(key=lambda x:x.getTimeToComplete(),reverse=True)
        else:
            runs.sort(key=lambda x:x.getNetworth(),reverse=True)
            
        
        # runs.append(run)
        
        rank = runs.index(run) + 1 if run in runs else None
        return rank
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
                        unlocks = {key:modeSpecificInfo[key] for key in ["Pre-Made Options","Custom Options","Stock Reports"]}
                        upgrades = {key:modeSpecificInfo[key] for key in ["Asset Storage","Loan Interest","Max Loan Amount","Tax Rate"]}
                        sandBox = modeSpecificInfo.popitem()[1]
                    run = CareerRun(basicInfo['name'],basicInfo['assetSpread'],basicInfo['gameDate'],basicInfo['iconIndex'],unlocks,upgrades,sandBox,self,startTime=basicInfo['startTime'],lastPlayed=basicInfo['lastPlayed'])
                elif mode == 'Blitz':
                    run = BlitzRun(basicInfo['name'],basicInfo['assetSpread'],basicInfo['gameDate'],basicInfo['iconIndex'],modeSpecificInfo['duration'],self,endGameDate=modeSpecificInfo['endGameDate'],startTime=basicInfo['startTime'],realWrldEndTime=modeSpecificInfo['endTime'],lastPlayed=basicInfo['lastPlayed'])
                elif mode == 'Goal':
                    run = GoalRun(basicInfo['name'],basicInfo['assetSpread'],basicInfo['gameDate'],basicInfo['iconIndex'],modeSpecificInfo['goalNetworth'],self,startTime=basicInfo['startTime'],realWrldEndTime=modeSpecificInfo['endTime'],lastPlayed=basicInfo['lastPlayed'])
                self.pastRuns[mode].append(run)

        for mode in self.completedRuns:
            for runName in os.listdir(os.path.join("Saves","complete",mode)):
                with open(os.path.join("Saves","complete",mode,runName,"BasicInfo.json"),"r") as f:
                    basicInfo = json.load(f)
                with open(os.path.join("Saves","complete",mode,runName,"ModeSpecificInfo.json"),"r") as f:
                    modeSpecificInfo : dict = json.load(f)
                if mode == 'Career':
                    if len(modeSpecificInfo) > 0:
                        unlocks = {key:modeSpecificInfo[key] for key in ["Pre-Made Options","Custom Options","Stock Reports"]}
                        upgrades = {key:modeSpecificInfo[key] for key in ["Asset Storage","Loan Interest","Max Loan Amount","Tax Rate"]}
                        sandBox = modeSpecificInfo.popitem()[1]
                    run = CareerRun(basicInfo['name'],basicInfo['assetSpread'],basicInfo['gameDate'],basicInfo['iconIndex'],unlocks,upgrades,sandBox,self,startTime=basicInfo['startTime'],lastPlayed=basicInfo['lastPlayed'],state='complete')
                elif mode == 'Blitz':
                    run = BlitzRun(basicInfo['name'],basicInfo['assetSpread'],basicInfo['gameDate'],basicInfo['iconIndex'],modeSpecificInfo['duration'],self,endGameDate=modeSpecificInfo['endGameDate'],startTime=basicInfo['startTime'],realWrldEndTime=modeSpecificInfo['endTime'],lastPlayed=basicInfo['lastPlayed'],state='complete')
                elif mode == 'Goal':
                    run = GoalRun(basicInfo['name'],basicInfo['assetSpread'],basicInfo['gameDate'],basicInfo['iconIndex'],modeSpecificInfo['goalNetworth'],self,startTime=basicInfo['startTime'],realWrldEndTime=modeSpecificInfo['endTime'],lastPlayed=basicInfo['lastPlayed'],state='complete')
                self.completedRuns[mode].append(run)
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
    