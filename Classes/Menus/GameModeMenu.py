import pygame
from Defs import *
from Classes.Menus.Menu import Menu
from Classes.imports.UIElements.PieChart import PieChart
from Classes.imports.UIElements.SideScroll import VerticalScroll,ModeMenuRunCard,UnlockUpgradeCard
from Classes.BigClasses.RunTypes import *
from Classes.imports.UIElements.BarGraph import BarGraph
from Classes.imports.UIElements.SelectionElements import MenuSelection
from Classes.imports.StockVisualizer import StockVisualizer
from Classes.imports.UIElements.OrderBox import OrderBox
from Classes.imports.UIElements.SelectionElements import SelectionBar
from Classes.imports.Bar import ProgressBar

class GameModeMenu(Menu):
    def __init__(self,stocklist,player,pastRuns:dict,currentRun,gametime) -> None:
        """Gets the past runs {'Blitz':[BlitzRun : obj],'Career':[],'Goal':[]}"""
        super().__init__()
        self.loadRuns(pastRuns)# loads the runs from the save file
        self.currentRun = currentRun
        match self.currentRun.gameMode:
            case 'Blitz':
                self.blitz : BlitzScreen = BlitzScreen(self.blitzReports,self.currentRun)
            case 'Career':
                self.career = CareerScreen(self.careerReports,self.currentRun,player,gametime)
            case 'Goal':
                self.goal = GoalScreen(self.goalReports,self.currentRun)
        self.player = player
        self.stocklist = stocklist
    

        self.gameMode = self.currentRun.gameMode# career, goal, or blitz

        self.menudrawn = True
    def loadRuns(self,pastRuns:dict):
        self.blitzReports = pastRuns['Blitz'].copy()# full of BlitzRun objects
        self.careerReports = pastRuns['Career'].copy()# full of CareerRun objects
        self.goalReports = pastRuns['Goal'].copy()# full of GoalRun objects

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, player, gametime):

        match self.gameMode:
            case 'Blitz':
                self.blitz.draw(screen,gametime)
            case 'Career':
                self.career.draw(screen,gametime)
            case 'Goal':
                self.goal.draw(screen,gametime)

class BlitzAndGoalScreen:
    def __init__(self,pastRuns:list[BlitzRun|GoalRun],curentRun:BlitzRun|GoalRun) -> None:
        self.pastRuns : list[BlitzRun|GoalRun] = pastRuns# PAST RUNS DOESNT INCLUDE THE CURRENT RUN
        self.currentRun : BlitzRun|GoalRun = curentRun
        if self.currentRun in self.pastRuns:
            self.pastRuns.remove(self.currentRun)

        self.currBarGraph = BarGraph(self.currentRun.name,(205,565),(520,300))
        self.selcBarGraph = BarGraph(self.currentRun.name,(750,565),(520,300))
        self.pieChart = PieChart((745,125),(520,430))

        self.sideScrollCards = {}
        self.vertScroll = VerticalScroll((1290,195),(610,770),(570,170))
        for run in self.pastRuns:
            self.sideScrollCards[run.name] = (ModeMenuRunCard(self.vertScroll,run))
        self.vertScroll.loadCards(list(self.sideScrollCards.values()))

        self.selectedRun : BlitzRun|GoalRun = None if len(self.pastRuns) == 0 else self.pastRuns[0]
        if len(self.pastRuns) > 0:
            run = max(self.pastRuns,key=lambda x:x.getNetworth())# gets the best run to start
            self.vertScroll.setCard(obj=self.sideScrollCards[run.name])# sets the card to the best run
    
    def drawBarGraphs(self,screen):
        colors = [(255, 205, 78),(191, 85, 178),(239, 131, 84),(12, 89, 27)]#[stocks, options, indexFunds, cash]
        for i in range(4):
            x = 215+i*300
            pygame.draw.rect(screen,colors[i],(x,930,20,20),border_radius=5)
            drawCenterTxt(screen,['Stocks','Options','Index Funds','Cash'][i],45,(200,200,200),(x+30,940),centerX=False)


        pygame.draw.rect(screen,(0,0,0),(195,560,540,355),5,10)# draws the box for the current run
        maxScale = max(self.currentRun.getAssets()[:-1]) if self.selectedRun == None else max(self.selectedRun.getAssets()[:-1]+self.currentRun.getAssets()[:-1])
        # print(maxScale)
        self.currBarGraph.updateValues(self.currentRun.getAssets()[:-1],colors,['$']*4)
        self.currBarGraph.draw(screen,absoluteScale=maxScale)
        if self.selectedRun != None:
            pygame.draw.rect(screen,(0,0,0),(745,560,540,355),5,10)
            self.selcBarGraph.changeName(self.selectedRun.name)
            self.selcBarGraph.updateValues(self.selectedRun.getAssets()[:-1],colors,['$']*4)
            self.selcBarGraph.draw(screen,absoluteScale=maxScale)
        else:
            drawCenterTxt(screen,"No Selected Run",65,(210, 50, 50),(1015,650),centerY=False)

    def drawPieChart(self,screen):
        colors = [(255, 205, 78),(191, 85, 178),(239, 131, 84),(12, 89, 27)]#[stocks, options, indexFunds, cash]
        names = ['Stocks','Options','Index Funds','Cash']
        values = [(val,name,color) for (val,name,color) in zip(self.currentRun.assetSpread[:-1],names,colors)]
        self.pieChart.updateData(values)
        self.pieChart.draw(screen,"",txtSize=35)

    def drawVertScroll(self,screen):
        drawCenterTxt(screen,"Other Runs",80,(200,200,200),(1595,110),centerY=False)
        pygame.draw.rect(screen,(0,0,0),(1290,195,610,770),5,10)
        if len(self.pastRuns) > 0:
            self.vertScroll.draw(screen)
        else:
            drawCenterTxt(screen,"No Other Runs",65,(210, 50, 50),(1595,220),centerY=False)
            

    def drawRunInfo(self,screen,gametime):
        raise NotImplementedError("drawRunInfo must be implemented in the child class")

    def draw(self,screen,gametime):
        if self.currentRun in self.pastRuns:
            self.pastRuns.remove(self.currentRun)
        self.selectedRun = None if self.vertScroll.getCard() == None else self.vertScroll.getCard().runObj# gets the selected run
        drawCenterTxt(screen,self.currentRun.name,95,(200,200,200),(740,105),centerY=False)
        self.drawPieChart(screen)
        self.drawVertScroll(screen)
        self.drawRunInfo(screen,gametime)
        self.drawBarGraphs(screen)

class BlitzScreen(BlitzAndGoalScreen):
    def __init__(self,pastRuns:list[BlitzRun],curentRun:BlitzRun) -> None:
        super().__init__(pastRuns,curentRun)
        
    def drawRunInfo(self,screen,gametime):
        infoList = [
            (f"Mode",f"{self.currentRun.gameMode}"),
            (f"Rank",f"{self.currentRun.getRankStr()}"),
            (f"Time Left",f"{self.currentRun.getRemainingTimeStr(gametime)}"),
            (f"Start Date",f"{self.currentRun.getFormattedStartTime()}"),
        ]
        
        modeColors = {['Career','Blitz','Goal'][i]:[(19, 133, 100), (199, 114, 44), (196, 22, 62)][i] for i in range(3)}
        
        rankColor = (200,200,200) if self.currentRun.getRankInt() > 3 else [(255, 215, 0), (192, 192, 192),(205, 127, 50)][self.currentRun.getRankInt()-1]
        timeLeftCol = (0, 150, 136) if self.currentRun.getTimeLeftInt(gametime) > 10 else (255, 69, 0)
        colors = [modeColors[self.currentRun.gameMode],rankColor,timeLeftCol,(200,200,200)]
        pygame.draw.rect(screen,(0,0,0),(195,185,500,370),5,10)
        drawLinedInfo(screen,(200,185),(490,380),infoList,45,colors=colors)
    
class GoalScreen(BlitzAndGoalScreen):
    def __init__(self,pastRuns:list[GoalRun],curentRun:GoalRun) -> None:
        super().__init__(pastRuns,curentRun)
    def drawRunInfo(self,screen,gametime):
        infoList = [
            (f"Mode",f"{self.currentRun.gameMode}"),
            (f"Rank",f"{self.currentRun.getRankStr()}"),
            (f"Goal Networth",f"${limit_digits(self.currentRun.getGoalNetworth(),30)}"),
            (f"Start Date",f"{self.currentRun.getFormattedStartTime()}"),
        ]
        
        modeColors = {['Career','Blitz','Goal'][i]:[(19, 133, 100), (199, 114, 44), (196, 22, 62)][i] for i in range(3)}
        
        rankColor = (200,200,200) if self.currentRun.getRankInt() > 3 else [(255, 215, 0), (192, 192, 192),(205, 127, 50)][self.currentRun.getRankInt()-1]
        timeLeftCol = (0, 150, 136) if self.currentRun.getNetworth() > self.currentRun.getGoalNetworth()*.75 else (255, 69, 0)# if the networth is greater than 75% of the goal
        colors = [modeColors[self.currentRun.gameMode],rankColor,timeLeftCol,(200,200,200)]
        pygame.draw.rect(screen,(0,0,0),(195,185,500,370),5,10)
        drawLinedInfo(screen,(200,185),(490,380),infoList,45,colors=colors)

class CareerScreen(BlitzAndGoalScreen):
    def __init__(self,pastRuns:list[CareerRun],curentRun:CareerRun,player,gametime) -> None:
        super().__init__(pastRuns,curentRun)
        self.currentRun : CareerRun = self.currentRun# just for type hinting
        self.player = player
        self.menuSelect : MenuSelection = MenuSelection((200, 105), (375, 95),["Unlock","Compare"],45,colors=[(100,200,100),(200,100,100)])
        self.menuSelect.setSelected(0)
        self.cashGraph = StockVisualizer(gametime,player.cashStock,[player,player.cashStock])
        self.networthGraph = StockVisualizer(gametime,player,[player,player.cashStock])
        self.uStringScroll = VerticalScroll((200,210),(450,750),(430,190))
        # self.cards = [UnlockUpgradeCard(self.uStringScroll,self.currentRun,uString,player) for uString in self.currentRun.getAllUStrings()]
        
        self.orderBox = OrderBox((1390,635),(510,340),gametime)
   

        self.modeSelection : SelectionBar = SelectionBar(horizontal=True,rounded=5)
        # self.progressBar = ProgressBar((675,140),txtsize=60)
        self.menuSpecficContent = {
            "Portfolio" : ["Asset Storage"],
            "Stockbook" : ["Stock Reports"],
            "Options" : ["Pre-Made Options","Custom Options"],
            "Bank" : ["Loan Interest","Max Loan Amount","Tax Rate"]
        }
        self.menuSpecficCards = {
            "Portfolio" : [UnlockUpgradeCard(self.uStringScroll,self.currentRun,uString,player) for uString in self.menuSpecficContent["Portfolio"]],
            "Stockbook" : [UnlockUpgradeCard(self.uStringScroll,self.currentRun,uString,player) for uString in self.menuSpecficContent["Stockbook"]],
            "Options" : [UnlockUpgradeCard(self.uStringScroll,self.currentRun,uString,player) for uString in self.menuSpecficContent["Options"]],
            "Bank" : [UnlockUpgradeCard(self.uStringScroll,self.currentRun,uString,player) for uString in self.menuSpecficContent["Bank"]]
        }
        self.menuColors = {
            "Portfolio" : (239, 131, 84),
            "Stockbook" : (86, 130, 189),
            "Options" : (191, 85, 178),
            "Bank" : (87, 167, 115)
        }

        # self.uStringDesc : dict = {
        #     "Asset Storage" : "Increases the maximum amount of assets you can hold in portfolio.",
        #     "Loan Interest" : "Decreases the interest rate on loans.",
        #     "Max Loan Amount" : f"Increases the max amount of money you can borrow. (% of networth)",
        #     "Tax Rate" : "Decreases the tax rate on all sales and other taxable actions.",
        #     "Stock Reports" : "Allows you to see the stock reports.",
        #     "Pre-Made Options" : "Allows you to trade options with pre-made options.",
        #     "Custom Options" : "Allows you to trade and create custom made options."}

        self.uStringDesc : dict = {
            "Asset Storage" : "Increases the maximum amount of assets you can hold in your portfolio. Each level allows you to diversify your investments further by expanding your storage capacity, letting you hold more unique stocks.",
            "Loan Interest" : "Decreases the interest rate charged on all loans. Lower rates mean smaller monthly payments and more capital available for investing, making loans a more viable tool for expanding your trading capabilities.",
            "Max Loan Amount" : "Increases the maximum amount of money you can borrow as a percentage of your total networth. Higher levels allow for larger loans, providing more leverage for when major trading opportunities arise.",
            "Tax Rate" : "Decreases the tax rate applied to all sales and other taxable actions. Each level reduces the percentage taken from your profits, allowing you to keep more of your earnings from successful trades.",
            "Stock Reports" : "Enables access to detailed stock analysis reports and market insights. These reports provide valuable information about stock performance, trends, and potential market movements to help inform your trading decisions.",
            "Pre-Made Options" : "Unlocks the ability to trade pre-configured options contracts. This feature opens up new strategic possibilities through put and call options, allowing you to profit from both rising and falling markets.",
            "Custom Options" : "Enables the creation and trading of custom-designed options contracts. This advanced feature gives you complete control over strike prices, expiration dates, and contract terms for maximum strategic flexibility."
        }
        

    def drawCompare(self,screen,gametime):
        """Couldn't use the super draw b/c of current name being drawn elsewhere"""
        if self.currentRun in self.pastRuns:
            self.pastRuns.remove(self.currentRun)
        self.selectedRun = None if self.vertScroll.getCard() == None else self.vertScroll.getCard().runObj# gets the selected run
        drawCenterTxt(screen,self.currentRun.name,85,(200,200,200),(932,110),centerY=False)
        self.drawPieChart(screen)
        self.drawVertScroll(screen)
        self.drawRunInfo(screen,gametime)
        self.drawBarGraphs(screen)

    def drawSelectedUstring(self,screen,mode):
        if self.uStringScroll.getCard() == None:
            self.uStringScroll.setCard(obj=self.menuSpecficCards[mode][0])# sets the card to the first card if there is no card selected

        currentCard = self.uStringScroll.getCard()
        uString = currentCard.uString

        # pygame.draw.rect(screen,(0,0,0),(750,210,700,370),5,10)# box for the explanation 
        pygame.draw.rect(screen,(0,0,0),(655,350,730,280),5,10)# box for the explanation

        for i,txt in enumerate(separate_strings(self.uStringDesc.get(uString,"No Description"),5)):# Draws the description of the unlock/upgrade
            drawCenterTxt(screen,txt,46,(200,200,200),(1020,375+i*46),centerY=False)

        drawCenterTxt(screen,uString,130,self.menuColors[mode],(1020,245),centerY=False)# draws the name of the unlock/upgrade
        
        requiredVal = self.currentRun.getNextCost(uString)
        # costTxt = "Maxed" if cost == None else f"${limit_digits(cost,30,True)}"
        
        cashNet = self.currentRun.getNetOrCash(uString)
        deficit = max(0,requiredVal-self.player.cash) if cashNet == "Cash" else max(0,requiredVal-self.currentRun.getNetworth())
        # drawBoxedTextWH(screen,(775,345),(675,85),f"Cost :   ${limit_digits(cost,30,True)}",55,(200,200,200))
        # drawBoxedTextWH(screen,(775,440),(675,85),f"Cash Needed :   ${limit_digits(neededCash,30,True)}",55,(200,200,200))
        # make the color a gradient between a dark red and a dark green depeneding on how far away the needed cash is from zero (zero is dark green and over 100k is dark red)
        # def get_gradient_color(deficit: float) -> tuple:
        #     """
        #     Returns RGB color tuple that gradients from dark green (0) to dark red (100k+)
        #     """
        #     maxGreen = (0, 255, 0)  # RGB for dark green
        #     maxRed = (255, 0, 0)    # RGB for dark red
        #     maxDeficit = 100_000        # Maximum cash threshold
            
        #     # Calculate percentage (0.0 to 1.0)
           
            
        #     # Interpolate between colors
        #     if deficit > maxDeficit/2:# red
        #         percent = min(deficit/maxDeficit, 1.0)
        #         return (max(120,maxRed[0]*percent),0,0)
        #     else:# green
        #         percent = min((50_000-deficit)/(maxDeficit/2), 1.0)
        #         return (0,max(120,maxGreen[1]*percent),0)

        # Usage example:

        # color = get_gradient_color(50000)  # Returns color halfway between dark green and dark red
        # pygame.draw.rect(screen,(0,0,0),(775,345,675,85),5,10)# box below stock graph for lineddata
        requirestxt = "Cost" if cashNet == "Cash" else "Networth Required"
        # drawCenterTxt(screen,f"{requirestxt}",55,(200,200,200),(655,645),centerX=False,centerY=False)
        # drawCenterTxt(screen,f"${limit_digits(requiredVal,30,True)}",55,(200,200,200),(1380,645),centerX=False,centerY=False,fullX=True)

        # drawCenterTxt(screen,f"{self.currentRun.getNextGrantStr(uString)}",55,(200,200,200),(655,715),centerX=False,centerY=False)
        infolist = [(f"{requirestxt}",f"${limit_digits(requiredVal,30,True)}"),(f"Current Lvl",self.currentRun.getCurrValStr(uString)),(f"Grants",f"{self.currentRun.getNextGrantStr(uString)}")]
        drawLinedInfo(screen,(650,640),(730,330),infolist,55,middleData=["-","-","-"],color=(170,170,170),border=5)


        # drawLinedInfo(screen,(775,345),(675,235),[(f"{cashNet} Needed",f"${limit_digits(requiredVal,30,True)}"),(f"Deficit",f"${limit_digits(deficit,30,True)}")],55,colors=[(200,200,200),get_gradient_color(deficit)],border=5)

        # Used stuff from 
        level = "Enabled";buyTxt = f"Purchasing Unlock" # if the uString is an unlock
        if uString in self.currentRun.upgrades:# if the uString is an upgrade
            level = f"Level {self.currentRun.upgrades[uString]+2}"; buyTxt = f"Buying Upgrade"


        # drawBoxedTextWH(screen,(200,595),(565,85),f"Current :   {self.currentRun.getCurrValStr(uString)}",55,(200,200,200))
        # drawBoxedTextWH(screen,(250,685),(465,140),f"{self.currentRun.getNextGrantStr(uString)}",65,(200,200,200))
        # drawBoxedTextWH(screen,(250,830),(465,140),f"{level}",65,(200,200,200))


        # pygame.draw.rect(screen,(0,0,0),(200,595,675,85),5,10)# box below stock graph for lineddata
        # drawLinedInfo(screen,(200,595),(560,355),[("Current",self.currentRun.getCurrValStr(uString)),("Grants",f"{self.currentRun.getNextGrantStr(uString)}"),("Next Lvl",level)],55,color=(200,200,200),border=7)



        if self.currentRun.getNetOrCash(uString) == "Networth":
            self.networthGraph.drawFull(screen,(1390,220),(510,410),uString,True,"")
            # self.progressBar.setProgress((deficit/requiredVal)*100) 
            # self.progressBar.drawBar(screen,(775,830))
            
            # infolist = [("Requires",costTxt),("Current",self.currentRun.getCurrValStr(uString)),("Grants",f"{self.currentRun.getNextGrantStr(uString)}")]
        else:
            self.cashGraph.drawFull(screen,(1390,220),(510,410),uString,True,"")

            self.orderBox.loadData(str(buyTxt),f"${limit_digits(requiredVal,24,True)}",[(uString,level,"")])
            result = self.orderBox.draw(screen)
            if result:
                self.player.purchaseCareerUpgrade(uString,self.currentRun)
                for card in self.menuSpecficCards[mode]:
                    card.updateSurf()


    def drawUnlock(self,screen):

        # menuNames = ["Portfolio","Options","Bank","Stockbook"]

        # for menu in menuNames:
        self.modeSelection.draw(screen,["Portfolio","Stockbook","Options","Bank"],(585,105),(1300,95),colors=list(self.menuColors.values()),txtsize=55)

        mode = self.modeSelection.getSelected()

        self.uStringScroll.loadCards(self.menuSpecficCards[mode])
        self.uStringScroll.draw(screen)

        self.drawSelectedUstring(screen,mode)

        # self.uStringScroll.draw(screen)
        # if self.uStringScroll.getCard() == None:
        #     # drawCenterTxt(screen,"No Unlock Selected",65,(210, 50, 50),(1015,260),centerY=False)
        #     pygame.draw.rect(screen,(0,0,0),(200,210,1200,275),5,10)# box for the explanation 
        #     txt = "There are Unlocks and Upgrades on the right. Unlocks allow you to access new parts of the game, and upgrades enhance your experience. Some unlocks/upgrades are based on networth and will be automatically unlocked, but others must be purchased with cash."
        #     for i,txt in enumerate(separate_strings(txt,4)):
        #         drawCenterTxt(screen,txt,55,(200,200,200),(800,220+i*50),centerY=False)
                
        #     drawCenterTxt(screen,"Select an unlock/upgrade to see more information",65,(210, 50, 50),(800,500),centerY=False)

        #     self.networthGraph.drawFull(screen,(200,560),(590,400),"Networth Graph",True,"")
        #     self.cashGraph.drawFull(screen,(810,560),(590,400),"Cash Graph",True,"")

        #     # pygame.draw.rect(screen,(0,0,0),(195,185,500,370),5,10)
        # else:
        #     self.drawSelectedUstring(screen)
            

            

            
        

    def draw(self, screen, gametime):
        self.menuSelect.draw(screen)
        if self.menuSelect.getSelected() == "Unlock":
            self.drawUnlock(screen)
        else:
            self.drawCompare(screen,gametime)
        
    def drawRunInfo(self,screen,gametime):
        infoList = [
            (f"Mode",f"{self.currentRun.gameMode}"),
            (f"Rank",f"{self.currentRun.getRankStr()}"),
            # (f"Networth Unlock",f"{self.currentRun.nextUnlock("Networth")}"),
            # (f"Paid for Unlock",f"{self.currentRun.nextUnlock("Paid")}"),
            (f"Start Date",f"{self.currentRun.getFormattedStartTime()}"),
        ]
        
        modeColors = {['Career','Blitz','Goal'][i]:[(19, 133, 100), (199, 114, 44), (196, 22, 62)][i] for i in range(3)}
        
        rankColor = (200,200,200) if self.currentRun.getRankInt() > 3 else [(255, 215, 0), (192, 192, 192),(205, 127, 50)][self.currentRun.getRankInt()-1]
        # colors = [modeColors[self.currentRun.gameMode],rankColor,(0, 170, 170),(0, 170, 170),(200,200,200)]
        colors = [modeColors[self.currentRun.gameMode],rankColor,(200,200,200)]
        pygame.draw.rect(screen,(0,0,0),(195,205,500,350),5,10)
        drawLinedInfo(screen,(200,205),(490,360),infoList,45,colors=colors)
