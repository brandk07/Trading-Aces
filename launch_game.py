#!/usr/bin/env python3
"""
Trading Aces - Simple launcher with instant startup and mouse scaling
"""
import sys
import time

def main():
    """Launch Trading Aces with instant startup and scaling"""
    
    print("Launching Trading Aces with resolution scaling...")
    
    # Test asset system first
    try:
        from Defs import find_game_root, get_asset_path
        game_root = find_game_root()
        print(f"Game root found: {game_root}")
        
        # Verify critical assets exist
        critical_assets = [
            get_asset_path('back1.jpeg'),
            get_asset_path('Fonts', 'antonio', 'Antonio-Regular.ttf'),
        ]
        
        for asset in critical_assets:
            if not os.path.exists(asset):
                print(f"Warning: Missing asset: {asset}")
        
    except Exception as e:
        print(f"Asset system warning: {e}")
    
    # Get primary display info before showing startup
    import os
    if sys.platform == "win32":
        import ctypes
        
        # Get primary monitor info using multiple methods
        user32 = ctypes.windll.user32
        
        # Method 1: Basic screen metrics (may be scaled)
        basic_width = user32.GetSystemMetrics(0)  # SM_CXSCREEN
        basic_height = user32.GetSystemMetrics(1)  # SM_CYSCREEN
        
        # Method 2: Get actual native resolution (unscaled)
        try:
            # Get the primary monitor handle
            hdc = user32.GetDC(0)
            
            # Get native resolution (ignoring Windows scaling)
            native_width = ctypes.windll.gdi32.GetDeviceCaps(hdc, 118)  # HORZRES
            native_height = ctypes.windll.gdi32.GetDeviceCaps(hdc, 117)  # VERTRES
            
            # Get actual physical resolution
            physical_width = ctypes.windll.gdi32.GetDeviceCaps(hdc, 110)  # DESKTOPHORZRES
            physical_height = ctypes.windll.gdi32.GetDeviceCaps(hdc, 111)  # DESKTOPVERTRES
            
            user32.ReleaseDC(0, hdc)
            
            print(f"Basic resolution (scaled): {basic_width}x{basic_height}")
            print(f"Native resolution: {native_width}x{native_height}")
            print(f"Physical resolution: {physical_width}x{physical_height}")
            
            # Use the highest resolution available
            if physical_width > 0 and physical_height > 0:
                primary_width = physical_width
                primary_height = physical_height
                print(f"Using physical resolution: {primary_width}x{primary_height}")
            elif native_width > basic_width or native_height > basic_height:
                primary_width = native_width
                primary_height = native_height
                print(f"Using native resolution: {primary_width}x{primary_height}")
            else:
                primary_width = basic_width
                primary_height = basic_height
                print(f"Using basic resolution: {primary_width}x{primary_height}")
                
        except Exception as e:
            print(f"Error getting native resolution: {e}")
            primary_width = basic_width
            primary_height = basic_height
            print(f"Falling back to basic resolution: {primary_width}x{primary_height}")
        
        # Set window position to primary monitor
        os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
        os.environ['SDL_VIDEO_CENTERED'] = '0'
        
        
        print(f"Final primary display resolution: {primary_width}x{primary_height}")
        
    else:
        # For non-Windows systems, use default behavior
        primary_width = 1920
        primary_height = 1080
        print("Non-Windows system detected, using default resolution")
    

    
    # Show instant startup screen immediately
    from StartupSequence.instant_startup import show_instant_startup, update_instant_startup, close_instant_startup
    
    startup_root = show_instant_startup()
    
    try:
        # Update progress
        if startup_root:
            update_instant_startup("Loading game engine...", 25)
            time.sleep(0.2)
        
        # Import resolution manager and mouse scaling
        if startup_root:
            update_instant_startup("Setting up resolution scaling...", 50)
            time.sleep(0.1)
        
        # Set environment variables for primary display
        if sys.platform == "win32":
            os.environ['TRADING_ACES_PRIMARY_WIDTH'] = str(primary_width)
            os.environ['TRADING_ACES_PRIMARY_HEIGHT'] = str(primary_height)
        
        # Import the fast main
        from StartupSequence.fast_main import main as fast_main
        
        # Close instant startup
        close_instant_startup()
        
        print("Resolution scaling and mouse coordinate translation enabled!")
        print("The game will now scale to your monitor resolution automatically.")
        
        # Run the game
        fast_main()
        
    except Exception as e:
        print(f"Error launching game: {e}")
        import traceback
        traceback.print_exc()
        
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
