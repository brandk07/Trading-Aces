from random import randint
from datetime import datetime,timedelta,date
from Classes.Gametime import GameTime
from Defs import *

class StockPriceEffects:
    def __init__(self,parentStock,gametime:GameTime) -> None:
        self._effectsDict = {}# {modiferName : [modifierAmount,duration:int,decayRate]} DON'T USE THIS DIRECTLY

        self.getQuart = lambda timeobj : (timeobj.month-1)//3+1
        currQ = self.getCurrentQuarter(gametime)
        print(currQ,[(i%4)+1 for i in range(currQ-2,currQ-6,-1)])
        # self.pastReports = []# [time of report,quarter of report [1,2,3,4],performance]

        self.pastReports = [(self.randomQuartDate((i%4)+1,gametime,True),(i%4)+1,randint(-1000,1000)/100) for i in range(currQ-2,currQ-6,-1)]# [time of report,quarter of report,performance]
        # self.futureReports:list[datetime,int] = [(self.randomQuartDate((i)%4+1,gametime),(i)%4+1) for i in range(currQ,currQ-4,-1)]# [time of report,quarter]
        self.futureReports:list[datetime,int] = [(self.randomQuartDate((i)%4+1,gametime),(i)%4+1) for i in range(currQ-5,currQ-1)]# [time of report,quarter]
        # self.pastReports.sort(key=lambda x: x[0],reverse=True)
        # self.futureReports.sort(key=lambda x: x[0])
        self._modifers = {"priceTrend":0,"volatility":0}
        self.parentStock = parentStock
        # for report in self.pastReports:
        #     print(report)
        
    def getCurrentQuarter(self,gametime:GameTime):
        """Returns the current quarter [1,2,3,4]"""
        return (gametime.time.month-1)//3+1

    def randomQuartDate(self,quarter,gametime:GameTime,past=False):
        """Returns a random date for a quarterly report, Quarter 1-4"""

        january_1st = datetime(gametime.time.year, 1, 1)# Really a placeholder datetime object

        timeOff = ((quarter-1)*timedelta(days=90))+timedelta(days=randint(0,90))#Normal time offset
        if not past and quarter == self.getCurrentQuarter(gametime):# if the report is in the current quarter
            daysPastQuart = int((gametime.time.month-1)*30+gametime.time.day-((quarter-1)*90))+1
            print(daysPastQuart,"Days past quart",print(range(min(89,daysPastQuart),90)))
            timeOff = ((quarter-1)*timedelta(days=90))+timedelta(days=randint(min(89,daysPastQuart),90))# the first day of the quarter
            print(timeOff,"Time off")

        quartTime = january_1st+timeOff# add the time offset

        year = gametime.time.year + 1 if quartTime < gametime.time else gametime.time.year# make sure it is in the future
        if past:# override the year with opposite if it should be in the past
            year = gametime.time.year - 1 if quartTime > gametime.time else gametime.time.year
            if quarter == self.getCurrentQuarter(gametime):# if it was really long ago
                year = gametime.time.year-1
        # print(year,quartTime,quartTime.month,quartTime.day)
        quartTime = datetime(year, quartTime.month, min(28,quartTime.day))# creating a new datetime object with the new year
        if not past and self.getQuart(quartTime) == self.getCurrentQuarter(gametime) and self.pastReports[-1][1] != self.getCurrentQuarter(gametime):# if the report is in the same quarter
            # print(gametime.time,quartTime,(gametime.time-quartTime).days,'Same quarter')
            quartTime = quartTime + timedelta(days=365)# move the report to next year at that time

        # offcase where the report is in the same quarter but is earlier in the year (so didn't trigger above), but should be a long way in the past
        if past and self.getQuart(quartTime) == self.getCurrentQuarter(gametime) and quartTime > gametime.time:
            print(gametime.time,quartTime,(gametime.time-quartTime).days,'Same quarter Past')
            quartTime = quartTime - timedelta(days=365)# move the report to next year at that time
        return quartTime
    
    def generateQuarterlyReport(self,gametime:GameTime) -> list:
        """Generates a quarterly report"""
        def findPercent(likelyPercent) -> float:
            result = 0
            randomx = randint(0,100)# random spot on the formula
            print(randomx,"Randomx")
            if likelyHood > 50:
                result = (2**((randomx-78)/3)+(randomx/2)+(likelyPercent/2)-50)/10
            else:
                result = ((randomx/2)-2**((randomx-22)/-3)+(likelyPercent/2))/10 - 5

            return result

        likelyHood = self.getQuarterlyLikelyhood(gametime)
        performance = findPercent(likelyHood)
        # print(likelyHood,performance,"New report")
    
        # self.__effectsDict["priceTrend"] = [performance,performance,randint(100,1800),0]# New  price trend that will last for 30 seconds
        if self.pastReports == 8:# if there are 8 reports
            self.pastReports.pop(0)# remove the oldest report
        newQuarter = self.futureReports[-1][1] % 4 + 1

        # extraYears = 1 if self.pastReports[0][0].year == gametime.time.year else 0# if the report is in the same year as the last report, add a year
        self.futureReports.append((self.randomQuartDate(newQuarter,gametime),newQuarter))
        self.pastReports.insert(0,[self.futureReports[0][0],self.futureReports[0][1],performance])
        self.futureReports.pop(0)

        self.applyPriceChange(performance)
        self.parentStock.resetTrends()
        
        return self.pastReports[-1]

    def applyPriceChange(self,performance:float):
        """Applies the immediate price change to the stock and gives a temporary volatility change"""
        self.parentStock.price *= 1+(performance/100)*(randint(40,125)/100)# Apply immediate price change

        self.addEffect("volatility",-performance*2,randint(40,150))# Add a temporary volatility change 2-8 minutes
                
    def addEffect(self,modiferName:str,amount:float,durationMins:int):
        """Adds a new effect to the stock"""
        self._effectsDict[modiferName] = [amount,durationMins*60,amount/(durationMins*60)]# [modifierAmount,duration:int,decayRate]
        self._modifers[modiferName] = amount
    
    def getReportLikelyhood(self):
        """Used as a part of the calculating the quarterly likelyhood (18% of the likelyhood)"""
        percent = 0
        for (time,quarter,performance) in self.pastReports[:4]:# for the last 4 reports
            percent += 3 if performance > 0 else 0# if the performance met expectations, add 5%

        return 3*len([p for (t,q,p) in self.pastReports[:4] if p > 0])
        # return percent
    def getPastPerfLikelyhood(self,gametime:GameTime):
        """Used as a part of the calculating the quarterly likelyhood (Can be any amount)"""
        perfEquation = lambda x : 2*x+70
        percent = ((self.parentStock.price/self.parentStock.getPointDate(self.pastReports[0][0],gametime))-1)*100
        # print(self.parentStock.getPointDate(self.pastReports[0][0],gametime))
        # print(percent)
        # print(self.parentStock.getPercentDate(self.pastReports[0][0],gametime))
        
        return max(0,min(88,perfEquation(percent)))# the stock performance over the last quarter
        
    def getQuarterlyLikelyhood(self,gametime:GameTime):
        """Gives the likelyhood that the quarterly report will meet expectations"""
        percent = 0
        # ---Past reports accounts for 12% of the likelyhood-----
        # print(self.pastReports)
        percent += self.getReportLikelyhood()
        # print(f"Percent after {percent} after past reports")
        # ---Stock performance accounts for 80% of the likelyhood-----
        
        # print(self.parentStock.getPercentDate(self.pastReports[0][1],gametime))
        # print(perfEquation(self.parentStock.getPercentDate(self.pastReports[0][1],gametime)))
        percent += self.getPastPerfLikelyhood(gametime)
        # print(f"Percent after {percent} after stock performance")
        return percent
        

    def updateEffects(self,gametime:GameTime):
        """Updates all the effects and effect attributes"""
        """Effects are lowered throughout their lifetime (duration) so that when duration hits zero the effect has already been lowered"""
        keystoRemove = []

        for var,(currentAmount,duration,decayRate) in (self._effectsDict.items()):
            if duration == 0 or currentAmount == 0:# if the effect has been active for the duration or the effect has been lowered to 0
                keystoRemove.append(var)
            else:
                self._effectsDict[var][1] -= 1# lower the duration by 1
                self._effectsDict[var][0] -= decayRate# lower the trend by the decay rate

                self._modifers[var] -= decayRate# lower the modifer by the decay rate

        for key in keystoRemove:
            self._effectsDict.pop(key)


       
                    
                    
    def update(self,gametime:GameTime,screen:pygame.Surface):
        """Updates the effects"""
        self.updateEffects(gametime)

        # if self.parentStock.name == "FARM":
        #     print(self._effectsDict)
        #     print(self._modifers)
        #     print(self.parentStock.volatility)
        
        
        # print(gametime.time < self.futureReports[0][0],self.parentStock.name)
        if gametime.time > self.futureReports[0][0]:
            print("Generating Quarterly Report",self.parentStock.name)
            self.generateQuarterlyReport(gametime)
            # self.futureReports.pop(0)
            # self.futureReports.append((gametime.time+timedelta(days=91)+timedelta(days=randint(30,60)),(self.futureReports[-1][1]+1)%4))