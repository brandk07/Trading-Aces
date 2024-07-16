from random import randint
from datetime import datetime,timedelta,date
from Classes.Gametime import GameTime
from Defs import *

class StockPriceEffects:
    def __init__(self,parentStock,gametime:GameTime) -> None:
        self.effectsDict = {}# {modiferName : [ogAmount,currentAmount,enlapsedtime:int,duration:int]}
        # self.pastReports = []# [time of report,quarter of report [1,2,3,4],performance]
        currQ = self.getCurrentQuarter(gametime)
        self.pastReports = [(self.randomQuartDate(((i)%4)+1,gametime,True),((i)%4)+1,randint(-1000,1000)/100) for i in range(currQ,currQ-4,-1)]# [time of report,quarter of report,performance]
        # self.futureReports:list[datetime,int] = [(self.randomQuartDate((i)%4+1,gametime),(i)%4+1) for i in range(currQ,currQ-4,-1)]# [time of report,quarter]
        self.futureReports:list[datetime,int] = [(self.randomQuartDate((i)%4+1,gametime),(i)%4+1) for i in range(currQ,currQ+4)]# [time of report,quarter]
        self.pastReports.sort(key=lambda x: x[0],reverse=True)
        self.futureReports.sort(key=lambda x: x[0])
        self.modifers = {"priceTrend":0,"tempVolatility":0}
        self.parentStock = parentStock
        # for report in self.pastReports:
        #     print(report)
    def getCurrentQuarter(self,gametime:GameTime):
        """Returns the current quarter"""
        return (gametime.time.month-1)//3+1
    def randomQuartDate(self,quarter,gametime:GameTime,past=False):
        """Returns a random date for a quarterly report, Quarter 1-4"""
        # create a datetime object with the same year as gametime, but january 1st
        # year = gametime.time.year+extraYears
        print(quarter)
        january_1st = datetime(gametime.time.year, 1, 1)
        print((quarter-1)*timedelta(days=75),"Days",quarter,quarter-1)
        quartTime = january_1st+((quarter-1)*timedelta(days=90))+timedelta(days=randint(30,90))
        print(quartTime,gametime)

        year = gametime.time.year + 1 if quartTime < gametime.time else gametime.time.year
        if past:# override the year with opposite
            year = gametime.time.year - 1 if quartTime > gametime.time else gametime.time.year
            if quarter == self.getCurrentQuarter(gametime):
                year = gametime.time.year-1
            
        print(year)
        quartTime = datetime(year, quartTime.month, quartTime.day)
        print(quartTime,"//////////////////////////////")
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
        print(likelyHood,performance,"New report")
    
        self.effectsDict["priceTrend"] = [performance,performance,randint(100,1800),0]# New  price trend that will last for 30 seconds
        if self.pastReports == 8:# if there are 8 reports
            self.pastReports.pop(0)# remove the oldest report
        newQuarter = self.futureReports[-1][1] % 4 + 1

        # extraYears = 1 if self.pastReports[0][0].year == gametime.time.year else 0# if the report is in the same year as the last report, add a year
        self.futureReports.append((self.randomQuartDate(newQuarter,gametime),newQuarter))
        self.pastReports.insert(0,[self.futureReports[0][0],self.futureReports[0][1],performance])
        self.futureReports.pop(0)
        return self.pastReports[-1]
    
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
        tempDict = self.effectsDict.copy()

        for var,(ogAmount,currentAmount,enlapsed,duration) in (self.effectsDict.items()):
            if enlapsed > duration or currentAmount == 0:# if the effect has been active for the duration or the effect has been lowered to 0
                tempDict.pop(var)
            else:
                if ogAmount > duration:
                    modifier = ogAmount/duration
                    self.effectsDict[var][1] -= modifier# lower the trend by the amount
                    self.modifers[var] -= modifier# lower the trend by the amount
                # finding how many seconds should pass before the trend should be lowered
                ratio = duration/ogAmount
                if enlapsed % ratio == 0:# if the trend should be lowered
                    self.effectsDict[var][1] -= 1
                    self.modifers[var] -= 1
                self.effectsDict[var][2] += 1

        self.effectsDict = tempDict
                    
                    
    def update(self,gametime:GameTime,screen:pygame.Surface):
        """Updates the effects"""
        self.updateEffects(gametime)
        
        
        # print(gametime.time < self.futureReports[0][0],self.parentStock.name)
        if gametime.time > self.futureReports[0][0]:
            print("Generating Quarterly Report",self.parentStock.name)
            self.generateQuarterlyReport(gametime)
            # self.futureReports.pop(0)
            # self.futureReports.append((gametime.time+timedelta(days=91)+timedelta(days=randint(30,60)),(self.futureReports[-1][1]+1)%4))