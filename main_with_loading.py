#!/usr/bin/env python3
"""
Trading Aces - Stock Market Trading Simulator
Entry point with loading screen for better user experience
"""
from Defs import *
import sys
import time

def main():
    """Main entry point with loading screen"""
    
    # Step 0: Show immediate loading feedback
    from loading_screen import show_loading_screen, update_loading_step, update_loading_display, finish_loading
    
    screen, loader = show_loading_screen()
    
    try:
        # Step 1: Initialize Pygame (this is the slow part)
        update_loading_step(1, "Initializing Pygame...")
        if screen:
            update_loading_display(screen)
        
        # Import Defs (contains pygame.init() - the slow part)
        start_time = time.time()
        
        pygame_time = time.time() - start_time
        print(f"Pygame initialization took: {pygame_time:.2f}s")
        
        # Step 2: Load game assets and classes
        update_loading_step(2, "Loading game assets...")
        if screen:
            update_loading_display(screen)
        
        from Classes.BigClasses.Stock import Stock
        from Classes.Menus.HomeScreen import HomeScreen
        from Classes.imports.Gametime import GameTime
        from Classes.BigClasses.Player import Player
        from Classes.Menus.StockScreen import StockScreen
        from Classes.Menus.Portfolio import Portfolio
        from collections import deque
        from Classes.imports.IndexFunds import TotalMarket, IndexFund
        import timeit
        from Classes.imports.OrderScreen import OrderScreen
        from Classes.imports.Transactions import Transactions
        from Classes.Menus.StockBook import Stockbook
        from Classes.Menus.OptionScreens.OptionMenu import Optiontrade
        from Classes.Menus.BankMenu import BankMenu
        from Classes.Menus.GameModeMenu import GameModeMenu, GameRun, RunManager
        from Classes.Menus.startMenus.StartMain import StartMain
        from Classes.Menus.Menu import ScreenManager
        
        # Step 3: Set up trading system
        update_loading_step(3, "Setting up trading system...")
        if screen:
            update_loading_display(screen)
        
        # Windows DPI awareness
        if sys.platform == "win32":
            import ctypes
            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except:
                try:
                    ctypes.windll.user32.SetProcessDPIAware()
                except:
                    pass
        
        # Step 4: Load stock data
        update_loading_step(4, "Loading stock data...")
        if screen:
            update_loading_display(screen)
        
        # Game constants
        GAMESPEED = 250
        FASTFORWARDSPEED = 1000
        CLICK_COOLDOWN = 0.15
        last_click_time = time.time()
        
        # Step 5: Prepare user interface
        update_loading_step(5, "Preparing user interface...")
        if screen:
            update_loading_display(screen)
        
        # Set up display
        monitor_width, monitor_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        window_width, window_height = (monitor_width, monitor_height)
        
        # Create the main game window
        main_screen = pygame.display.set_mode((monitor_width, monitor_height), 
                                            pygame.NOFRAME|pygame.HWSURFACE|pygame.SRCALPHA)
        pygame.display.set_caption("Trading Aces")
        main_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        
        # Step 6: Finalizing setup
        update_loading_step(6, "Finalizing setup...")
        if screen:
            update_loading_display(screen)
        
        # Initialize game objects
        clock = pygame.time.Clock()
        
        # Step 7: Ready to trade!
        update_loading_step(7, "Ready to trade!")
        if screen:
            update_loading_display(screen)
        
        # Small delay to show "Ready" message
        time.sleep(0.5)
        
        # Finish loading
        finish_loading()
        
        # Close loading screen if it exists
        if screen:
            time.sleep(0.3)  # Brief pause to show completion
        
        # Step 8: Start the main game
        print("Starting main game loop...")
        
        # Import and run the original main game logic
        from Main import run_main_game
        run_main_game(main_screen, clock)
        
    except Exception as e:
        print(f"Error during game initialization: {e}")
        import traceback
        traceback.print_exc()
        
        if screen:
            # Show error on loading screen
            try:
                font = pygame.font.Font(None, 36)
                error_text = font.render(f"Error: {str(e)}", True, (255, 100, 100))
                error_rect = error_text.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 200))
                screen.blit(error_text, error_rect)
                pygame.display.flip()
                time.sleep(3)
            except:
                pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()
