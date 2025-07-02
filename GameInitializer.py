import pygame
import sys
import time
from Defs import *
from Classes.BigClasses.Stock import Stock
from Classes.Menus.HomeScreen import HomeScreen
from Classes.imports.Gametime import GameTime
from Classes.BigClasses.Player import Player
from Classes.Menus.StockScreen import StockScreen
from Classes.Menus.Portfolio import Portfolio
from collections import deque
from Classes.imports.IndexFunds import TotalMarket,IndexFund
import timeit
from Classes.imports.OrderScreen import OrderScreen
from Classes.imports.Transactions import Transactions
from Classes.Menus.StockBook import Stockbook
from Classes.Menus.OptionScreens.OptionMenu import Optiontrade
from Classes.Menus.BankMenu import BankMenu
from Classes.Menus.GameModeMenu import GameModeMenu,GameRun,RunManager
from Classes.Menus.startMenus.StartMain import StartMain
from Classes.Menus.Menu import ScreenManager


def initialize_game_with_progress(currentRun, pastRuns, progress_callback=None):
    """
    Initialize a new game with progress callbacks for the loading animation.
    
    Args:
        currentRun: The game run object
        pastRuns: Dictionary of past game runs
        progress_callback: Function to call with (progress, message) for updates
    
    Returns:
        Tuple of initialized game objects
    """
    
    if progress_callback:
        progress_callback(0.1, "Setting up game time...")
    
    gametime = GameTime(DEFAULTSTARTDATE.strftime(DFORMAT), 250)  # GAMESPEED
    setGameTime(gametime, currentRun.getFileDir())

    if progress_callback:
        progress_callback(0.15, "Initializing stock data...")
    
    stocknames = STOCKNAMES
    stockVolatilities = [i*(2 if currentRun.gameMode == 'Blitz' else 1) for i in [8.03, 7.42, 6.13, 5.58, 4.74, 5.13, 7.8, 4.2, 3.8]]
    stockcolors = [(0, 102, 204),(255, 0, 0),(0, 128, 0),(255, 165, 0),(255, 215, 0),(147,112,219),(46, 139, 87),(255, 69, 0),(0, 191, 255),(128, 0, 128),(12, 89, 27)]

    if progress_callback:
        progress_callback(0.2, "Creating player and transactions...")
    
    transact = Transactions(currentRun.getFileDir())
    player = Player(stocknames, stockcolors[-1], transact, gametime, currentRun)
    
    if progress_callback:
        progress_callback(0.25, "Setting up stocks...")
    
    stockdict = {name:Stock(name,stockcolors[i],gametime,stockVolatilities[i],currentRun,player) for i,name in enumerate(stocknames)}
    stocklist = [stockdict[name] for name in stocknames]
    
    if progress_callback:
        progress_callback(0.3, "Creating index funds...")
    
    indexfundColors = [(217, 83, 149),(64, 192, 128),(138, 101, 235)]
    indexFunds = [IndexFund(gametime,name,stockcolors[i],stocklist[i*3:i*3+3],currentRun,player) for i,name in enumerate(["TDIF","IEIF", "FHMF"])]
    tmarket = TotalMarket(gametime,stocklist,currentRun,player)
    indexFunds.append(tmarket)
    indexFundDict = {fund.name: fund for fund in indexFunds}

    if progress_callback:
        progress_callback(0.35, "Setting up trading options...")
    
    optiontrade = Optiontrade(stocklist,gametime,player,currentRun)
    Getfromfile(stockdict,indexFundDict,player,gametime,currentRun.getFileDir(),optiontrade)

    if progress_callback:
        progress_callback(0.4, "Creating user interface...")
    
    stockScreen = StockScreen(stocklist,gametime)
    orderScreen = OrderScreen()
    homeScreen = HomeScreen(stocklist,gametime,tmarket,player)
    stockbook = Stockbook(stocklist,gametime,orderScreen,currentRun)
    portfolio = Portfolio(stocklist,player,gametime,tmarket,currentRun)
    bank = BankMenu(stocklist,gametime,player,transact,tmarket,indexFunds,currentRun)

    if progress_callback:
        progress_callback(0.45, "Setting up game menus...")
    
    gameModeMenu = GameModeMenu(stocklist,player,pastRuns,currentRun,gametime)
    menuDict = {'Portfolio':portfolio,'Stockbook':stockbook,'Options':optiontrade,'Bank':bank,'Mode':gameModeMenu}
    screenManager = ScreenManager(menuDict,homeScreen,stockScreen,gametime,currentRun)
    player.screenManager = screenManager

    if progress_callback:
        progress_callback(0.5, "Filling stock graph data...")
    
    # Fill stock graphs with progress tracking
    timer = timeit.default_timer()
    if not all([all([len(graph) == POINTSPERGRAPH for graph in stock.graphs.values()]) for stock in stocklist]):
        total_stocks = len(stocklist)
        for i, stock in enumerate(stocklist):
            # Create a wrapper progress callback that accounts for the stock index
            def stock_progress_callback(stock_progress, message):
                # Calculate overall progress: 50% base + (stock_index/total * 40%) + (stock_progress * 40%/total)
                overall_progress = 0.5 + (i / total_stocks) * 0.4 + (stock_progress * 0.4 / total_stocks)
                if progress_callback:
                    progress_callback(overall_progress, message)
            
            stock.fill_graphs(stock_progress_callback)
        
        if progress_callback:
            progress_callback(0.9, "Saving game data...")
        
        saveGame(stocklist,player,currentRun.getFileDir(),gametime,transact,currentRun,optiontrade)
        print('time to fill graphs',timeit.default_timer()-timer)

    if progress_callback:
        progress_callback(0.95, "Finalizing index funds...")
    
    for indexfund in indexFunds:
        indexfund.fill_graphs()

    if progress_callback:
        progress_callback(1.0, "Game ready!")
    
    return (stocklist, player, gametime, transact, screenManager, 
            stockScreen, homeScreen, stockbook, portfolio, bank, 
            gameModeMenu, indexFunds, tmarket, optiontrade)
