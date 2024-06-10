from random import randint
from datetime import datetime,timedelta

class StockPriceEffects:
    def __init__(self,parentStock) -> None:
        self.effectsDict = {}# {modiferName : [ogAmount,currentAmount,enlapsedtime:int,duration:int]}
        self.pastReports = []# [performance,time of report]
        self.modifers = {"priceTrend":0,"tempVolatility":0}
        self.parentStock = parentStock
    
    def generateQuarterlyReport(self,gametime:datetime) -> list:
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

        likelyHood = self.getQuarterlyLikelyhood()
        performance = findPercent(likelyHood)
    
        self.effectsDict["priceTrend"] = [performance,performance,randint(100,1800),0]# New  price trend that will last for 30 seconds
        if self.pastReports == 4:# if there are 4 reports
            self.pastReports.pop(0)# remove the oldest report
        self.pastReports.append([performance,gametime])
        return [performance,gametime]

    def getQuarterlyLikelyhood(self):
        """Gives the likelyhood that the quarterly report will meet expectations"""
        percent = 0
        # ---Past reports accounts for 20% of the likelyhood-----
        for performance,time in self.pastReports:
            percent += 5 if performance > 0 else 0# if the performance met expectations, add 5%
        
        # ---Stock performance accounts for 80% of the likelyhood-----
        
        



    def updateEffects(self,gametime:datetime):
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

                    
                    
                