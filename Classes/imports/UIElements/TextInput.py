import pygame
import time
from Defs import *

class TextInput:
    def __init__(self, initial_text="", max_length=50, font_size=45, text_color=(255, 255, 255), 
                 cursor_color=(255, 255, 255), background_color=(40, 40, 40), border_color=(0, 0, 0),
                 border_width=5, border_radius=10, padding=10):
        """
        Advanced text input with key holding support, cursor positioning, and modern features
        
        Args:
            initial_text: Starting text
            max_length: Maximum number of characters
            font_size: Size of the font
            text_color: Color of the text
            cursor_color: Color of the cursor
            background_color: Background color of the input box
            border_color: Border color
            border_width: Width of the border
            border_radius: Radius for rounded corners
            padding: Internal padding
        """
        self.text = initial_text
        self.max_length = max_length
        self.font_size = font_size
        self.text_color = text_color
        self.cursor_color = cursor_color
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.padding = padding
        
        # Cursor management
        self.cursor_pos = len(initial_text)  # Position in text where cursor is
        self.cursor_visible = True
        self.cursor_blink_time = 0.5  # Blink every 500ms
        self.last_cursor_toggle = time.time()
        
        # Key holding management
        self.keys_pressed = set()
        self.key_repeat_times = {}
        self.key_repeat_delay = 0.5  # Initial delay before repeating (500ms)
        self.key_repeat_interval = 0.05  # Interval between repeats (50ms)
        self.last_key_times = {}
        
        # Selection management (for future enhancement)
        self.selection_start = None
        self.selection_end = None
        
        # Focus management
        self.focused = False
        
        # Valid characters (can be customized)
        self.allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?-_()[]{}:;"\'/')
        
    def handle_event(self, event):
        """Handle pygame events for text input"""
        if event.type == pygame.KEYDOWN:
            self.keys_pressed.add(event.key)
            self.key_repeat_times[event.key] = time.time()
            self.last_key_times[event.key] = time.time()
            self._process_keydown(event)
            
        elif event.type == pygame.KEYUP:
            if event.key in self.keys_pressed:
                self.keys_pressed.remove(event.key)
            if event.key in self.key_repeat_times:
                del self.key_repeat_times[event.key]
            if event.key in self.last_key_times:
                del self.last_key_times[event.key]
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mouse clicks for cursor positioning and focus
            pass  # Will be implemented in draw method based on rect collision
            
    def _process_keydown(self, event):
        """Process individual key press"""
        current_time = time.time()
        
        # Reset cursor blink when typing
        self.cursor_visible = True
        self.last_cursor_toggle = current_time
        
        if event.key == pygame.K_BACKSPACE:
            self._delete_char()
        elif event.key == pygame.K_DELETE:
            self._delete_char_forward()
        elif event.key == pygame.K_LEFT:
            self._move_cursor_left()
        elif event.key == pygame.K_RIGHT:
            self._move_cursor_right()
        elif event.key == pygame.K_HOME:
            self.cursor_pos = 0
        elif event.key == pygame.K_END:
            self.cursor_pos = len(self.text)
        elif event.unicode and event.unicode in self.allowed_chars and len(self.text) < self.max_length:
            self._insert_char(event.unicode)
            
    def _delete_char(self):
        """Delete character before cursor"""
        if self.cursor_pos > 0:
            self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
            self.cursor_pos -= 1
            
    def _delete_char_forward(self):
        """Delete character after cursor"""
        if self.cursor_pos < len(self.text):
            self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
            
    def _move_cursor_left(self):
        """Move cursor left"""
        if self.cursor_pos > 0:
            self.cursor_pos -= 1
            
    def _move_cursor_right(self):
        """Move cursor right"""
        if self.cursor_pos < len(self.text):
            self.cursor_pos += 1
            
    def _insert_char(self, char):
        """Insert character at cursor position"""
        self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
        self.cursor_pos += 1
        
    def update(self):
        """Update key holding and cursor blinking - call this every frame"""
        current_time = time.time()
        
        # Handle key holding/repeating
        for key in list(self.keys_pressed):
            if key in self.key_repeat_times:
                time_held = current_time - self.key_repeat_times[key]
                if time_held > self.key_repeat_delay:
                    # Check if enough time has passed for next repeat
                    if current_time - self.last_key_times[key] > self.key_repeat_interval:
                        # Create a fake event for the repeated key
                        fake_event = pygame.event.Event(pygame.KEYDOWN, key=key, unicode='')
                        
                        # Handle special keys
                        if key == pygame.K_BACKSPACE:
                            fake_event.unicode = '\b'
                        elif key == pygame.K_DELETE:
                            fake_event.unicode = '\x7f'
                        
                        self._process_keydown(fake_event)
                        self.last_key_times[key] = current_time
        
        # Handle cursor blinking
        if current_time - self.last_cursor_toggle > self.cursor_blink_time:
            self.cursor_visible = not self.cursor_visible
            self.last_cursor_toggle = current_time
            
    def handle_mouse_click(self, mouse_pos, rect):
        """Handle mouse click for cursor positioning and focus"""
        if rect.collidepoint(mouse_pos):
            self.focused = True
            # Calculate cursor position based on mouse click
            relative_x = mouse_pos[0] - rect.x - self.padding
            
            if not self.text:
                self.cursor_pos = 0
                return
                
            # Find the closest character position to the mouse click
            best_pos = 0
            best_distance = float('inf')
            
            for i in range(len(self.text) + 1):
                text_width = s_render(self.text[:i], self.font_size, self.text_color).get_width() if i > 0 else 0
                distance = abs(text_width - relative_x)
                if distance < best_distance:
                    best_distance = distance
                    best_pos = i
                    
            self.cursor_pos = best_pos
            self.cursor_visible = True
            self.last_cursor_toggle = time.time()
        else:
            self.focused = False
            
    def get_text(self):
        """Get the current text"""
        return self.text
        
    def set_text(self, text):
        """Set the text content"""
        self.text = text[:self.max_length]  # Truncate if too long
        self.cursor_pos = min(self.cursor_pos, len(self.text))
        
    def clear(self):
        """Clear all text"""
        self.text = ""
        self.cursor_pos = 0
        
    def draw(self, screen, rect):
        """
        Draw the text input box
        
        Args:
            screen: pygame surface to draw on
            rect: pygame.Rect defining position and size
        """
        # Handle mouse clicks
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            mouse_pos = pygame.mouse.get_pos()
            if hasattr(self, '_last_click_handled'):
                if time.time() - self._last_click_handled > 0.1:  # Prevent multiple clicks
                    self.handle_mouse_click(mouse_pos, rect)
                    self._last_click_handled = time.time()
            else:
                self.handle_mouse_click(mouse_pos, rect)
                self._last_click_handled = time.time()
        
        # Draw background
        if self.background_color:
            pygame.draw.rect(screen, self.background_color, rect, border_radius=self.border_radius)
        
        # Draw border (different color if focused)
        border_color = self.border_color
        if self.focused:
            border_color = tuple(min(255, c + 50) for c in self.border_color)  # Brighten border when focused
            
        pygame.draw.rect(screen, border_color, rect, self.border_width, self.border_radius)
        
        # Calculate text position
        text_rect = pygame.Rect(
            rect.x + self.padding,
            rect.y + self.padding,
            rect.width - 2 * self.padding,
            rect.height - 2 * self.padding
        )
        
        # Draw text
        if self.text:
            text_surface = s_render(self.text, self.font_size, self.text_color)
            
            # Center text vertically
            text_y = text_rect.y + (text_rect.height - text_surface.get_height()) // 2
            screen.blit(text_surface, (text_rect.x, text_y))
            
            # Draw cursor if focused and visible
            if self.focused and self.cursor_visible:
                cursor_text = self.text[:self.cursor_pos]
                cursor_width = s_render(cursor_text, self.font_size, self.text_color).get_width() if cursor_text else 0
                cursor_x = text_rect.x + cursor_width
                cursor_y = text_y
                cursor_height = text_surface.get_height()
                
                pygame.draw.line(screen, self.cursor_color, 
                               (cursor_x, cursor_y), 
                               (cursor_x, cursor_y + cursor_height), 2)
        else:
            # Draw cursor at start if focused and no text
            if self.focused and self.cursor_visible:
                cursor_x = text_rect.x
                cursor_y = text_rect.y + (text_rect.height - self.font_size) // 2
                cursor_height = self.font_size
                
                pygame.draw.line(screen, self.cursor_color,
                               (cursor_x, cursor_y),
                               (cursor_x, cursor_y + cursor_height), 2)
