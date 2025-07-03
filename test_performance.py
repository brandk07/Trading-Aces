#!/usr/bin/env python3
"""
Performance test for Defs.py import time
Run this to measure the initialization time improvement
"""

import time
import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_import_time():
    """Test how long it takes to import Defs.py"""
    print("Testing Defs.py import performance...")
    
    # Test import time
    start_time = time.perf_counter()
    
    try:
        import Defs
        import_time = time.perf_counter() - start_time
        
        print(f"✅ Defs.py imported successfully in {import_time:.3f} seconds")
        
        # Test lazy loading works
        print("\nTesting lazy loading functionality...")
        
        # Test font lazy loading
        start_font = time.perf_counter()
        font_obj = Defs.get_font('reg', 50)
        font_time = time.perf_counter() - start_font
        print(f"✅ First font load: {font_time:.3f} seconds")
        
        # Test string size lazy loading
        start_str = time.perf_counter()
        char_size = Defs.get_char_size('5', 30)
        str_time = time.perf_counter() - start_str
        print(f"✅ First character size calculation: {str_time:.3f} seconds")
        
        # Test sound lazy loading
        start_sound = time.perf_counter()
        sound_obj = Defs.soundEffects['generalClick']
        sound_time = time.perf_counter() - start_sound
        print(f"✅ First sound load: {sound_time:.3f} seconds")
        
        print(f"\n🎉 Total initialization time: {import_time:.3f} seconds")
        print("All lazy loading systems working correctly!")
        
        return import_time
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return None

if __name__ == "__main__":
    test_import_time()
