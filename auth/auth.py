import bcrypt
from database.db import Database
from typing import Optional, Tuple

class Auth:
    """Handles user authentication - registration, login, password hashing"""
    
    def __init__(self, db: Database):
        self.db = db
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
    
    def register(self, username: str, email: str, password: str) -> Tuple[bool, str, Optional[int]]:
        """
        Register a new user
        
        Returns:
            (success: bool, message: str, user_id: Optional[int])
        """
        # Validation
        if len(username) < 3:
            return False, "Username must be at least 3 characters long", None
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long", None
        
        if '@' not in email or '.' not in email:
            return False, "Invalid email format", None
        
        # Check if user already exists
        existing_user = self.db.get_user_by_username(username)
        if existing_user:
            return False, "Username already exists", None
        
        # Hash password and create user
        password_hash = self.hash_password(password)
        user_id = self.db.create_user(username, email, password_hash)
        
        if user_id:
            return True, "Registration successful!", user_id
        else:
            return False, "Email already exists", None
    
    def login(self, username: str, password: str) -> Tuple[bool, str, Optional[dict]]:
        """
        Authenticate a user
        
        Returns:
            (success: bool, message: str, user_data: Optional[dict])
        """
        # Get user from database
        user = self.db.get_user_by_username(username)
        
        if not user:
            return False, "Invalid username or password", None
        
        # Verify password
        if not self.verify_password(password, user['password_hash']):
            return False, "Invalid username or password", None
        
        # Update last login
        self.db.update_last_login(user['user_id'])
        
        # Don't return password hash to caller
        user_data = {
            'user_id': user['user_id'],
            'username': user['username'],
            'email': user['email'],
            'created_at': user['created_at'],
            'last_login': user['last_login']
        }
        
        return True, "Login successful!", user_data
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Change user password
        
        Returns:
            (success: bool, message: str)
        """
        # Get user
        user = self.db.get_user_by_id(user_id)
        if not user:
            return False, "User not found"
        
        # Verify old password
        if not self.verify_password(old_password, user['password_hash']):
            return False, "Current password is incorrect"
        
        # Validate new password
        if len(new_password) < 6:
            return False, "New password must be at least 6 characters long"
        
        # Hash and update
        new_hash = self.hash_password(new_password)
        self.db.cursor.execute(
            'UPDATE users SET password_hash = ? WHERE user_id = ?',
            (new_hash, user_id)
        )
        self.db.conn.commit()
        
        return True, "Password changed successfully!"


# ==================== TEST CODE ====================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("AUTHENTICATION TEST")
    print("="*50 + "\n")
    
    # Create database and auth instances
    db = Database()
    auth = Auth(db)
    
    # Test 1: Register a new user
    print("TEST 1: Registering new user...")
    success, message, user_id = auth.register("testuser123", "test@example.com", "password123")
    print(f"{'✓' if success else '✗'} {message}")
    if user_id:
        print(f"  User ID: {user_id}")
    
    # Test 2: Try to register duplicate username
    print("\nTEST 2: Trying duplicate username...")
    success, message, _ = auth.register("testuser123", "another@email.com", "password123")
    print(f"{'✓' if not success else '✗'} {message} (should fail)")
    
    # Test 3: Login with correct credentials
    print("\nTEST 3: Login with correct password...")
    success, message, user_data = auth.login("testuser123", "password123")
    print(f"{'✓' if success else '✗'} {message}")
    if user_data:
        print(f"  Logged in as: {user_data['username']}")
    
    # Test 4: Login with wrong password
    print("\nTEST 4: Login with wrong password...")
    success, message, _ = auth.login("testuser123", "wrongpassword")
    print(f"{'✓' if not success else '✗'} {message} (should fail)")
    
    # Test 5: Login with non-existent user
    print("\nTEST 5: Login with non-existent user...")
    success, message, _ = auth.login("nonexistent", "password123")
    print(f"{'✓' if not success else '✗'} {message} (should fail)")
    
    # Test 6: Password validation
    print("\nTEST 6: Register with short password...")
    success, message, _ = auth.register("newuser", "new@example.com", "12345")
    print(f"{'✓' if not success else '✗'} {message} (should fail)")
    
    # Test 7: Change password
    if user_id:
        print("\nTEST 7: Changing password...")
        success, message = auth.change_password(user_id, "password123", "newpassword456")
        print(f"{'✓' if success else '✗'} {message}")
        
        print("\nTEST 8: Login with new password...")
        success, message, _ = auth.login("testuser123", "newpassword456")
        print(f"{'✓' if success else '✗'} {message}")
    
    db.close()
    
    print("\n" + "="*50)
    print("✓ AUTHENTICATION TESTS COMPLETE!")
    print("="*50 + "\n")