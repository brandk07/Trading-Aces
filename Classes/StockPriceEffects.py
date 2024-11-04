from random import randint
from datetime import datetime,timedelta,date
from Classes.Gametime import GameTime
from Defs import *
import calendar

class Report:
    def __init__(self,time:datetime,quarter:int,performance:float=None) -> None:
        self.quarter = quarter
        self.time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S") if isinstance(time,str) else time
        assert isinstance(self.time,datetime), f"Time must be a datetime object : Currently {type(self.time)}"
        if performance:
            self.type = "past"
            self.performance = performance
        else:
            self.type = "future"
            self.performance = None
        
    def getTime(self):
        return self.time
    def getQ(self):
        return self.quarter
    def getPerf(self):
        assert self.type == "past", "Performance is only available for past reports"
        return self.performance
    def savingInputs(self):
        return (str(self.time),self.quarter,self.performance)

class StockPriceEffects:
    def __init__(self,parentStock,gametime:GameTime,fileData=None) -> None:
        self._effectsDict = {}# {modiferName : [modifierAmount,duration:int,decayRate]} DON'T USE THIS DIRECTLY

        self.getQuart = lambda timeobj : (timeobj.month-1)//3+1
        currQ = self.getCurrentQuarter(gametime)
        if fileData == None:
            # [time of report,quarter of report,performance]
            self.pastReports:list[Report] = self.createPastReports(gametime,currQ)# Creates past reports if none are given
            self.futureReports:list[Report] = self.createFutureReports(gametime,currQ)# [time of report,quarter]
        else: 
            self.pastReports,self.futureReports = self.dataFromFile(fileData)
        

        self._modifers = {"priceTrend":0,"volatility":0}
        self.parentStock = parentStock

    def createPastReports(self,gametime:GameTime,currQ:int):
        """Creates the past reports for the stock"""
        pastList = []
        for i in range(currQ-2,currQ-6,-1):
            pastList.append(Report(self.randomQuartDate((i%4)+1,gametime,True),(i%4)+1,randint(-1000,1000)/100))
        return pastList
    
    def createFutureReports(self,gametime:GameTime,currQ:int):
        """Creates the future reports for the stock"""
        futureList = []
        for i in range(currQ-1,currQ+3):
            futureList.append(Report(self.randomQuartDate((i%4)+1,gametime),(i%4)+1,None))
        return futureList

    def dataFromFile(self,fileData):
        """Returns the past and future reports from a file"""
        pastReports = [Report(*data) for data in fileData[0]]
        futureReports = [Report(*data) for data in fileData[1]]
        return pastReports,futureReports
    
    def getCurrentQuarter(self,gametime:GameTime):
        """Returns the current quarter [1,2,3,4]"""
        return (gametime.time.month-1)//3+1

    

    def randomQuartDate(self,quarter,gametime:GameTime,past=False):
        """Returns a random date for a quarterly report, Quarter 1-4"""
        def daysInQuarter(quarter:int,gametime:GameTime):
            """Returns the # of days from beginning of the year to the end of the quarter"""
            assert quarter in range(1, 5), "Quarter must be between 1 and 4"
            # Calculate the number of days in each month of the quarter
            days_in_quarter = 0
            for month in range(1, (quarter-1)*3 + 1):
                days_in_quarter += calendar.monthrange(gametime.time.year, month)[1]
            return days_in_quarter
        def daysInMonthRange(startMonth:int,endMonth:int,gametime:GameTime):
            """Includes the end month"""
            days_in_month_range = 0
            for month in range(startMonth,endMonth+1):
                days_in_month_range += calendar.monthrange(gametime.time.year, month)[1]
                # print(days_in_month_range,calendar.monthrange(gametime.time.year, month)[1],month)
            return days_in_month_range
    
        january_1st = datetime(gametime.time.year, 1, 1)# Really a placeholder datetime object

        timeOff = (timedelta(days=daysInQuarter(quarter,gametime)))+timedelta(days=randint(0,90))#Normal time offset
        if not past and quarter == self.getCurrentQuarter(gametime) and self.pastReports[0].getQ() != self.getCurrentQuarter(gametime):# if the report is in the current quarter
            # print(f"Current quarter {quarter} {daysInQuarter(quarter,gametime)}, {daysInMonthRange(1,gametime.time.month-1,gametime)} {gametime.time.day}")
            daysPastQuart = daysInMonthRange(1,gametime.time.month-1,gametime)-daysInQuarter(quarter,gametime)+gametime.time.day
            # daysPastQuart = int((gametime.time.month-1)*32+gametime.time.day-((quarter-1)*90))+1
            # print(daysPastQuart,"Days past quart",print(range(min(89,daysPastQuart),90)))
            timeOff = (timedelta(days=daysInQuarter(quarter,gametime)))+timedelta(days=randint(min(89,daysPastQuart),90))# the first day of the quarter
            # print(timeOff,"Time off")

        quartTime = january_1st+timeOff# add the time offset

        year = gametime.time.year + 1 if quartTime < gametime.time else gametime.time.year# make sure it is in the future
        if past:# override the year with opposite if it should be in the past
            year = gametime.time.year - 1 if quartTime > gametime.time else gametime.time.year
            if quarter == self.getCurrentQuarter(gametime):# if it was really long ago
                year = gametime.time.year-1
        # print(year,quartTime,quartTime.month,quartTime.day)
        quartTime = datetime(year, quartTime.month, min(28,quartTime.day))# creating a new datetime object with the new year
        # if not past:
            # print('/'*10,'\n',quartTime, gametime)
            # print(self.pastReports[0][1], self.getCurrentQuarter(gametime), self.pastReports[0][1] == self.getCurrentQuarter(gametime),not past and self.getQuart(quartTime) == self.getCurrentQuarter(gametime) )
        if not past and self.getQuart(quartTime) == self.getCurrentQuarter(gametime) and self.pastReports[0].getQ() == self.getCurrentQuarter(gametime) and quartTime.year == gametime.time.year:# if the report is in the same quarter
            # print(gametime.time,quartTime,(gametime.time-quartTime).days,'Same quarter')
            quartTime = quartTime + timedelta(days=365)# move the report to next year at that time

        # offcase where the report is in the same quarter but is earlier in the year (so didn't trigger above), but should be a long way in the past
        if past and self.getQuart(quartTime) == self.getCurrentQuarter(gametime) and quartTime > gametime.time:
            # print(gametime.time,quartTime,(gametime.time-quartTime).days,'Same quarter Past')
            quartTime = quartTime - timedelta(days=365)# move the report to next year at that time
        return quartTime
    
    def generateQuarterlyReport(self,gametime:GameTime) -> list:
        """Generates a quarterly report"""
        def findPercent(likelyPercent) -> float:
            result = 0
            randomx = randint(0,100)# random spot on the formula
            # print(randomx,"Randomx")
            if likelyHood > 50:
                result = (2**((randomx-78)/3)+(randomx/2)+(likelyPercent/2)-50)/10
            else:
                result = ((randomx/2)-2**((randomx-22)/-3)+(likelyPercent/2))/10 - 5

            return result

        likelyHood = self.getQuarterlyLikelyhood(gametime)
        performance = findPercent(likelyHood)
        # print(likelyHood,performance,"New report")
    
        # self.__effectsDict["priceTrend"] = [performance,performance,randint(100,1800),0]# New  price trend that will last for 30 seconds
        if len(self.pastReports) == 5:# if there are 8 reports
            self.pastReports.pop(0)# remove the oldest report
        newQuarter = self.futureReports[-1].getQ() % 4 + 1

        # extraYears = 1 if self.pastReports[0][0].year == gametime.time.year else 0# if the report is in the same year as the last report, add a year
        self.pastReports.insert(0,Report(self.futureReports[0].getTime(),self.futureReports[0].getQ(),performance))
        self.futureReports.append(Report(self.randomQuartDate(newQuarter,gametime),newQuarter))
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
    
    # def getPastPerfLikelyhood(self,gametime:GameTime):
    #     """Used as a part of the calculating the quarterly likelyhood (Can be any amount)"""
    #     perfEquation = lambda x : 2*x+70
    #     percent = ((self.parentStock.price/self.parentStock.getPointDate(self.pastReports[0][0],gametime))-1)*100
        
    #     return max(0,min(88,perfEquation(percent)))# the stock performance over the last quarter
    def getLikelyHoods(self,gametime:GameTime):
        """Returns the components that go into making the quarterly likelyhood,
        [0] is the % that comes from the reports that met expectations
        [1] is the % that comes from the stock performance since the last report and over the last year"""
        perfEquation = lambda x : 2*x+70
        tempP = ((self.parentStock.price/self.parentStock.getPointDate(self.pastReports[0].getTime(),gametime))-1)*50# half from last report
        tempP += self.parentStock.getPercent("1Y")/2# half from the last year
        perlikelyhood = max(0,min(88,perfEquation(tempP)))# the stock performance over the last quarter

        return 3*len([report.getPerf() for report in self.pastReports[:4] if report.getPerf() > 0]), perlikelyhood

    def getQuarterlyLikelyhood(self,gametime:GameTime):
        """Gives the likelyhood that the quarterly report will meet expectations"""
        # ---Past reports accounts for 12% of the likelyhood-----
        # percent += 3*len([p for (t,q,p) in self.pastReports[:4] if p > 0])# if the performance met expectations, add 3%
        # # ---Stock performance accounts for 80% of the likelyhood-----
        # # percent += self.getPastPerfLikelyhood(gametime)
        # perfEquation = lambda x : 2*x+70
        # tempP = ((self.parentStock.price/self.parentStock.getPointDate(self.pastReports[0][0],gametime))-1)*100
        # percent += max(0,min(88,perfEquation(tempP)))# the stock performance over the last quarter
        pastReportsPer,PerfPercent = self.getLikelyHoods(gametime)

        return pastReportsPer + PerfPercent
        

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


       
                    
                    
    def update(self,gametime:GameTime,screen:pygame.Surface,player):
        """Updates the effects"""
        self.updateEffects(gametime)

        # if self.parentStock.name == "FARM":
        #     print(self._effectsDict)
        #     print(self._modifers)
        #     print(self.parentStock.volatility)
        
        
        # print(gametime.time < self.futureReports[0][0],self.parentStock.name)
        if gametime.time > self.futureReports[0].getTime():# if it is time for the next report
            print("Generating Quarterly Report",self.parentStock.name)
            self.generateQuarterlyReport(gametime)
            player.payDividend(stockObj=self.parentStock)
            # self.futureReports.pop(0)
            # self.futureReports.append((gametime.time+timedelta(days=91)+timedelta(days=randint(30,60)),(self.futureReports[-1][1]+1)%4))