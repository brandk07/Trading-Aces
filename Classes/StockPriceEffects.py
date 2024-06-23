from random import randint
from datetime import datetime,timedelta
from Classes.Gametime import GameTime
from Defs import *

class StockPriceEffects:
    def __init__(self,parentStock,gametime:GameTime) -> None:
        self.effectsDict = {}# {modiferName : [ogAmount,currentAmount,enlapsedtime:int,duration:int]}
        # self.pastReports = []# [performance,time of report,quarter of report [1,2,3,4]]
        self.pastReports = [(gametime.time-timedelta(days=91)*i-timedelta(days=randint(30,60)),((7-i)%4)+1,randint(-1000,1000)/100) for i in range(8)]# [time of report,quarter of report,performance]
        self.futureReports:list[datetime,int] = [(gametime.time+timedelta(days=91)*i+timedelta(days=randint(30,60)),i+1) for i in range(4)]# [time of report,quarter]
        self.modifers = {"priceTrend":0,"tempVolatility":0}
        self.parentStock = parentStock
        # for report in self.pastReports:
        #     print(report)
    def randomQuartDate(self):
        """Returns a random date for a quarterly report"""
        return timedelta(days=91)+timedelta(days=randint(30,60))
    def generateQuarterlyReport(self,gametime:GameTime) -> list:
        """Generates a quarterly report"""
        def findPercent(likelyPercent) -> float:
            result = 0
            randomx = randint(0,100)# random spot on the formula
            if likelyHood > 0.5:
                result = 2**((randomx-78)/3)+(randomx/2)+likelyPercent-50
            else:
                result = (randomx/2)-2**((randomx-22)/-3)+likelyPercent
            result /= 10; result += 5
            return result

        likelyHood = self.getQuarterlyLikelyhood(gametime)
        performance = findPercent(likelyHood)
    
        self.effectsDict["priceTrend"] = [performance,performance,randint(100,1800),0]# New  price trend that will last for 30 seconds
        if self.pastReports == 8:# if there are 8 reports
            self.pastReports.pop(0)# remove the oldest report
        
        self.futureReports.append((self.futureReports[-1][0]+self.randomQuartDate(),(self.futureReports[-1][1]) % 4 + 1))
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
        perfEquation = lambda x : 8*x+65
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
            # print("Generating Quarterly Report",self.parentStock.name)
            self.generateQuarterlyReport(gametime)
            # self.futureReports.pop(0)
            # self.futureReports.append((gametime.time+timedelta(days=91)+timedelta(days=randint(30,60)),(self.futureReports[-1][1]+1)%4))