from typing import Optional

class Session:
    """Manages the current logged-in user session"""
    
    def __init__(self):
        self.current_user: Optional[dict] = None
        self.is_logged_in: bool = False
    
    def login(self, user_data: dict):
        """Set current user session"""
        self.current_user = user_data
        self.is_logged_in = True
        print(f"Session: User '{user_data['username']}' logged in")
    
    def logout(self):
        """Clear current user session"""
        if self.current_user:
            print(f"Session: User '{self.current_user['username']}' logged out")
        self.current_user = None
        self.is_logged_in = False
    
    def get_user_id(self) -> Optional[int]:
        """Get current user's ID"""
        return self.current_user['user_id'] if self.current_user else None
    
    def get_username(self) -> Optional[str]:
        """Get current user's username"""
        return self.current_user['username'] if self.current_user else None
    
    def require_login(self) -> bool:
        """Check if user is logged in"""
        return self.is_logged_in
    
    def __repr__(self):
        if self.is_logged_in:
            return f"<Session: {self.current_user['username']} (ID: {self.current_user['user_id']})>"
        return "<Session: Not logged in>"


# ==================== TEST CODE ====================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("SESSION TEST")
    print("="*50 + "\n")
    
    session = Session()
    
    print("TEST 1: Initial state")
    print(f"Is logged in: {session.is_logged_in}")
    print(f"Session: {session}\n")
    
    print("TEST 2: Login user")
    test_user = {
        'user_id': 1,
        'username': 'johndoe',
        'email': 'john@example.com'
    }
    session.login(test_user)
    print(f"Is logged in: {session.is_logged_in}")
    print(f"Current user: {session.get_username()}")
    print(f"User ID: {session.get_user_id()}")
    print(f"Session: {session}\n")
    
    print("TEST 3: Logout")
    session.logout()
    print(f"Is logged in: {session.is_logged_in}")
    print(f"Session: {session}")
    
    print("\n" + "="*50)
    print("✓ SESSION TESTS COMPLETE!")
    print("="*50 + "\n")