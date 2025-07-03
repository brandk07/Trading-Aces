#!/usr/bin/env python3
"""
Trading Aces - Simple launcher with instant startup and mouse scaling
"""
import sys
import time

def main():
    """Launch Trading Aces with instant startup and scaling"""
    
    print("Launching Trading Aces with resolution scaling...")
    
    # Show instant startup screen immediately
    from instant_startup import show_instant_startup, update_instant_startup, close_instant_startup
    
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
        
        # Import the fast main
        from fast_main import main as fast_main
        
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
