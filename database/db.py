import sqlite3
import os
from typing import Optional, List

class Database:
    def __init__(self, db_path='database/chess.db'):
        """Initialize database connection and create tables if they don't exist"""
        # Ensure database directory exists
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else '.', exist_ok=True)
        
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # Allow dict-like access to rows
        self.cursor = self.conn.cursor()
        self._create_tables()
    
    def _create_tables(self):
        """Create all necessary tables - NEW LICHESS-STYLE SCHEMA"""
        
        # USERS table (unchanged)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME
            )
        ''')
        
        # GAMES table - NOW WITH MOVES COLUMN (no separate moves table!)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                game_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                difficulty TEXT NOT NULL,
                result TEXT,
                moves TEXT,
                total_moves INTEGER DEFAULT 0,
                started_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                ended_at DATETIME,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        ''')
        
        self.conn.commit()
        print(f"✓ Database initialized at {self.db_path}")
        print(f"✓ Schema: Lichess-style (moves stored as TEXT)")
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, username: str, email: str, password_hash: str) -> Optional[int]:
        """Create a new user. Returns user_id if successful, None if username/email exists"""
        try:
            self.cursor.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[dict]:
        """Get user by username. Returns dict with user data or None"""
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        """Get user by ID"""
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def update_last_login(self, user_id: int):
        """Update user's last login timestamp"""
        self.cursor.execute(
            'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = ?',
            (user_id,)
        )
        self.conn.commit()
    
    def get_all_users(self) -> List[dict]:
        """Get all users (for admin viewing)"""
        self.cursor.execute(
            'SELECT user_id, username, email, created_at, last_login FROM users ORDER BY created_at DESC'
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user (CASCADE will delete their games)"""
        try:
            self.cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting user: {e}")
            return False
    
    # ==================== GAME OPERATIONS (UPDATED) ====================
    
    def create_game(self, user_id: int, difficulty: str) -> int:
        """Create a new game. Returns game_id"""
        self.cursor.execute(
            'INSERT INTO games (user_id, difficulty, result) VALUES (?, ?, ?)',
            (user_id, difficulty, 'ongoing')
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def end_game(self, game_id: int, result: str, moves_string: str, total_moves: int):
        """
        End a game and save all moves as a single string
        
        Args:
            game_id: The game ID
            result: 'win', 'loss', 'draw', or 'resign'
            moves_string: Space-separated moves (e.g., "e2e4 e7e5 g1f3")
            total_moves: Number of moves
        """
        self.cursor.execute(
            '''UPDATE games 
               SET result = ?, moves = ?, ended_at = CURRENT_TIMESTAMP, total_moves = ?
               WHERE game_id = ?''',
            (result, moves_string, total_moves, game_id)
        )
        self.conn.commit()
    
    def get_game_by_id(self, game_id: int) -> Optional[dict]:
        """Get a specific game by ID"""
        self.cursor.execute('SELECT * FROM games WHERE game_id = ?', (game_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None
    
    def get_user_games(self, user_id: int, limit: int = 20) -> List[dict]:
        """Get recent games for a user"""
        self.cursor.execute(
            '''SELECT * FROM games 
               WHERE user_id = ? 
               ORDER BY started_at DESC 
               LIMIT ?''',
            (user_id, limit)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_all_games(self, limit: int = 50) -> List[dict]:
        """Get all games with username (for admin)"""
        self.cursor.execute(
            '''SELECT g.*, u.username 
               FROM games g
               JOIN users u ON g.user_id = u.user_id
               ORDER BY g.started_at DESC 
               LIMIT ?''',
            (limit,)
        )
        return [dict(row) for row in self.cursor.fetchall()]

    def get_total_games_count(self) -> int:
        """Get total number of games in the system"""
        self.cursor.execute('SELECT COUNT(*) AS total FROM games')
        row = self.cursor.fetchone()
        return row['total'] if row else 0

    def update_user(self, user_id: int, username: str, email: str, password_hash: Optional[str] = None) -> tuple[bool, str]:
        """Update user fields. Password is optional."""
        try:
            if password_hash:
                self.cursor.execute(
                    'UPDATE users SET username = ?, email = ?, password_hash = ? WHERE user_id = ?',
                    (username, email, password_hash, user_id)
                )
            else:
                self.cursor.execute(
                    'UPDATE users SET username = ?, email = ? WHERE user_id = ?',
                    (username, email, user_id)
                )
            self.conn.commit()
            if self.cursor.rowcount == 0:
                return False, "User not found"
            return True, "User updated successfully"
        except sqlite3.IntegrityError as e:
            lower_error = str(e).lower()
            if 'username' in lower_error:
                return False, "Username already exists"
            if 'email' in lower_error:
                return False, "Email already exists"
            return False, "Could not update user"
    
    def get_user_stats(self, user_id: int) -> dict:
        """Get win/loss/draw statistics for a user"""
        self.cursor.execute(
            '''SELECT 
                COUNT(*) as total_games,
                SUM(CASE WHEN result = 'win' THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN result = 'loss' THEN 1 ELSE 0 END) as losses,
                SUM(CASE WHEN result = 'draw' THEN 1 ELSE 0 END) as draws,
                SUM(CASE WHEN result = 'resign' THEN 1 ELSE 0 END) as resigns
               FROM games 
               WHERE user_id = ? AND result IS NOT NULL AND result != 'ongoing' ''',
            (user_id,)
        )
        row = self.cursor.fetchone()
        return dict(row) if row else {
            'total_games': 0, 'wins': 0, 'losses': 0, 'draws': 0, 'resigns': 0
        }
    
    def get_game_moves(self, game_id: int) -> List[str]:
        """
        Get all moves for a game as a list
        
        Returns:
            List of moves in notation (e.g., ['e2e4', 'e7e5', 'g1f3'])
        """
        game = self.get_game_by_id(game_id)
        if game and game['moves']:
            return game['moves'].split()
        return []
    
    # ==================== UTILITY ====================
    
    def close(self):
        """Close database connection"""
        self.conn.close()
    
    def __enter__(self):
        """Context manager support"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close connection when exiting context"""
        self.close()


# ==================== TEST CODE ====================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("DATABASE TEST - Lichess-Style Schema")
    print("="*50 + "\n")
    
    # Create database instance
    db = Database()
    
    # Test 1: Create a test user
    print("TEST 1: Creating user...")
    test_user_id = db.create_user("testplayer", "test@example.com", "hashed_password_123")
    if test_user_id:
        print(f"✓ User created with ID: {test_user_id}")
    else:
        print("✗ User creation failed (may already exist)")
    
    # Test 2: Retrieve user
    print("\nTEST 2: Retrieving user...")
    user = db.get_user_by_username("testplayer")
    if user:
        print(f"✓ Retrieved user: {user['username']} (email: {user['email']})")
    
    # Test 3: Create a game
    print("\nTEST 3: Creating game...")
    game_id = db.create_game(test_user_id or 1, "medium")
    print(f"✓ Game created with ID: {game_id}")
    
    # Test 4: Simulate moves (like from gs.moveLog)
    print("\nTEST 4: Simulating game moves...")
    simulated_moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "f8c5"]
    moves_string = " ".join(simulated_moves)
    print(f"✓ Moves string: {moves_string}")
    
    # Test 5: End game with moves
    print("\nTEST 5: Ending game...")
    db.end_game(game_id, "win", moves_string, len(simulated_moves))
    print(f"✓ Game ended as 'win' with {len(simulated_moves)} moves")
    
    # Test 6: Retrieve game
    print("\nTEST 6: Retrieving game...")
    saved_game = db.get_game_by_id(game_id)
    print(f"✓ Game {saved_game['game_id']}: {saved_game['result']}")
    print(f"  Difficulty: {saved_game['difficulty']}")
    print(f"  Total moves: {saved_game['total_moves']}")
    print(f"  Moves: {saved_game['moves']}")
    
    # Test 7: Get moves as list
    print("\nTEST 7: Parsing moves...")
    moves_list = db.get_game_moves(game_id)
    print(f"✓ Parsed {len(moves_list)} moves:")
    print(f"  {moves_list}")
    
    # Test 8: Get user stats
    print("\nTEST 8: User statistics...")
    stats = db.get_user_stats(test_user_id or 1)
    print(f"✓ Stats for user:")
    print(f"   Total games: {stats['total_games']}")
    print(f"   Wins: {stats['wins']}")
    print(f"   Losses: {stats['losses']}")
    print(f"   Draws: {stats['draws']}")
    
    db.close()
    
    print("\n" + "="*50)
    print("✓ ALL TESTS PASSED!")
    print("="*50 + "\n")
    print("New schema uses 1 row per game (Lichess-style)")
    print("Moves stored as TEXT: 'e2e4 e7e5 g1f3'")
