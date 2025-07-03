#!/usr/bin/env python3
"""
Quick test to verify mouse scaling fix
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

import pygame

def test_mouse_fix():
    pygame.init()
    
    # Test basic mouse functions
    print("Testing mouse coordinate functions...")
    
    # Import after pygame init
    from Defs import get_mouse_pos, get_raw_mouse_pos, enable_mouse_scaling, disable_mouse_scaling, resolution_manager
    
    # Setup a simple display for testing
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Mouse Fix Test")
    
    # Setup resolution manager
    resolution_manager.setup(800, 600)
    
    print("Testing before enabling scaling...")
    raw_pos = get_raw_mouse_pos()
    scaled_pos = get_mouse_pos()
    print(f"Raw: {raw_pos}, Scaled: {scaled_pos}")
    
    print("Enabling mouse scaling...")
    enable_mouse_scaling()
    
    print("Testing after enabling scaling...")
    try:
        # This should not cause recursion
        pygame_pos = pygame.mouse.get_pos()
        manual_scaled = get_mouse_pos()
        raw_pos = get_raw_mouse_pos()
        
        print(f"pygame.mouse.get_pos(): {pygame_pos}")
        print(f"get_mouse_pos(): {manual_scaled}")
        print(f"get_raw_mouse_pos(): {raw_pos}")
        print("✅ No recursion error!")
        
    except RecursionError:
        print("❌ Recursion error still exists!")
        return False
    
    print("Disabling mouse scaling...")
    disable_mouse_scaling()
    
    print("Test completed successfully!")
    pygame.quit()
    return True

if __name__ == "__main__":
    test_mouse_fix()
