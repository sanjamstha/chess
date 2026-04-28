import pygame as p
import sys
from typing import Optional, Tuple
from database.db import Database
from auth.auth import Auth
from auth.session import Session

class LoginScreen:
    """Pygame-based login and registration screen"""
    
    def __init__(self, width=600, height=750):
        p.init()
        self.width = width
        self.height = height
        self.screen = p.display.set_mode((width, height))
        p.display.set_caption("Chess Game - Login")
        
        # Colors - CONSISTENT emerald green theme
        self.BG_COLOR = (40, 44, 52)           # Dark background
        self.PANEL_COLOR = (50, 54, 62)        # Panel background
        self.INPUT_COLOR = (60, 64, 72)        # Input field
        self.INPUT_ACTIVE = (70, 74, 82)       # Active input field
        self.BUTTON_COLOR = (16, 185, 129)     # #10B981 - Your chosen emerald green
        self.BUTTON_HOVER = (52, 211, 153)     # Lighter emerald
        self.TEXT_COLOR = (255, 255, 255)      # White text
        self.TEXT_GRAY = (158, 158, 158)       # Gray text
        self.ERROR_COLOR = (244, 67, 54)       # Red for errors
        self.SUCCESS_COLOR = (16, 185, 129)    # Same emerald for success
        self.CURSOR_COLOR = (16, 185, 129)     # Emerald cursor
        
        # Fonts
        self.title_font = p.font.SysFont("Arial", 48, bold=True)
        self.font = p.font.SysFont("Arial", 24)
        self.small_font = p.font.SysFont("Arial", 18)
        
        # Input fields
        self.username_input = ""
        self.email_input = ""
        self.password_input = ""
        self.active_field = None  # 'username', 'email', or 'password'
        
        # UI state
        self.mode = "login"  # 'login' or 'register'
        self.message = ""
        self.message_color = self.TEXT_GRAY
        self.show_password = False
        
        # Cursor blink
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_speed = 530  # milliseconds
        
        # Button rectangles (will be set in draw methods)
        self.username_rect = None
        self.email_rect = None
        self.password_rect = None
        self.submit_button_rect = None
        self.switch_button_rect = None
        self.show_password_rect = None
        
        # Database and Auth
        self.db = Database()
        self.auth = Auth(self.db)
        self.session = Session()
        
        self.clock = p.time.Clock()
    
    def draw_input_field(self, x, y, width, height, text, placeholder, active, is_password=False):
        """Draw an input field with blinking cursor"""
        # Background
        color = self.INPUT_ACTIVE if active else self.INPUT_COLOR
        p.draw.rect(self.screen, color, (x, y, width, height), border_radius=8)
        
        # Border for active field
        if active:
            p.draw.rect(self.screen, self.BUTTON_COLOR, (x, y, width, height), 2, border_radius=8)
        
        # Text or placeholder
        if text:
            display_text = "•" * len(text) if is_password and not self.show_password else text
            text_surface = self.font.render(display_text, True, self.TEXT_COLOR)
            text_x = x + 15
            text_y = y + (height - text_surface.get_height()) // 2
            self.screen.blit(text_surface, (text_x, text_y))
            
            # Draw blinking cursor if active
            if active and self.cursor_visible:
                cursor_x = text_x + text_surface.get_width() + 2
                cursor_y = y + 12
                cursor_height = height - 24
                p.draw.line(self.screen, self.CURSOR_COLOR, 
                           (cursor_x, cursor_y), 
                           (cursor_x, cursor_y + cursor_height), 2)
        else:
            text_surface = self.font.render(placeholder, True, self.TEXT_GRAY)
            self.screen.blit(text_surface, (x + 15, y + (height - text_surface.get_height()) // 2))
        
        return p.Rect(x, y, width, height)
    
    def draw_button(self, x, y, width, height, text, color=None, hover_color=None):
        """Draw a button and return its rect - now uses consistent emerald color"""
        if color is None:
            color = self.BUTTON_COLOR
        if hover_color is None:
            hover_color = self.BUTTON_HOVER
            
        mouse_pos = p.mouse.get_pos()
        rect = p.Rect(x, y, width, height)
        
        # Check hover
        is_hover = rect.collidepoint(mouse_pos)
        button_color = hover_color if is_hover else color
        
        # Draw button
        p.draw.rect(self.screen, button_color, rect, border_radius=8)
        
        # Draw text
        text_surface = self.font.render(text, True, self.TEXT_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return rect
    
    def draw_checkbox(self, x, y, size, checked):
        """Draw a checkbox for show/hide password"""
        rect = p.Rect(x, y, size, size)
        p.draw.rect(self.screen, self.INPUT_COLOR, rect, border_radius=4)
        p.draw.rect(self.screen, self.TEXT_GRAY, rect, 2, border_radius=4)
        
        if checked:
            # Draw checkmark
            p.draw.line(self.screen, self.BUTTON_COLOR, 
                       (x + size*0.2, y + size*0.5), 
                       (x + size*0.4, y + size*0.7), 3)
            p.draw.line(self.screen, self.BUTTON_COLOR, 
                       (x + size*0.4, y + size*0.7), 
                       (x + size*0.8, y + size*0.3), 3)
        
        return rect
    
    def draw(self):
        """Draw the login/register screen"""
        self.screen.fill(self.BG_COLOR)
        
        # Title
        title = "Welcome to Chessly" if self.mode == "login" else "Create Account"
        title_surface = self.title_font.render(title, True, self.TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(self.width // 2, 80))
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle = "Login to continue" if self.mode == "login" else "Register a new account"
        subtitle_surface = self.small_font.render(subtitle, True, self.TEXT_GRAY)
        subtitle_rect = subtitle_surface.get_rect(center=(self.width // 2, 130))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Panel - FIXED HEIGHT to prevent overlap
        panel_y = 180
        panel_height = 450 if self.mode == "register" else 380
        p.draw.rect(self.screen, self.PANEL_COLOR, 
                   (50, panel_y, self.width - 100, panel_height), border_radius=15)
        
        # Input fields
        field_width = self.width - 140
        field_height = 50
        field_x = 70
        current_y = panel_y + 40
        
        # Username field
        label = self.small_font.render("Username", True, self.TEXT_GRAY)
        self.screen.blit(label, (field_x, current_y))
        current_y += 30
        
        self.username_rect = self.draw_input_field(
            field_x, current_y, field_width, field_height,
            self.username_input, "Enter username",
            self.active_field == 'username'
        )
        current_y += field_height + 20
        
        # Email field (only for register)
        if self.mode == "register":
            label = self.small_font.render("Email", True, self.TEXT_GRAY)
            self.screen.blit(label, (field_x, current_y))
            current_y += 30
            
            self.email_rect = self.draw_input_field(
                field_x, current_y, field_width, field_height,
                self.email_input, "Enter email",
                self.active_field == 'email'
            )
            current_y += field_height + 20
        
        # Password field
        label = self.small_font.render("Password", True, self.TEXT_GRAY)
        self.screen.blit(label, (field_x, current_y))
        current_y += 30
        
        self.password_rect = self.draw_input_field(
            field_x, current_y, field_width, field_height,
            self.password_input, "Enter password",
            self.active_field == 'password',
            is_password=True
        )
        current_y += field_height + 15
        
        # Show password checkbox
        checkbox_size = 20
        self.show_password_rect = self.draw_checkbox(
            field_x, current_y, checkbox_size, self.show_password
        )
        show_text = self.small_font.render("Show password", True, self.TEXT_GRAY)
        self.screen.blit(show_text, (field_x + checkbox_size + 10, current_y))
        current_y += 50
        
        # Submit button - CONSISTENT EMERALD COLOR
        button_width = field_width
        button_height = 50
        button_text = "Login" if self.mode == "login" else "Register"
        
        self.submit_button_rect = self.draw_button(
            field_x, current_y, button_width, button_height, button_text
        )
        
        # Switch mode text - FIXED POSITIONING (no overlap)
        switch_y = panel_y + panel_height + 30
        if self.mode == "login":
            switch_text = "Don't have an account? Register"
        else:
            switch_text = "Already have an account? Login"
        
        switch_surface = self.small_font.render(switch_text, True, self.BUTTON_COLOR)
        switch_rect = switch_surface.get_rect(center=(self.width // 2, switch_y))
        self.screen.blit(switch_surface, switch_rect)
        self.switch_button_rect = switch_rect
        
        # Message (error or success) - BELOW switch button
        if self.message:
            message_surface = self.small_font.render(self.message, True, self.message_color)
            message_rect = message_surface.get_rect(center=(self.width // 2, switch_y + 50))
            self.screen.blit(message_surface, message_rect)
        
        p.display.flip()
    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        # Check input field clicks
        if self.username_rect and self.username_rect.collidepoint(pos):
            self.active_field = 'username'
        elif self.email_rect and self.email_rect.collidepoint(pos):
            self.active_field = 'email'
        elif self.password_rect and self.password_rect.collidepoint(pos):
            self.active_field = 'password'
        elif self.show_password_rect and self.show_password_rect.collidepoint(pos):
            self.show_password = not self.show_password
        elif self.submit_button_rect and self.submit_button_rect.collidepoint(pos):
            self.handle_submit()
        elif self.switch_button_rect and self.switch_button_rect.collidepoint(pos):
            self.switch_mode()
        else:
            self.active_field = None
    
    def handle_submit(self):
        """Handle login or register submission"""
        if self.mode == "login":
            # Hardcoded admin authentication bypasses database auth.
            if self.username_input == "admin" and self.password_input == "admin":
                admin_user = {
                    'user_id': -1,
                    'username': 'admin',
                    'email': 'admin@local',
                    'created_at': None,
                    'last_login': None,
                    'is_admin': True
                }
                self.session.login(admin_user)
                self.message = "Admin login successful!"
                self.message_color = self.SUCCESS_COLOR
                p.time.wait(600)
                return True

            success, message, user_data = self.auth.login(
                self.username_input,
                self.password_input
            )
            
            if success:
                self.session.login(user_data)
                self.message = message
                self.message_color = self.SUCCESS_COLOR
                # Login successful - will return True from run()
                p.time.wait(1000)  # Show success message briefly
                return True
            else:
                self.message = message
                self.message_color = self.ERROR_COLOR
        
        else:  # register
            success, message, user_id = self.auth.register(
                self.username_input,
                self.email_input,
                self.password_input
            )
            
            if success:
                self.message = message + " You can now login."
                self.message_color = self.SUCCESS_COLOR
                # Auto-switch to login after brief delay
                p.time.wait(1500)
                self.switch_mode()
                self.clear_inputs()
            else:
                self.message = message
                self.message_color = self.ERROR_COLOR
    
    def switch_mode(self):
        """Switch between login and register"""
        self.mode = "register" if self.mode == "login" else "login"
        self.message = ""
        self.active_field = None
    
    def clear_inputs(self):
        """Clear all input fields"""
        self.username_input = ""
        self.email_input = ""
        self.password_input = ""
    
    def handle_text_input(self, event):
        """Handle keyboard text input"""
        if event.key == p.K_BACKSPACE:
            if self.active_field == 'username' and self.username_input:
                self.username_input = self.username_input[:-1]
            elif self.active_field == 'email' and self.email_input:
                self.email_input = self.email_input[:-1]
            elif self.active_field == 'password' and self.password_input:
                self.password_input = self.password_input[:-1]
        
        elif event.key == p.K_RETURN:
            self.handle_submit()
        
        elif event.key == p.K_TAB:
            # Tab to next field
            if self.mode == "login":
                if self.active_field == 'username':
                    self.active_field = 'password'
                else:
                    self.active_field = 'username'
            else:  # register
                if self.active_field == 'username':
                    self.active_field = 'email'
                elif self.active_field == 'email':
                    self.active_field = 'password'
                else:
                    self.active_field = 'username'
        
        elif event.unicode and len(event.unicode) == 1:
            # Add character to active field
            if self.active_field == 'username' and len(self.username_input) < 20:
                self.username_input += event.unicode
            elif self.active_field == 'email' and len(self.email_input) < 50:
                self.email_input += event.unicode
            elif self.active_field == 'password' and len(self.password_input) < 30:
                self.password_input += event.unicode
    
    def run(self) -> Tuple[bool, Session]:
        """
        Run the login screen
        
        Returns:
            (success: bool, session: Session)
        """
        running = True
        
        while running:
            dt = self.clock.tick(60)
            
            # Update cursor blink
            self.cursor_timer += dt
            if self.cursor_timer >= self.cursor_blink_speed:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
            
            for event in p.event.get():
                if event.type == p.QUIT:
                    p.quit()
                    sys.exit()
                
                elif event.type == p.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                
                elif event.type == p.KEYDOWN:
                    self.handle_text_input(event)
            
            self.draw()
            
            # Check if logged in
            if self.session.is_logged_in:
                return True, self.session
        
        return False, self.session
    
    def close(self):
        """Close the login screen"""
        self.db.close()
        p.quit()


# ==================== TEST CODE ====================
if __name__ == "__main__":
    login_screen = LoginScreen()
    success, session = login_screen.run()
    
    if success:
        print(f"\n✓ Login successful!")
        print(f"  User: {session.get_username()}")
        print(f"  User ID: {session.get_user_id()}")
        print(f"  Session: {session}")
    else:
        print("\n✗ Login cancelled")
    
    login_screen.close()
