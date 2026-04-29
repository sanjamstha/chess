import os
import sys
import pygame as p
import ChessEngine, SmartMoveFinder
from ui.login_screen import LoginScreen
from admin.admin_panel import AdminPanel
from database.db import Database
from auth.session import Session

# ═══════════════════════════════════════════════════════════════
# LAYOUT CONSTANTS
# ═══════════════════════════════════════════════════════════════
BOARD_SIZE = 600
SIDEBAR_WIDTH = 300
WINDOW_WIDTH = BOARD_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = BOARD_SIZE

DIMENSION = 8
SQ_SIZE = BOARD_SIZE // DIMENSION
MAX_FPS = 60

# ═══════════════════════════════════════════════════════════════
# COLORS - EMERALD THEME
# ═══════════════════════════════════════════════════════════════
BG_COLOR = (40, 44, 52)
PANEL_COLOR = (50, 54, 62)
BUTTON_COLOR = (16, 185, 129)
BUTTON_HOVER = (52, 211, 153)
BUTTON_DISABLED = (80, 84, 92)
TEXT_COLOR = (255, 255, 255)
TEXT_GRAY = (158, 158, 158)
HIGHLIGHT_COLOR = (70, 74, 82)

LIGHT_SQ = (240, 217, 181)
DARK_SQ = (181, 136, 99)
HIGHLIGHT_LAST_MOVE = (205, 210, 106, 128)
HIGHLIGHT_SELECTED = (130, 151, 105, 128)

# ═══════════════════════════════════════════════════════════════
# GLOBAL STATE
# ═══════════════════════════════════════════════════════════════
IMAGES = {}
APP_NAME = "Chessly"

# Game state
game_mode = "play"  # "play", "replay", or "finished"
replay_index = -1
player_color = "white"
board_flipped = False
game_type = "player_vs_ai"  # "player_vs_ai" or "ai_vs_ai"
white_ai_difficulty = "medium"
black_ai_difficulty = "medium"

# Move list scrolling
move_list_scroll = 0
move_list_max_scroll = 0

def get_asset_path(*path_parts):
    """Resolve asset paths for both source runs and PyInstaller builds."""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, *path_parts)

def set_app_icon():
    """Set the application window icon when available."""
    icon_path = get_asset_path("images", "chessly.png")
    if os.path.exists(icon_path):
        try:
            p.display.set_icon(p.image.load(icon_path))
        except p.error:
            pass

def loadImages():
    """Load piece images"""
    pieces = ['wp','wK','wQ','wN','wB','wR','bp','bK','bQ','bN','bB','bR']
    for piece in pieces:
        IMAGES[piece] = p.transform.smoothscale(
            p.image.load(get_asset_path("images", f"{piece}.png")),
            (SQ_SIZE, SQ_SIZE)
        )

def generate_pgn_string(gs):
    """Generate PGN notation with check/checkmate symbols"""
    temp_gs = ChessEngine.GameState()
    pgn_moves = []
    
    for i, move in enumerate(gs.moveLog):
        temp_gs.makeMove(move)
        in_check = temp_gs.inCheck()
        valid_moves = temp_gs.getValidMoves()
        is_checkmate = (len(valid_moves) == 0 and in_check)
        san = move.getSAN(temp_gs, is_check=in_check, is_checkmate=is_checkmate)
        pgn_moves.append(san)
    
    return " ".join(pgn_moves)


# ═══════════════════════════════════════════════════════════════
# MAIN GAME LOOP
# ═══════════════════════════════════════════════════════════════

def main():
    # ────────────────────────────────────────────────────────────
    # STEP 1: LOGIN
    # ────────────────────────────────────────────────────────────
    print("\n" + "="*50)
    print(f"{APP_NAME.upper()} - Starting Login Screen")
    print("="*50 + "\n")
    
    login_screen = LoginScreen()
    success, session = login_screen.run()
    
    if not success:
        print("Login cancelled. Exiting...")
        return
    
    print(f"\n✓ Logged in as: {session.get_username()}")
    print(f"  User ID: {session.get_user_id()}\n")

    if session.current_user and session.current_user.get("is_admin"):
        print("✓ Admin mode detected. Launching Admin Dashboard...")
        login_screen.close()
        admin_panel = AdminPanel()
        admin_panel.run()
        admin_panel.close()
        p.quit()
        return

    login_screen.close()
    
    # ────────────────────────────────────────────────────────────
    # STEP 2: GAME LOOP (can restart games)
    # ────────────────────────────────────────────────────────────
    p.init()
    screen = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    set_app_icon()
    p.display.set_caption(f"{APP_NAME} - {session.get_username()}")
    clock = p.time.Clock()
    
    loadImages()
    db = Database()
    
    keep_playing = True
    
    while keep_playing:
        # Run one game
        result = run_single_game(screen, clock, db, session)
        
        if result == "quit":
            keep_playing = False
        elif result == "logout":
            keep_playing = False
            print(f"\n✓ {session.get_username()} logged out")
        elif result == "new_game":
            # Loop continues, will call run_single_game again
            continue
        else:
            keep_playing = False
    
    db.close()
    p.quit()


def run_single_game(screen, clock, db, session):
    """
    Run a single chess game.
    Returns: "quit", "new_game", "logout", or "finished"
    """
    global player_color, board_flipped, game_mode, replay_index, move_list_scroll, move_list_max_scroll
    global game_type, white_ai_difficulty, black_ai_difficulty
    
    # ────────────────────────────────────────────────────────────
    # GAME SETUP
    # ────────────────────────────────────────────────────────────
    setup_result = selectGameSettings(screen, clock)
    
    if setup_result == "logout":
        return "logout"
    
    game_type, player_color, white_ai_difficulty, black_ai_difficulty = setup_result
    
    board_flipped = (player_color == "black")
    
    # Set difficulty based on game type
    if game_type == "player_vs_ai":
        difficulty = white_ai_difficulty if player_color == "black" else black_ai_difficulty
        print(f"✓ Game type: Player vs AI")
        print(f"  You: {player_color}, AI: {difficulty}")
    else:
        difficulty = "ai_vs_ai"
        print(f"✓ Game type: AI vs AI")
        print(f"  White AI: {white_ai_difficulty}, Black AI: {black_ai_difficulty}")
    
    current_game_id = db.create_game(session.get_user_id(), difficulty)
    print(f"✓ Game created (ID: {current_game_id})")
    
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    
    sqSelected = ()
    playerClicks = []
    
    game_mode = "play"
    replay_index = -1
    move_list_scroll = 0
    move_list_max_scroll = 0
    
    gameOver = False
    game_result = None  # Will store (result, text, pgn)
    game_is_active = True  # NEW: Track if game is active (not resigned)
    
    # Determine who is human/AI
    if game_type == "player_vs_ai":
        playerOne = (player_color == "white")
        playerTwo = (player_color == "black")
    else:
        playerOne = False  # Both are AI
        playerTwo = False
    
    running = True
    
    # ────────────────────────────────────────────────────────────
    # GAME LOOP
    # ────────────────────────────────────────────────────────────
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        
        for e in p.event.get():
            if e.type == p.QUIT:
                return "quit"
            
            # ── MOUSE WHEEL (SCROLL MOVE LIST) ──
            elif e.type == p.MOUSEWHEEL:
                # Only scroll if mouse is over sidebar
                mouse_x, mouse_y = p.mouse.get_pos()
                if mouse_x >= BOARD_SIZE:
                    move_list_scroll -= e.y * 20  # Scroll speed
                    move_list_scroll = max(0, min(move_list_scroll, move_list_max_scroll))
            
            # ── MOUSE CLICKS ──
            elif e.type == p.MOUSEBUTTONDOWN:
                x, y = e.pos
                
                # Check if click is on sidebar
                if x >= BOARD_SIZE:
                    action = handle_sidebar_click(x, y, gs, db, current_game_id, session, validMoves, game_is_active)
                    
                    if action == "quit":
                        return "quit"
                    elif action == "new_game":
                        return "new_game"
                    elif action == "logout":
                        return "logout"
                    elif action == "resigned":
                        # Set game to finished state
                        game_mode = "finished"
                        gameOver = True
                        game_is_active = False
                        
                        # Determine result
                        result = 'loss' if player_color == "white" else 'win'
                        text = f"{'Black' if player_color == 'white' else 'White'} wins by Resignation!"
                        pgn = generate_pgn_string(gs)
                        
                        game_result = (result, text, pgn, len(gs.moveLog))
                    
                    continue
                
                # Board clicks (only in play mode, not finished, and if human turn)
                if game_mode == "play" and not gameOver and humanTurn:
                    col, row = get_square_from_pos(x, y)
                    
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                                break
                        
                        if not moveMade:
                            playerClicks = [sqSelected]
            
            # ── KEYBOARD CONTROLS ──
            elif e.type == p.KEYDOWN:
                # Only allow navigation if not in finished state
                if game_mode != "finished":
                    if e.key == p.K_LEFT:
                        navigate_replay(gs, "prev")
                    elif e.key == p.K_RIGHT:
                        navigate_replay(gs, "next")
                    elif e.key == p.K_DOWN:
                        navigate_replay(gs, "start")
                    elif e.key == p.K_UP:
                        navigate_replay(gs, "end")
                    elif e.key == p.K_u:
                        try_undo_move(gs, validMoves, game_is_active)
                    elif e.key == p.K_f:
                        board_flipped = not board_flipped
        
        # ── AI MOVE (only if game is active) ──
        if game_mode == "play" and not gameOver and not humanTurn:
            # Determine which AI to use
            if game_type == "ai_vs_ai":
                current_difficulty = white_ai_difficulty if gs.whiteToMove else black_ai_difficulty
            else:
                current_difficulty = white_ai_difficulty if gs.whiteToMove else black_ai_difficulty
            
            AIMove, eval_score = SmartMoveFinder.findBestMove(gs, validMoves, current_difficulty)
            
            if AIMove is None:
                AIMove = SmartMoveFinder.findRandomMove(validMoves)
            
            gs.makeMove(AIMove)
            moveMade = True
            animate = True
        
        # ── UPDATE GAME STATE ──
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            
            validMoves = gs.getValidMoves()
            gs.checkFiftyMoveRule()
            gs.checkThreefoldRepetition()
            
            moveMade = False
            animate = False
            
            # Exit replay mode when new move is made
            if game_mode == "replay":
                game_mode = "play"
                replay_index = -1
        
        # ── CHECK FOR GAME OVER ──
        if gs.checkMate or gs.staleMate or gs.drawByFiftyMoves or gs.drawByRepetition:
            if not gameOver:
                gameOver = True
                game_mode = "finished"
                game_is_active = False
                
                if gs.staleMate:
                    result = 'draw'
                    text = 'Draw by Stalemate!'
                elif gs.drawByFiftyMoves:
                    result = 'draw'
                    text = 'Draw by Fifty-Move Rule!'
                elif gs.drawByRepetition:
                    result = 'draw'
                    text = 'Draw by Threefold Repetition!'
                else:
                    if gs.whiteToMove:
                        result = 'loss' if player_color == "white" else 'win'
                        text = 'Black wins by Checkmate!'
                    else:
                        result = 'win' if player_color == "white" else 'loss'
                        text = 'White wins by Checkmate!'
                
                pgn = generate_pgn_string(gs)
                db.end_game(current_game_id, result, pgn, len(gs.moveLog))
                
                game_result = (result, text, pgn, len(gs.moveLog))
                
                print(f"\n✓ Game Over: {result.upper()}")
                print(f"  {text}")
                print(f"  Saved to database (ID: {current_game_id})\n")
        
        # ── RENDER ──
        drawGameState(screen, gs, validMoves, sqSelected)
        
        # Show post-game summary popup
        if gameOver and game_result:
            action = drawPostGameSummary(screen, game_result)
            if action == "new_game":
                return "new_game"
            elif action == "quit":
                return "quit"
        
        clock.tick(MAX_FPS)
        p.display.flip()
    
    return "finished"


# ═══════════════════════════════════════════════════════════════
# GAME SETTINGS SCREEN - NOW WITH AI VS AI MODE
# ═══════════════════════════════════════════════════════════════

def selectGameSettings(screen, clock):
    """
    Select game type, player color, and AI difficulties
    Returns: (game_type, player_color, white_ai_diff, black_ai_diff) or "logout"
    """
    selecting = True
    game_type = "player_vs_ai"  # "player_vs_ai" or "ai_vs_ai"
    selected_color = "white"
    white_ai_diff = "medium"
    black_ai_diff = "medium"
    
    # Dropdown states
    white_dropdown_open = False
    black_dropdown_open = False
    
    font_title = p.font.SysFont("Arial", 32, bold=True)
    font_label = p.font.SysFont("Arial", 20)
    font_button = p.font.SysFont("Arial", 24)
    font_small = p.font.SysFont("Arial", 18)
    
    while selecting:
        screen.fill(BG_COLOR)
        
        title = font_title.render("Game Setup", True, TEXT_COLOR)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))
        
        mouse_pos = p.mouse.get_pos()
        
        # ── GAME TYPE SELECTION ──
        label = font_label.render("Game Type:", True, TEXT_GRAY)
        screen.blit(label, (100, 120))
        
        pvai_rect = p.Rect(100, 160, 180, 50)
        aivai_rect = p.Rect(300, 160, 180, 50)
        
        pvai_color = BUTTON_COLOR if game_type == "player_vs_ai" else (BUTTON_HOVER if pvai_rect.collidepoint(mouse_pos) else PANEL_COLOR)
        p.draw.rect(screen, pvai_color, pvai_rect, border_radius=8)
        pvai_text = font_button.render("Player vs AI", True, TEXT_COLOR)
        screen.blit(pvai_text, (pvai_rect.centerx - pvai_text.get_width() // 2, pvai_rect.centery - pvai_text.get_height() // 2))
        
        aivai_color = BUTTON_COLOR if game_type == "ai_vs_ai" else (BUTTON_HOVER if aivai_rect.collidepoint(mouse_pos) else PANEL_COLOR)
        p.draw.rect(screen, aivai_color, aivai_rect, border_radius=8)
        aivai_text = font_button.render("AI vs AI", True, TEXT_COLOR)
        screen.blit(aivai_text, (aivai_rect.centerx - aivai_text.get_width() // 2, aivai_rect.centery - aivai_text.get_height() // 2))
        
        current_y = 240
        
        # ── PLAYER VS AI OPTIONS ──
        if game_type == "player_vs_ai":
            # Color selection
            label = font_label.render("Play as:", True, TEXT_GRAY)
            screen.blit(label, (100, current_y))
            current_y += 40
            
            white_rect = p.Rect(100, current_y, 150, 50)
            black_rect = p.Rect(270, current_y, 150, 50)
            
            white_color = BUTTON_COLOR if selected_color == "white" else (BUTTON_HOVER if white_rect.collidepoint(mouse_pos) else PANEL_COLOR)
            p.draw.rect(screen, white_color, white_rect, border_radius=8)
            white_text = font_button.render("White", True, TEXT_COLOR)
            screen.blit(white_text, (white_rect.centerx - white_text.get_width() // 2, white_rect.centery - white_text.get_height() // 2))
            
            black_color = BUTTON_COLOR if selected_color == "black" else (BUTTON_HOVER if black_rect.collidepoint(mouse_pos) else PANEL_COLOR)
            p.draw.rect(screen, black_color, black_rect, border_radius=8)
            black_text = font_button.render("Black", True, TEXT_COLOR)
            screen.blit(black_text, (black_rect.centerx - black_text.get_width() // 2, black_rect.centery - black_text.get_height() // 2))
            
            current_y += 80
            
            # AI difficulty (opponent)
            label = font_label.render("AI Difficulty:", True, TEXT_GRAY)
            screen.blit(label, (100, current_y))
            current_y += 40
            
            ai_diff = white_ai_diff if selected_color == "black" else black_ai_diff
            
            easy_rect = p.Rect(100, current_y, 100, 50)
            medium_rect = p.Rect(220, current_y, 100, 50)
            hard_rect = p.Rect(340, current_y, 100, 50)
            
            easy_color = BUTTON_COLOR if ai_diff == "easy" else (BUTTON_HOVER if easy_rect.collidepoint(mouse_pos) else PANEL_COLOR)
            p.draw.rect(screen, easy_color, easy_rect, border_radius=8)
            easy_text = font_button.render("Easy", True, TEXT_COLOR)
            screen.blit(easy_text, (easy_rect.centerx - easy_text.get_width() // 2, easy_rect.centery - easy_text.get_height() // 2))
            
            medium_color = BUTTON_COLOR if ai_diff == "medium" else (BUTTON_HOVER if medium_rect.collidepoint(mouse_pos) else PANEL_COLOR)
            p.draw.rect(screen, medium_color, medium_rect, border_radius=8)
            medium_text = font_button.render("Med", True, TEXT_COLOR)
            screen.blit(medium_text, (medium_rect.centerx - medium_text.get_width() // 2, medium_rect.centery - medium_text.get_height() // 2))
            
            hard_color = BUTTON_COLOR if ai_diff == "hard" else (BUTTON_HOVER if hard_rect.collidepoint(mouse_pos) else PANEL_COLOR)
            p.draw.rect(screen, hard_color, hard_rect, border_radius=8)
            hard_text = font_button.render("Hard", True, TEXT_COLOR)
            screen.blit(hard_text, (hard_rect.centerx - hard_text.get_width() // 2, hard_rect.centery - hard_text.get_height() // 2))
        
        # ── AI VS AI OPTIONS ──
        else:
            # White AI difficulty dropdown
            label = font_label.render("White AI:", True, TEXT_GRAY)
            screen.blit(label, (100, current_y))
            current_y += 40
            
            white_dropdown_rect = p.Rect(100, current_y, 150, 50)
            draw_dropdown(screen, white_dropdown_rect, white_ai_diff, white_dropdown_open, mouse_pos, font_button, font_small)
            
            current_y += 70 if white_dropdown_open else 80
            
            # Black AI difficulty dropdown
            label = font_label.render("Black AI:", True, TEXT_GRAY)
            screen.blit(label, (100, current_y))
            current_y += 40
            
            black_dropdown_rect = p.Rect(100, current_y, 150, 50)
            draw_dropdown(screen, black_dropdown_rect, black_ai_diff, black_dropdown_open, mouse_pos, font_button, font_small)
        
        # ── START BUTTON ──
        start_rect = p.Rect(150, 510, 200, 60)
        start_color = BUTTON_HOVER if start_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        p.draw.rect(screen, start_color, start_rect, border_radius=10)
        start_text = font_title.render("Start Game", True, TEXT_COLOR)
        screen.blit(start_text, (start_rect.centerx - start_text.get_width() // 2, start_rect.centery - start_text.get_height() // 2))
        
        # ── LOGOUT BUTTON ──
        logout_rect = p.Rect(380, 510, 120, 60)
        logout_color = BUTTON_HOVER if logout_rect.collidepoint(mouse_pos) else BUTTON_DISABLED
        p.draw.rect(screen, logout_color, logout_rect, border_radius=10)
        logout_text = font_button.render("Logout", True, TEXT_COLOR)
        screen.blit(logout_text, (logout_rect.centerx - logout_text.get_width() // 2, logout_rect.centery - logout_text.get_height() // 2))
        
        p.display.flip()
        
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                return ("player_vs_ai", "white", "medium", "medium")
            
            elif event.type == p.MOUSEBUTTONDOWN:
                if pvai_rect.collidepoint(event.pos):
                    game_type = "player_vs_ai"
                    white_dropdown_open = False
                    black_dropdown_open = False
                
                elif aivai_rect.collidepoint(event.pos):
                    game_type = "ai_vs_ai"
                
                elif logout_rect.collidepoint(event.pos):
                    return "logout"
                
                elif game_type == "player_vs_ai":
                    if white_rect.collidepoint(event.pos):
                        selected_color = "white"
                    elif black_rect.collidepoint(event.pos):
                        selected_color = "black"
                    elif easy_rect.collidepoint(event.pos):
                        if selected_color == "black":
                            white_ai_diff = "easy"
                        else:
                            black_ai_diff = "easy"
                    elif medium_rect.collidepoint(event.pos):
                        if selected_color == "black":
                            white_ai_diff = "medium"
                        else:
                            black_ai_diff = "medium"
                    elif hard_rect.collidepoint(event.pos):
                        if selected_color == "black":
                            white_ai_diff = "hard"
                        else:
                            black_ai_diff = "hard"
                    elif start_rect.collidepoint(event.pos):
                        return (game_type, selected_color, white_ai_diff, black_ai_diff)
                
                else:  # ai_vs_ai
                    # Handle dropdowns
                    if white_dropdown_rect.collidepoint(event.pos):
                        white_dropdown_open = not white_dropdown_open
                        black_dropdown_open = False
                    elif black_dropdown_rect.collidepoint(event.pos):
                        black_dropdown_open = not black_dropdown_open
                        white_dropdown_open = False
                    elif start_rect.collidepoint(event.pos):
                        return (game_type, selected_color, white_ai_diff, black_ai_diff)
                    else:
                        # Check dropdown options
                        if white_dropdown_open:
                            option_y = white_dropdown_rect.y + 50
                            for i, option in enumerate(["easy", "medium", "hard"]):
                                option_rect = p.Rect(white_dropdown_rect.x, option_y + i * 35, white_dropdown_rect.width, 35)
                                if option_rect.collidepoint(event.pos):
                                    white_ai_diff = option
                                    white_dropdown_open = False
                                    break
                        
                        if black_dropdown_open:
                            option_y = black_dropdown_rect.y + 50
                            for i, option in enumerate(["easy", "medium", "hard"]):
                                option_rect = p.Rect(black_dropdown_rect.x, option_y + i * 35, black_dropdown_rect.width, 35)
                                if option_rect.collidepoint(event.pos):
                                    black_ai_diff = option
                                    black_dropdown_open = False
                                    break
        
        clock.tick(60)


def draw_dropdown(screen, rect, selected_value, is_open, mouse_pos, font_button, font_small):
    """Draw a dropdown menu"""
    # Main button
    main_color = BUTTON_HOVER if rect.collidepoint(mouse_pos) else BUTTON_COLOR
    p.draw.rect(screen, main_color, rect, border_radius=8)
    
    # Selected value text
    value_text = font_button.render(selected_value.capitalize(), True, TEXT_COLOR)
    screen.blit(value_text, (rect.x + 15, rect.centery - value_text.get_height() // 2))
    
    # Dropdown arrow
    arrow = "▼" if not is_open else "▲"
    arrow_text = font_small.render(arrow, True, TEXT_COLOR)
    screen.blit(arrow_text, (rect.right - 30, rect.centery - arrow_text.get_height() // 2))
    
    # Options (if open)
    if is_open:
        options = ["easy", "medium", "hard"]
        option_y = rect.y + 50
        
        for i, option in enumerate(options):
            option_rect = p.Rect(rect.x, option_y + i * 35, rect.width, 35)
            option_color = BUTTON_HOVER if option_rect.collidepoint(mouse_pos) else PANEL_COLOR
            p.draw.rect(screen, option_color, option_rect, border_radius=6)
            
            option_text = font_small.render(option.capitalize(), True, TEXT_COLOR)
            screen.blit(option_text, (option_rect.x + 15, option_rect.centery - option_text.get_height() // 2))


# ═══════════════════════════════════════════════════════════════
# POST-GAME SUMMARY POPUP
# ═══════════════════════════════════════════════════════════════

def drawPostGameSummary(screen, game_result):
    """
    Display post-game summary popup.
    Returns: "new_game", "quit", or None (still showing)
    """
    result, text, pgn, total_moves = game_result
    
    # Semi-transparent overlay
    overlay = p.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Popup dimensions
    popup_width = 700
    popup_height = 500
    popup_x = (WINDOW_WIDTH - popup_width) // 2
    popup_y = (WINDOW_HEIGHT - popup_height) // 2
    
    # Draw popup background
    popup_rect = p.Rect(popup_x, popup_y, popup_width, popup_height)
    p.draw.rect(screen, PANEL_COLOR, popup_rect, border_radius=15)
    p.draw.rect(screen, BUTTON_COLOR, popup_rect, 3, border_radius=15)
    
    # Fonts
    font_title = p.font.SysFont("Arial", 36, bold=True)
    font_subtitle = p.font.SysFont("Arial", 20)
    font_pgn = p.font.SysFont("Courier New", 14)
    font_button = p.font.SysFont("Arial", 22)
    
    y_offset = popup_y + 30
    
    # Title
    title_color = BUTTON_COLOR if result == "win" else (TEXT_GRAY if result == "draw" else (244, 67, 54))
    title_surf = font_title.render(text, True, title_color)
    screen.blit(title_surf, (popup_x + (popup_width - title_surf.get_width()) // 2, y_offset))
    y_offset += 60
    
    # Stats
    stats_text = f"Total Moves: {total_moves}"
    stats_surf = font_subtitle.render(stats_text, True, TEXT_GRAY)
    screen.blit(stats_surf, (popup_x + 30, y_offset))
    y_offset += 40
    
    # PGN Section
    pgn_label = font_subtitle.render("Game Notation (PGN):", True, TEXT_COLOR)
    screen.blit(pgn_label, (popup_x + 30, y_offset))
    y_offset += 30
    
    # PGN box
    pgn_box_rect = p.Rect(popup_x + 30, y_offset, popup_width - 60, 200)
    p.draw.rect(screen, BG_COLOR, pgn_box_rect, border_radius=8)
    p.draw.rect(screen, TEXT_GRAY, pgn_box_rect, 1, border_radius=8)
    
    # Wrap PGN text
    pgn_lines = wrap_text(pgn, font_pgn, popup_width - 80)
    pgn_y = y_offset + 10
    for line in pgn_lines[:8]:  # Show first 8 lines
        pgn_surf = font_pgn.render(line, True, TEXT_COLOR)
        screen.blit(pgn_surf, (popup_x + 40, pgn_y))
        pgn_y += 22
    
    y_offset += 220
    
    # Buttons
    mouse_pos = p.mouse.get_pos()
    
    new_game_rect = p.Rect(popup_x + 50, y_offset, 250, 50)
    quit_rect = p.Rect(popup_x + popup_width - 300, y_offset, 250, 50)
    
    # New Game button
    new_game_color = BUTTON_HOVER if new_game_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    p.draw.rect(screen, new_game_color, new_game_rect, border_radius=8)
    new_game_text = font_button.render("New Game", True, TEXT_COLOR)
    screen.blit(new_game_text, (new_game_rect.centerx - new_game_text.get_width() // 2, new_game_rect.centery - new_game_text.get_height() // 2))
    
    # Quit button
    quit_color = BUTTON_HOVER if quit_rect.collidepoint(mouse_pos) else BUTTON_DISABLED
    p.draw.rect(screen, quit_color, quit_rect, border_radius=8)
    quit_text = font_button.render("Exit to Desktop", True, TEXT_COLOR)
    screen.blit(quit_text, (quit_rect.centerx - quit_text.get_width() // 2, quit_rect.centery - quit_text.get_height() // 2))
    
    # Check for clicks
    for event in p.event.get():
        if event.type == p.QUIT:
            return "quit"
        elif event.type == p.MOUSEBUTTONDOWN:
            if new_game_rect.collidepoint(event.pos):
                return "new_game"
            elif quit_rect.collidepoint(event.pos):
                return "quit"
    
    return None

def wrap_text(text, font, max_width):
    """Wrap text to fit within max_width"""
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line.strip())
            current_line = word + " "
    
    if current_line:
        lines.append(current_line.strip())
    
    return lines


# ═══════════════════════════════════════════════════════════════
# COORDINATE CONVERSION
# ═══════════════════════════════════════════════════════════════

def get_square_from_pos(x, y):
    """Convert pixel position to (col, row)"""
    col = x // SQ_SIZE
    row = y // SQ_SIZE
    
    if board_flipped:
        col = 7 - col
        row = 7 - row
    
    return (col, row)

def get_pos_from_square(row, col):
    """Convert (row, col) to pixel position"""
    if board_flipped:
        display_row = 7 - row
        display_col = 7 - col
    else:
        display_row = row
        display_col = col
    
    return (display_col * SQ_SIZE, display_row * SQ_SIZE)


# ═══════════════════════════════════════════════════════════════
# REPLAY NAVIGATION
# ═══════════════════════════════════════════════════════════════

def navigate_replay(gs, direction):
    """Navigate through move history"""
    global game_mode, replay_index
    
    if len(gs.moveLog) == 0:
        return
    
    if direction == "start":
        game_mode = "replay"
        replay_index = 0
    elif direction == "end":
        game_mode = "play"
        replay_index = -1
    elif direction == "prev":
        if game_mode == "play":
            game_mode = "replay"
            replay_index = len(gs.moveLog) - 1
        elif replay_index > 0:
            replay_index -= 1
    elif direction == "next":
        if game_mode == "replay":
            if replay_index < len(gs.moveLog) - 1:
                replay_index += 1
            else:
                game_mode = "play"
                replay_index = -1

def get_replay_board(gs):
    """Get board state at replay_index"""
    if game_mode != "replay" or replay_index == -1:
        return gs.board
    
    temp_gs = ChessEngine.GameState()
    for i in range(replay_index + 1):
        if i < len(gs.moveLog):
            temp_gs.makeMove(gs.moveLog[i])
    
    return temp_gs.board


# ═══════════════════════════════════════════════════════════════
# SIDEBAR HANDLING - FIXED: No gamestate change on move log click
# ═══════════════════════════════════════════════════════════════

def handle_sidebar_click(x, y, gs, db, game_id, session, validMoves, game_is_active):
    """
    Handle sidebar clicks.
    Returns: None, "quit", "new_game", "logout", or "resigned"
    """
    global game_mode, replay_index, board_flipped
    
    # Button positions
    button_x = BOARD_SIZE + 20
    button_width = SIDEBAR_WIDTH - 40
    button_height = 40
    button_spacing = 10
    start_y = 20
    
    buttons = [
        ("Undo Move", start_y),
        ("New Game", start_y + button_height + button_spacing),
        ("Resign", start_y + 2 * (button_height + button_spacing)),
        ("Flip Board", start_y + 3 * (button_height + button_spacing)),
        ("Logout", start_y + 4 * (button_height + button_spacing)),
    ]
    
    for label, btn_y in buttons:
        btn_rect = p.Rect(button_x, btn_y, button_width, button_height)
        
        if btn_rect.collidepoint(x, y):
            # Ignore all buttons if game is finished
            if game_mode == "finished" and label not in ["New Game", "Logout"]:
                return None
            
            if label == "Undo Move":
                try_undo_move(gs, validMoves, game_is_active)
            
            elif label == "New Game":
                # Check if current game is active
                if game_is_active and len(gs.moveLog) > 0:
                    # Show confirmation dialog
                    if show_confirmation_dialog("Start a new game? Current game will be resigned."):
                        # Resign current game
                        moves_string = generate_pgn_string(gs)
                        result = 'resign'
                        db.end_game(game_id, result, moves_string, len(gs.moveLog))
                        return "new_game"
                else:
                    return "new_game"
            
            elif label == "Resign":
                if game_is_active:
                    # Save game as resigned
                    moves_string = generate_pgn_string(gs)
                    result = 'loss' if player_color == "white" else 'win'
                    db.end_game(game_id, result, moves_string, len(gs.moveLog))
                    return "resigned"
            
            elif label == "Flip Board":
                board_flipped = not board_flipped
            
            elif label == "Logout":
                # Confirm logout
                if show_confirmation_dialog("Logout? Current game will be resigned."):
                    if game_is_active and len(gs.moveLog) > 0:
                        moves_string = generate_pgn_string(gs)
                        result = 'resign'
                        db.end_game(game_id, result, moves_string, len(gs.moveLog))
                    return "logout"
            
            return None
    
    # REMOVED: Move log click navigation (now only scrolling)
    # The move log area is now ONLY for scrolling, not for navigation
    
    return None


def try_undo_move(gs, validMoves, game_is_active):
    """Run the existing sidebar undo behavior and report if it succeeded."""
    if game_mode == "play" and len(gs.moveLog) >= 2 and game_is_active:
        gs.undoMove()
        gs.undoMove()
        validMoves.clear()
        validMoves.extend(gs.getValidMoves())
        return True
    return False


def show_confirmation_dialog(message):
    """Show a simple confirmation dialog"""
    # Create a simple overlay
    screen = p.display.get_surface()
    overlay = p.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Dialog box
    dialog_width = 500
    dialog_height = 200
    dialog_x = (WINDOW_WIDTH - dialog_width) // 2
    dialog_y = (WINDOW_HEIGHT - dialog_height) // 2
    
    dialog_rect = p.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
    p.draw.rect(screen, PANEL_COLOR, dialog_rect, border_radius=15)
    p.draw.rect(screen, BUTTON_COLOR, dialog_rect, 3, border_radius=15)
    
    # Message
    font = p.font.SysFont("Arial", 20)
    msg_lines = message.split('\n')
    y_offset = dialog_y + 40
    for line in msg_lines:
        msg_surf = font.render(line, True, TEXT_COLOR)
        screen.blit(msg_surf, (dialog_x + (dialog_width - msg_surf.get_width()) // 2, y_offset))
        y_offset += 30
    
    # Buttons
    yes_rect = p.Rect(dialog_x + 50, dialog_y + 130, 180, 50)
    no_rect = p.Rect(dialog_x + dialog_width - 230, dialog_y + 130, 180, 50)
    
    while True:
        mouse_pos = p.mouse.get_pos()
        
        # Yes button
        yes_color = BUTTON_HOVER if yes_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        p.draw.rect(screen, yes_color, yes_rect, border_radius=8)
        yes_text = font.render("Yes", True, TEXT_COLOR)
        screen.blit(yes_text, (yes_rect.centerx - yes_text.get_width() // 2, yes_rect.centery - yes_text.get_height() // 2))
        
        # No button
        no_color = BUTTON_HOVER if no_rect.collidepoint(mouse_pos) else BUTTON_DISABLED
        p.draw.rect(screen, no_color, no_rect, border_radius=8)
        no_text = font.render("No", True, TEXT_COLOR)
        screen.blit(no_text, (no_rect.centerx - no_text.get_width() // 2, no_rect.centery - no_text.get_height() // 2))
        
        p.display.flip()
        
        for event in p.event.get():
            if event.type == p.QUIT:
                return False
            elif event.type == p.MOUSEBUTTONDOWN:
                if yes_rect.collidepoint(event.pos):
                    return True
                elif no_rect.collidepoint(event.pos):
                    return False


# ═══════════════════════════════════════════════════════════════
# RENDERING
# ═══════════════════════════════════════════════════════════════

def drawGameState(screen, gs, validMoves, sqSelected):
    """Main rendering"""
    screen.fill(BG_COLOR)
    
    board = get_replay_board(gs)
    
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected, board)
    drawPieces(screen, board)
    drawSidebar(screen, gs)
    
    if game_mode == "replay":
        drawReplayIndicator(screen, gs)

def drawBoard(screen):
    """Draw chess board"""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = LIGHT_SQ if (r + c) % 2 == 0 else DARK_SQ
            x, y = get_pos_from_square(r, c)
            p.draw.rect(screen, color, p.Rect(x, y, SQ_SIZE, SQ_SIZE))

def highlightSquares(screen, gs, validMoves, sqSelected, board):
    """Highlight squares"""
    # Only highlight in play mode
    if game_mode != "play":
        return
    
    # Last move
    if len(gs.moveLog) > 0:
        last_move = gs.moveLog[-1]
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(128)
        s.fill(HIGHLIGHT_LAST_MOVE[:3])
        
        for r, c in [(last_move.startRow, last_move.startCol), (last_move.endRow, last_move.endCol)]:
            x, y = get_pos_from_square(r, c)
            screen.blit(s, (x, y))
    
    # Selected square
    if sqSelected != ():
        r, c = sqSelected
        if board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(128)
            s.fill(HIGHLIGHT_SELECTED[:3])
            
            x, y = get_pos_from_square(r, c)
            screen.blit(s, (x, y))
            
            # Valid moves
            s.fill((255, 255, 0))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    x, y = get_pos_from_square(move.endRow, move.endCol)
                    screen.blit(s, (x, y))

def drawPieces(screen, board):
    """Draw pieces"""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                x, y = get_pos_from_square(r, c)
                screen.blit(IMAGES[piece], p.Rect(x, y, SQ_SIZE, SQ_SIZE))

def drawSidebar(screen, gs):
    """Draw sidebar"""
    global move_list_max_scroll
    
    sidebar_rect = p.Rect(BOARD_SIZE, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
    p.draw.rect(screen, PANEL_COLOR, sidebar_rect)
    
    font_button = p.font.SysFont("Arial", 18)
    font_log = p.font.SysFont("Arial", 16)
    
    mouse_pos = p.mouse.get_pos()
    
    # Buttons
    button_x = BOARD_SIZE + 20
    button_width = SIDEBAR_WIDTH - 40
    button_height = 40
    button_spacing = 10
    start_y = 20
    
    buttons = [
        ("Undo Move", start_y),
        ("New Game", start_y + button_height + button_spacing),
        ("Resign", start_y + 2 * (button_height + button_spacing)),
        ("Flip Board", start_y + 3 * (button_height + button_spacing)),
        ("Logout", start_y + 4 * (button_height + button_spacing)),
    ]
    
    for label, btn_y in buttons:
        btn_rect = p.Rect(button_x, btn_y, button_width, button_height)
        is_hover = btn_rect.collidepoint(mouse_pos)
        
        # Disable all buttons if game is finished (except New Game and Logout)
        if game_mode == "finished" and label not in ["New Game", "Logout"]:
            color = BUTTON_DISABLED
        elif label == "Undo Move" and (game_mode == "replay" or len(gs.moveLog) < 2):
            color = BUTTON_DISABLED
        else:
            color = BUTTON_HOVER if is_hover else BUTTON_COLOR
        
        p.draw.rect(screen, color, btn_rect, border_radius=8)
        
        text = font_button.render(label, True, TEXT_COLOR)
        text_rect = text.get_rect(center=btn_rect.center)
        screen.blit(text, text_rect)
    
    # Move log
    log_y = start_y + 5 * (button_height + button_spacing) + 20
    
    title = font_button.render("Move History", True, TEXT_GRAY)
    screen.blit(title, (button_x, log_y))
    log_y += 30
    
    # Info text about arrow keys
    info = p.font.SysFont("Arial", 12).render("Use ← → arrows to navigate", True, TEXT_GRAY)
    screen.blit(info, (button_x, log_y))
    log_y += 20
    
    # Scrollable move log
    move_log_rect = p.Rect(button_x, log_y, button_width, WINDOW_HEIGHT - log_y - 20)
    
    moveLog = gs.moveLog
    line_height = 24
    
    # Calculate max scroll
    total_lines = (len(moveLog) + 1) // 2
    total_height = total_lines * line_height
    visible_height = move_log_rect.height
    move_list_max_scroll = max(0, total_height - visible_height)
    
    # Render moves (with scroll offset)
    y_offset = -move_list_scroll
    
    for i in range(0, len(moveLog), 2):
        move_num_text = f"{i//2 + 1}."
        white_move = moveLog[i].getSAN(gs, is_check=False, is_checkmate=False)
        black_move = ""
        if i + 1 < len(moveLog):
            black_move = moveLog[i+1].getSAN(gs, is_check=False, is_checkmate=False)
        
        # Highlight current replay position
        if game_mode == "replay" and (i <= replay_index < i + 2):
            highlight_rect = p.Rect(button_x, log_y + y_offset, button_width, line_height)
            if highlight_rect.colliderect(move_log_rect):
                p.draw.rect(screen, HIGHLIGHT_COLOR, highlight_rect, border_radius=4)
        
        # Render text (only if visible)
        text_y = log_y + y_offset + 3
        if text_y >= log_y and text_y < log_y + move_log_rect.height:
            move_text = f"{move_num_text} {white_move} {black_move}"
            text = font_log.render(move_text, True, TEXT_COLOR)
            screen.blit(text, (button_x + 5, text_y))
        
        y_offset += line_height

def drawReplayIndicator(screen, gs):
    """Replay mode banner"""
    font = p.font.SysFont("Arial", 20, bold=True)
    
    if replay_index >= 0 and replay_index < len(gs.moveLog):
        move = gs.moveLog[replay_index]
        text = f"◀ REPLAY: Move {replay_index + 1} - {move.getSAN()} ▶"
    else:
        text = "◀ REPLAY: Starting Position ▶"
    
    text_surf = font.render(text, True, (255, 255, 0))
    text_rect = text_surf.get_rect(center=(BOARD_SIZE // 2, 20))
    
    bg_rect = text_rect.inflate(20, 10)
    p.draw.rect(screen, (0, 0, 0), bg_rect, border_radius=8)
    p.draw.rect(screen, (255, 255, 0), bg_rect, 2, border_radius=8)
    
    screen.blit(text_surf, text_rect)

def animateMove(move, screen, board, clock):
    """Animate move"""
    dr = move.endRow - move.startRow
    dc = move.endCol - move.startCol
    framesPerSquare = 8
    frameCount = (abs(dr) + abs(dc)) * framesPerSquare
    
    for frame in range(frameCount + 1):
        r = move.startRow + dr * frame / frameCount
        c = move.startCol + dc * frame / frameCount
        
        drawBoard(screen)
        drawPieces(screen, board)
        
        color = LIGHT_SQ if (move.endRow + move.endCol) % 2 == 0 else DARK_SQ
        end_x, end_y = get_pos_from_square(move.endRow, move.endCol)
        p.draw.rect(screen, color, p.Rect(end_x, end_y, SQ_SIZE, SQ_SIZE))
        
        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                cap_x, cap_y = get_pos_from_square(enPassantRow, move.endCol)
            else:
                cap_x, cap_y = end_x, end_y
            screen.blit(IMAGES[move.pieceCaptured], p.Rect(cap_x, cap_y, SQ_SIZE, SQ_SIZE))
        
        piece_x, piece_y = get_pos_from_square(r, c)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(piece_x, piece_y, SQ_SIZE, SQ_SIZE))
        
        p.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
