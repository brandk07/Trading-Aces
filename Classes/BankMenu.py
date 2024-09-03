import pygame
from Defs import *
from pygame import gfxdraw
from Classes.imports.Menu import Menu
import numpy as np
from Classes.imports.Bar import SliderBar
from Classes.StockVisualizer import StockVisualizer
from Classes.imports.Latterscroll import PortfolioLatter,LatterScroll
from Classes.Stock import Stock
from Classes.imports.PieChart import PieChart
from Classes.imports.BarGraph import BarGraph
from Classes.imports.SelectionElements import SelectionBar,MenuSelection
from Classes.imports.PerfChart import PerfChart
from Classes.imports.Numpad import Numpad
from Classes.imports.OrderBox import OrderBox
from Classes.AssetTypes.IndexFunds import IndexFundAsset

import datetime
from Classes.imports.SideScroll import SideScroll,CdCard


class BankMenu(Menu):
    def __init__(self,stocklist,gametime,player,transactions,tmarket,indexFunds:list) -> None:
        self.icon = pygame.image.load(r'Assets\Menu_Icons\bankIcon.jpg').convert_alpha()
        self.icon = pygame.transform.scale(self.icon,(140,100))
        super().__init__(self.icon)
        self.menuSelection = MenuSelection((200,105),(520,100),["Overview","Investments","Loans"],45)
        self.overView = OverView(player,transactions)
        self.investScreen = InvestmentScreen(stocklist.copy(),gametime,player,tmarket,indexFunds.copy())
        self.menudrawn = True

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player,gametime):

        self.menuSelection.draw(screen,mousebuttons)


        match self.menuSelection.getSelected():
            case "Overview":
                self.overView.draw(screen)
            case "Investments":
                self.investScreen.draw(screen,mousebuttons,gametime)
            case "Loans":
                pass


class OverView:
    def __init__(self,player,transactions) -> None:
        self.player = player
        self.transactions = transactions
    def draw(self,screen):
        pass

class InvestmentScreen:
    def __init__(self,stocklist,gametime,player,tmarket,indexFunds) -> None:
        self.player = player
        self.sideScroll = SideScroll((200,235),(1120,365),(315,315))
        bankIcons = {}
        data = {"duration":12,"apr":7.63,"minBalance":16000,"risk":"High (3.82%)"}
        self.assetSelection = MenuSelection((1580,110),(320,105),["CD","Index Funds"],45)
        for file in os.listdir(r"Assets\bankIcons"):
            image = pygame.image.load(r"Assets\bankIcons\{}".format(file)).convert_alpha()
            bankIcons[file.split(".")[0]] = CdCard(image,file.split(".")[0],self.sideScroll,data,(315,315))
        self.sideScroll.loadCards(list(bankIcons.values()))

        self.fundNumpad = Numpad(False)
        self.fundOrderBox = OrderBox((1405,600),(475,365))

        self.indexFunds = indexFunds; self.indexFunds.append(tmarket)
        self.indexGraphs : dict[str:StockVisualizer] = {}
        for indexFund in self.indexFunds:
            self.indexGraphs[indexFund.name] = StockVisualizer(gametime,indexFund,stocklist)
        # self.indexGraphs["Total Market"] = StockVisualizer(gametime,tmarket,stocklist)

        self.fundSelection = SelectionBar(horizontal=False)
        self.fundPerfChart = PerfChart((620,300))
        # self.totalGraph = StockVisualizer(gametime,tmarket,[tmarket,player])
        # self.networthGraph = StockVisualizer(gametime,player,stocklist)
        self.getRealSelc = lambda fakeSelect: list(self.indexGraphs.keys())[["V & V","A & A", "R & R", "Total"].index(fakeSelect)]# Need since the namse in fundSelection are abbreviated
        self.updateCards([])

    def updateCards(self,cardsData:list[dict]):
        """Updates the CDs in the sidescroll element for cd cards it is [{"duration":int(Months),"apr":float,"minBalance":int,"risk":str}]"""
        newData = []
        for _ in self.sideScroll.cards:
            newData.append({"duration":randint(3,36),"apr":randint(200,900)/100,"minBalance":randint(500,25000),"risk":f"{random.choice(["High","Medium","Low"])} (??%)"})
        self.sideScroll.updateCards(newData)

    def draw(self,screen,mousebuttons,gametime):
        
        self.assetSelection.draw(screen,mousebuttons)

        match self.assetSelection.getSelected():
            case "CD":
                self.sideScroll.draw(screen,mousebuttons)

            case "Index Funds":
                self.fundSelection.draw(screen,["V & V","A & A", "R & R", "Total"],(200,210),(100,355),mousebuttons,colors=[f.color for f in self.indexFunds])
                
                if self.fundSelection.getSelected() != None:
                    realName = self.getRealSelc(self.fundSelection.getSelected())
                    fund = [fund for fund in self.indexFunds if fund.name == realName][0]
                    self.indexGraphs[realName].drawFull(screen,(305,215),(620,455),realName,True,"Normal")

                    currentQ = (gametime.time.month-1)//3+1

                    self.fundPerfChart.updateData({f"Q{(i+(currentQ+1)-1)%4+1}":limit_digits(fund.getQuarterReturns((i+(currentQ+1)-1)%4+1,gametime),15) for i in range(4)})
                    self.fundPerfChart.draw(screen,(305,675))# perf chart for the fund

                    self.fundNumpad.draw(screen,(930,600),(460,365),"Shares",mousebuttons,self.player.cash//fund.price)
                    

                    pricePer = limit_digits(fund.getValue(),15)
                    data = [("Value",f"${pricePer}","x")]
                    totalCost = fund.getValue()*self.fundNumpad.getValue()*(1-2/100)

                    self.fundOrderBox.loadData(self.fundNumpad.getNumstr('Option'),f"${limit_digits(totalCost,22)}",data)
                    result = self.fundOrderBox.draw(screen,mousebuttons)

                    if result and self.fundNumpad.getValue() > 0:
                        fundObj = IndexFundAsset(self.player,fund,gametime.time,fund.price,self.fundNumpad.getValue())
                        self.player.buyAsset(fundObj)


        # self.sideScroll.draw(screen,mousebuttons)

        # self.totalGraph.drawFull(screen,(760,610),(550,355),"Total Market Graph",True,"Normal")
        # self.networthGraph.drawFull(screen,(200,610),(550,355),"Networth Graph",True,"Normal")
        # for i,graph in enumerate(self.indexGraphs):
        #     graph.drawFull(screen,(200+(i*570),235),(550,355),f"{i} Graph",True,"Normal")

