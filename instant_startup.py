#!/usr/bin/env python3
"""
Instant startup screen using Tkinter - appears immediately before Pygame loads
"""
import tkinter as tk
from tkinter import ttk
import threading
import time
import sys
import os

class InstantStartup:
    def __init__(self):
        self.root = None
        self.progress_var = None
        self.status_var = None
        self.is_running = False
        
    def show(self):
        """Show the instant startup screen"""
        try:
            self.root = tk.Tk()
            self.root.title("Trading Aces")
            
            # Get screen dimensions
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # Window size
            window_width = 500
            window_height = 300
            
            # Center the window
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            self.root.configure(bg='#1a1a2e')
            self.root.resizable(False, False)
            
            # Remove window decorations for a cleaner look
            self.root.overrideredirect(True)
            
            # Create main frame
            main_frame = tk.Frame(self.root, bg='#1a1a2e', padx=20, pady=20)
            main_frame.pack(fill='both', expand=True)
            
            # Title
            title_label = tk.Label(
                main_frame, 
                text="TRADING ACES", 
                font=('Arial', 28, 'bold'),
                fg='#00ff88',
                bg='#1a1a2e'
            )
            title_label.pack(pady=(20, 10))
            
            # Subtitle
            subtitle_label = tk.Label(
                main_frame, 
                text="Stock Market Trading Simulator", 
                font=('Arial', 12),
                fg='#cccccc',
                bg='#1a1a2e'
            )
            subtitle_label.pack(pady=(0, 30))
            
            # Status
            self.status_var = tk.StringVar()
            self.status_var.set("Starting up...")
            status_label = tk.Label(
                main_frame, 
                textvariable=self.status_var, 
                font=('Arial', 11),
                fg='#ffffff',
                bg='#1a1a2e'
            )
            status_label.pack(pady=(0, 15))
            
            # Progress bar
            style = ttk.Style()
            style.theme_use('clam')
            style.configure(
                "Custom.Horizontal.TProgressbar",
                troughcolor='#0f0f23',
                bordercolor='#00ff88',
                background='#00ff88',
                lightcolor='#00ff88',
                darkcolor='#00ff88'
            )
            
            self.progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(
                main_frame,
                variable=self.progress_var,
                maximum=100,
                style="Custom.Horizontal.TProgressbar",
                length=400
            )
            progress_bar.pack(pady=(0, 20))
            
            # Loading dots animation
            self.dots_var = tk.StringVar()
            self.dots_var.set("●○○")
            dots_label = tk.Label(
                main_frame,
                textvariable=self.dots_var,
                font=('Arial', 16),
                fg='#00ff88',
                bg='#1a1a2e'
            )
            dots_label.pack()
            
            # Start animation
            self.is_running = True
            self.animate_dots()
            
            # Make window stay on top
            self.root.attributes('-topmost', True)
            
            # Update once to show immediately
            self.root.update()
            
            return self.root
            
        except Exception as e:
            print(f"Error creating instant startup: {e}")
            return None
    
    def animate_dots(self):
        """Animate the loading dots"""
        if not self.is_running or not self.root:
            return
            
        try:
            dots_cycle = ["●○○", "○●○", "○○●", "○●○"]
            current_time = int(time.time() * 2) % len(dots_cycle)
            self.dots_var.set(dots_cycle[current_time])
            
            # Schedule next update
            self.root.after(250, self.animate_dots)
        except:
            pass
    
    def update_status(self, status, progress=None):
        """Update the status and progress"""
        if not self.root or not self.is_running:
            return
            
        try:
            self.status_var.set(status)
            if progress is not None:
                self.progress_var.set(progress)
            self.root.update()
        except:
            pass
    
    def close(self):
        """Close the startup screen"""
        self.is_running = False
        if self.root:
            try:
                self.root.destroy()
            except:
                pass
            self.root = None

def show_instant_feedback():
    """Legacy function for compatibility"""
    startup = InstantStartup()
    root = startup.show()
    return root, startup, startup

# Global instance
_startup_instance = None

def show_instant_startup():
    """Show the instant startup screen"""
    global _startup_instance
    _startup_instance = InstantStartup()
    return _startup_instance.show()

def update_instant_startup(status, progress=None):
    """Update the instant startup screen"""
    global _startup_instance
    if _startup_instance:
        _startup_instance.update_status(status, progress)

def close_instant_startup():
    """Close the instant startup screen"""
    global _startup_instance
    if _startup_instance:
        _startup_instance.close()
        _startup_instance = None
if __name__ == "__main__":
    # Test the instant startup
    root = show_instant_startup()
    if root:
        import time
        
        for i in range(101):
            update_instant_startup(f"Loading... {i}%", i)
            time.sleep(0.05)
        
        update_instant_startup("Complete!", 100)
        time.sleep(1)
        close_instant_startup()