# ♟️ Chessly

A desktop chess game where you play against an AI that uses negamax search to evaluate moves. Built to understand how chess engines work, it includes user authentication, game history tracking, and three difficulty levels.

![Windows](https://img.shields.io/badge/Windows-0078D6?style=flat&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-00ADD8?style=flat&logo=python&logoColor=white)

## Features

- **Three AI Difficulty Levels**: Easy (depth 1), Medium (depth 2), Hard (depth 3)
- **AI vs AI Mode**: Watch the engine play against itself
- **Opening Book**: 50+ classic opening lines (Sicilian, French, Caro-Kann, etc.)
- **User Accounts**: Secure registration and login with bcrypt password hashing
- **Game History**: SQLite database stores all your games with complete move lists
- **Admin Dashboard**: View users, browse game logs, and check stats
- **Complete Ruleset**: Castling, en passant, pawn promotion, 50-move rule, and threefold repetition

## How to Run

### Windows (Easy Way)

1. Download `Chessly.exe` from [Releases](../../releases)
2. Run it—no Python installation needed

### From Source

```bash
git clone https://github.com/yourusername/chessly.git
cd chessly
pip install -r requirements.txt
python ChessMain.py
```

To build the executable:
```bash
python build_executable.py
```

## How the AI Works

The engine uses negamax with several optimizations:

- **Alpha-Beta Pruning**: Skips unpromising branches
- **Zobrist Hashing**: Fast position representation
- **Transposition Table**: Caches 500,000+ positions
- **Quiescence Search**: Extends search during tactical sequences
- **Move Ordering**: Evaluates strong moves first for faster cutoffs

Position evaluation uses piece values, piece-square tables, and bonuses for things like bishop pairs and rooks on open files.

## Tech Stack

- **Python 3.x** - Core language
- **Pygame** - GUI and rendering
- **SQLite** - Game storage
- **bcrypt** - Password hashing
- **PyInstaller** - Standalone executable

## Project Structure
```text
chess/
├── ChessMain.py              # Main game loop
├── ChessEngine.py            # Board state and move generation
├── SmartMoveFinder.py        # AI engine (negamax + optimizations)
├── ChessOpenings.py          # Opening book
├── database/db.py            # SQLite wrapper
├── auth/                     # Authentication system
├── ui/login_screen.py        # Login/register UI
├── admin/admin_panel.py      # Admin dashboard
└── images/                   # Chess piece sprites
```
## Admin Access

Use the following credentials to access the dashboard. From here, you can view past game records, browse user activity, and manage account details:

Username: `admin`  
Password: `admin`

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built to learn how chess engines work. Feel free to open an issue if you find bugs!