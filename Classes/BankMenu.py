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
        self.sideScroll = SideScroll((200,210),(1200,450),(375,400))
        bankIcons = {}
        data = {"duration":12,"apr":7.63,"minBalance":16000,"risk":"High (3.82%)"}
        self.assetSelection = MenuSelection((1580,105),(320,100),["CD","Index Funds"],45)
        for file in os.listdir(r"Assets\bankIcons"):
            image = pygame.image.load(r"Assets\bankIcons\{}".format(file)).convert_alpha()
            bankIcons[file.split(".")[0]] = CdCard(image,file.split(".")[0],self.sideScroll,data,(375,400))
        
        self.sideScroll.loadCards(list(bankIcons.values()))

        self.fundNumpad = Numpad(False,maxDecimals=0)
        self.fundOrderBox = OrderBox((1410,670),(475,300))

        self.indexFunds = indexFunds; self.indexFunds.append(tmarket)
        self.indexGraphs : dict[str:StockVisualizer] = {}
        for indexFund in self.indexFunds:
            self.indexGraphs[indexFund.name] = StockVisualizer(gametime,indexFund,stocklist)

        self.fundSelection = SelectionBar(horizontal=False)
        self.fundPerfChart = PerfChart((620,300))
        
        self.getRealSelc = lambda fakeSelect: ['Velocity Ventures','Adaptive Allocation','Reliable Returns',"Total Market"][["V & V","A & A", "R & R", "Total"].index(fakeSelect)]# Need since the fund names are abbreviated
        self.updateCards([])

    def updateCards(self,cardsData:list[dict]):
        """Updates the CDs in the sidescroll element for cd cards it is [{"duration":int(Months),"apr":float,"minBalance":int,"risk":str}]"""
        newData = []
        for _ in self.sideScroll.cards:
            newData.append({"duration":randint(3,36),"apr":randint(200,900)/100,"minBalance":randint(500,25000),"risk":f"{random.choice(["High","Medium","Low"])} (??%)"})
        self.sideScroll.updateCards(newData)
        
    def drawAssetInfo(self,screen,mousebuttons,gametime,assetType):
        if assetType == "CD":
            txt = "A certificate of deposit (CD) is a type of savings account that has a fixed interest rate and fixed date of withdrawal, known as the maturity date. CDs also typically don’t have monthly fees. You agree to keep the full deposit in the account for the term length, and the bank agrees to pay you a fixed interest rate during that time."
            screen.blit(s_render("CD",70,(255,255,255)),(1425,220))

        elif assetType == "Index Funds":
            txt = "An index fund is an investment that tracks the performance of an entire market, rather than a single stock. It accomplishes this by holding a portfolio of multiple companies within the market. This diversification helps to reduce risk and volatility, making index funds a popular choice for long-term investors."
            screen.blit(s_render("Index Funds",60,(255,255,255)),(1425,220))
        txt = separate_strings(txt,7)
        for i,line in enumerate(txt):
            # screen.blit(s_render(line,30,(255,255,255)),(1425,300+(i*40)))
            drawCenterTxt(screen,line,30,(255,255,255),(1647,300+(i*40)))
        


    def drawIndexFundInfo(self,screen,mousebuttons,gametime,fund):
        screen.blit(s_render(self.getRealSelc(fund.name),60,fund.color),(940,220))

    def drawIndexFunds(self,screen,mousebuttons,gametime):

        self.fundSelection.draw(screen,["V & V","A & A", "R & R", "Total"],(200,210),(100,355),mousebuttons,colors=[f.color for f in self.indexFunds])
        

        if self.fundSelection.getSelected() != None:
            # realName = self.getRealSelc(self.fundSelection.getSelected())# get the real name of the fund
            fund = [fund for fund in self.indexFunds if fund.name == self.fundSelection.getSelected()][0]# get the fund object
            self.indexGraphs[self.fundSelection.getSelected()].drawFull(screen,(305,210),(620,450),self.fundSelection.getSelected(),True,"Normal")# draw the graph for the fund

            currentQ = gametime.getCurrentQuarter()# current game quarter

            self.fundPerfChart.updateData({f"Q{(i+(currentQ+1)-1)%4+1}":limit_digits(fund.getQuarterReturns((i+(currentQ+1)-1)%4+1,gametime),15) for i in range(4)})# update the data for the perf chart
            self.fundPerfChart.draw(screen,(305,670))# perf chart for the fund

            self.fundNumpad.draw(screen,(930,670),(475,320),"Shares",mousebuttons,int(self.player.cash/fund.price))# draw the numpad
            pygame.draw.rect(screen,(0,0,0),(930,670,475,300),5,border_radius=10)# draw the numpad box

            pricePer = limit_digits(fund.getValue(),15)# price per share
            data = [("Value",f"${pricePer}","x")]# data for the order box
            totalCost = fund.getValue()*self.fundNumpad.getValue()*(1-2/100)# total cost of the shares

            self.fundOrderBox.loadData(self.fundNumpad.getNumstr('Share'),f"${limit_digits(totalCost,22)}",data)# load the data into the order box
            result = self.fundOrderBox.draw(screen,mousebuttons)# draw the order box

            self.drawIndexFundInfo(screen,mousebuttons,gametime,fund)

            if result and self.fundNumpad.getValue() > 0:# if the order box is clicked and the value is greater than 0
                fundObj = IndexFundAsset(self.player,fund,gametime.time,fund.price,self.fundNumpad.getValue())
                self.player.buyAsset(fundObj)

    def draw(self,screen,mousebuttons,gametime):
        
        self.assetSelection.draw(screen,mousebuttons)

       
        pygame.draw.rect(screen,(0,0,0),(1410,210,475,450),5,border_radius=10)# Describes what an index fund/CD is
        match self.assetSelection.getSelected():
            case "CD":
                self.sideScroll.draw(screen,mousebuttons)
                # (self,screen,coords,mousebuttons,minX,maxX
                self.sideScroll.getCard().draw(screen,(200,670),mousebuttons,customWh=(375,300))# Draw the selected card 

                pygame.draw.rect(screen,(0,0,0),(585,670,375,300),5,border_radius=10)# box for extra cD info

                data = [("Duration",f"{self.sideScroll.getCard().data['duration']} Months"),("APR",f"{round(self.sideScroll.getCard().data['apr'],2)}%"),("Min Balance",f"${limit_digits(self.sideScroll.getCard().data['minBalance'],20,True)}"),("Risk",self.sideScroll.getCard().data['risk'])]
                drawLinedInfo(screen,(585,670),(375,300),data,30,(255,255,255))# draw the extra info for the CD


            case "Index Funds":
                pygame.draw.rect(screen,(0,0,0),(930,210,475,450),5,border_radius=10)# for the indexFund info (deeper in depth for specific fund)
                self.drawIndexFunds(screen,mousebuttons,gametime)

        self.drawAssetInfo(screen,mousebuttons,gametime,self.assetSelection.getSelected())
                


        # self.sideScroll.draw(screen,mousebuttons)

        # self.totalGraph.drawFull(screen,(760,610),(550,355),"Total Market Graph",True,"Normal")
        # self.networthGraph.drawFull(screen,(200,610),(550,355),"Networth Graph",True,"Normal")
        # for i,graph in enumerate(self.indexGraphs):
        #     graph.drawFull(screen,(200+(i*570),235),(550,355),f"{i} Graph",True,"Normal")

