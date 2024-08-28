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
import datetime
from Classes.imports.SideScroll import SideScroll,CdCard


class BankMenu(Menu):
    def __init__(self,stocklist,gametime,player,transactions,tmarket,indexFunds) -> None:
        self.icon = pygame.image.load(r'Assets\Menu_Icons\bankIcon.jpg').convert_alpha()
        self.icon = pygame.transform.scale(self.icon,(140,100))
        super().__init__(self.icon)
        self.menuSelection = MenuSelection((200,105),(520,100),["Overview","Investments","Loans"],45)
        self.overView = OverView(player,transactions)
        self.investScreen = InvestmentScreen(stocklist,gametime,player,tmarket,indexFunds)

    def draw_menu_content(self, screen: pygame.Surface, stocklist: list, mousebuttons: int, player,gametime):

        self.menuSelection.draw(screen,mousebuttons)


        match self.menuSelection.getSelected():
            case "Overview":
                self.overView.draw(screen)
            case "Investments":
                self.investScreen.draw(screen,mousebuttons)
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

        for file in os.listdir(r"Assets\bankIcons"):
            image = pygame.image.load(r"Assets\bankIcons\{}".format(file)).convert_alpha()
            bankIcons[file.split(".")[0]] = CdCard(image,file.split(".")[0],self.sideScroll,data,(315,315))
        self.sideScroll.loadCards(list(bankIcons.values()))
        self.indexFunds = indexFunds
        self.indexGraphs = []
        for indexFund in self.indexFunds:
            self.indexGraphs.append(StockVisualizer(gametime,indexFund,stocklist))

        self.totalGraph = StockVisualizer(gametime,tmarket,[tmarket,player])
        self.networthGraph = StockVisualizer(gametime,player,stocklist)
        self.updateCards([])
    def updateCards(self,cardsData:list[dict]):
        """Updates the CDs in the sidescroll element for cd cards it is [{"duration":int(Months),"apr":float,"minBalance":int,"risk":str}]"""
        newData = []
        for _ in self.sideScroll.cards:
            newData.append({"duration":randint(3,36),"apr":randint(200,900)/100,"minBalance":randint(500,25000),"risk":f"{random.choice(["High","Medium","Low"])} (??%)"})
        self.sideScroll.updateCards(newData)

    def draw(self,screen,mousebuttons):
        
        self.sideScroll.draw(screen,mousebuttons)

        self.totalGraph.drawFull(screen,(760,610),(550,355),"Total Market Graph",True,"Normal")
        self.networthGraph.drawFull(screen,(200,610),(550,355),"Networth Graph",True,"Normal")
        for i,graph in enumerate(self.indexGraphs):
            graph.drawFull(screen,(200+(i*570),235),(550,355),f"{i} Graph",True,"Normal")

