#!/usr/bin/env python3
"""
Trading Aces - Stock Market Trading Simulator
Fast startup entry point with instant visual feedback
"""
import sys
import time

def main():
    """Main entry point with instant startup feedback"""
    
    # Step 0: Show INSTANT feedback (before any heavy imports)
    print("Starting Trading Aces...")
    
    # Show instant visual feedback window
    from instant_startup import show_instant_startup, update_instant_startup, close_instant_startup
    
    startup_root = show_instant_startup()
    
    if startup_root:
        # Give user immediate feedback
        update_instant_startup("Initializing game engine...", 10)
        time.sleep(0.1)  # Brief pause to ensure window is visible
    
    try:
        # Step 1: Import pygame and basic dependencies (the slow part)
        update_instant_startup("Loading Pygame...", 20)
        
        # Import Defs which contains pygame initialization
        start_time = time.time()
        import Defs
        import pygame
        pygame_time = time.time() - start_time
        print(f"Pygame initialization took: {pygame_time:.2f}s")
        
        # Step 2: Load game classes
        update_instant_startup("Loading game classes...", 40)
        
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
        
        # Step 3: Setup display and DPI awareness
        update_instant_startup("Setting up display...", 60)
        
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
        
        # Step 4: Initialize game constants
        update_instant_startup("Loading game data...", 75)
        
        # Game constants
        GAMESPEED = 250
        FASTFORWARDSPEED = 1000
        CLICK_COOLDOWN = 0.15
        last_click_time = time.time()
        
        # Step 5: Create main display with auto-scaling
        update_instant_startup("Creating game window...", 85)
        
        # Get primary monitor resolution from environment or detect it
        import os
        if sys.platform == "win32":
            # Use primary monitor resolution passed from launcher
            primary_width = int(os.environ.get('TRADING_ACES_PRIMARY_WIDTH', '1920'))
            primary_height = int(os.environ.get('TRADING_ACES_PRIMARY_HEIGHT', '1080'))
            
            # Ensure we're on the primary monitor
            import ctypes
            user32 = ctypes.windll.user32
            
            # Set window position to primary monitor (0,0)
            os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
            
            monitor_width, monitor_height = primary_width, primary_height
            print(f"Using primary display: {monitor_width}x{monitor_height}")
        else:
            # Fallback for non-Windows systems
            monitor_width, monitor_height = pygame.display.Info().current_w, pygame.display.Info().current_h
            print(f"Using detected display: {monitor_width}x{monitor_height}")
        
        # Create fullscreen display on primary monitor
        main_screen = pygame.display.set_mode((monitor_width, monitor_height), pygame.FULLSCREEN)
        pygame.display.set_caption("Trading Aces")
        
        # Setup automatic resolution scaling
        from Defs import resolution_manager
        game_size = resolution_manager.setup(monitor_width, monitor_height)
        
        # Step 6: Final initialization
        update_instant_startup("Finalizing setup...", 95)
        
        # Initialize game objects
        clock = pygame.time.Clock()
        
        # Step 7: Ready!
        update_instant_startup("Ready to trade!", 100)
        
        # Small delay to show completion
        time.sleep(1.5)
        
        # Close the instant startup screen
        close_instant_startup()
        
        # Step 8: Start the main game
        print("Starting main game loop...")
        
        # Import and run the original main game logic
        from Main import run_main_game
        from Defs import mouseButton
        run_main_game(main_screen, clock, mouseButton=mouseButton)

    except Exception as e:
        print(f"Error during game initialization: {e}")
        import traceback
        traceback.print_exc()
        
        # Update instant startup with error
        if startup_root:
            try:
                update_instant_startup(f"Error: {str(e)}", 0)
                time.sleep(3)
                close_instant_startup()
            except:
                pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()
