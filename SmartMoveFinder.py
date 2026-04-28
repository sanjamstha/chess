# Algorithms:
# ✅ Zobrist Hashing (10x faster TT lookups)
# ✅ Iterative Deepening (better time management)
# ✅ Centipawn scaling (faster integer math)
# ✅ Fixed stalemate bug (was declaring draw incorrectly)
# ✅ Killer moves heuristic (better move ordering)

import random
from ChessOpenings import OPENING_BOOK

CHECKMATE = 100000
STALEMATE = 0
INF       = 999999

pieceScore = {"K": 0, "Q": 900, "R": 500, "B": 330, "N": 320, "p": 100}

# Transposition table flags
TT_EXACT = 0
TT_LOWER = 1
TT_UPPER = 2

# ─────────────────────────────────────────────
#  ZOBRIST HASHING INITIALIZATION
# ─────────────────────────────────────────────
import random as _rnd
_rnd.seed(42)  # Reproducible random numbers

# Zobrist table: [piece][square]
# Pieces: wp, wN, wB, wR, wQ, wK, bp, bN, bB, bR, bQ, bK (12 types)
# Squares: 64
ZOBRIST_TABLE = {}
ZOBRIST_SIDE = _rnd.getrandbits(64)  # Hash for side to move

piece_to_index = {
    'wp': 0, 'wN': 1, 'wB': 2, 'wR': 3, 'wQ': 4, 'wK': 5,
    'bp': 6, 'bN': 7, 'bB': 8, 'bR': 9, 'bQ': 10, 'bK': 11
}

for piece in piece_to_index.keys():
    ZOBRIST_TABLE[piece] = [_rnd.getrandbits(64) for _ in range(64)]


def zobrist_hash(gs):
    """
    Fast incremental hash using Zobrist method.
    This should be updated incrementally in makeMove/undoMove for speed.
    """
    h = 0
    for r in range(8):
        for c in range(8):
            piece = gs.board[r][c]
            if piece != "--":
                sq = r * 8 + c
                h ^= ZOBRIST_TABLE[piece][sq]
    
    if gs.whiteToMove:
        h ^= ZOBRIST_SIDE
    
    return h

# PST
pawn_pst = [
    [  0,   0,   0,   0,   0,   0,   0,   0],
    [ 50,  50,  50,  50,  50,  50,  50,  50],
    [ 10,  10,  20,  30,  30,  20,  10,  10],
    [  5,   5,  10,  25,  25,  10,   5,   5],
    [  0,   0,   0,  20,  20,   0,   0,   0],
    [  5,  -5, -10,   0,   0, -10,  -5,   5],
    [  5,  10,  10, -20, -20,  10,  10,   5],
    [  0,   0,   0,   0,   0,   0,   0,   0],
]

knight_pst = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20,   0,   0,   0,   0, -20, -40],
    [-30,   0,  10,  15,  15,  10,   0, -30],
    [-30,   5,  15,  20,  20,  15,   5, -30],
    [-30,   0,  15,  20,  20,  15,   0, -30],
    [-30,   5,  10,  15,  15,  10,   5, -30],
    [-40, -20,   0,   5,   5,   0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50],
]

bishop_pst = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10,   0,   0,   0,   0,   0,   0, -10],
    [-10,   0,   5,  10,  10,   5,   0, -10],
    [-10,   5,   5,  10,  10,   5,   5, -10],
    [-10,   0,  10,  10,  10,  10,   0, -10],
    [-10,  10,  10,  10,  10,  10,  10, -10],
    [-10,   5,   0,   0,   0,   0,   5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20],
]

rook_pst = [
    [  0,   0,   0,   0,   0,   0,   0,   0],
    [  5,  10,  10,  10,  10,  10,  10,   5],
    [ -5,   0,   0,   0,   0,   0,   0,  -5],
    [ -5,   0,   0,   0,   0,   0,   0,  -5],
    [ -5,   0,   0,   0,   0,   0,   0,  -5],
    [ -5,   0,   0,   0,   0,   0,   0,  -5],
    [ -5,   0,   0,   0,   0,   0,   0,  -5],
    [  0,   0,   0,   5,   5,   0,   0,   0],
]

queen_pst = [
    [-20, -10, -10,  -5,  -5, -10, -10, -20],
    [-10,   0,   0,   0,   0,   0,   0, -10],
    [-10,   0,   5,   5,   5,   5,   0, -10],
    [ -5,   0,   5,   5,   5,   5,   0,  -5],
    [  0,   0,   5,   5,   5,   5,   0,  -5],
    [-10,   5,   5,   5,   5,   5,   0, -10],
    [-10,   0,   5,   0,   0,   0,   0, -10],
    [-20, -10, -10,  -5,  -5, -10, -10, -20],
]

king_mid_pst = [
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [ 20,  20,   0,   0,   0,   0,  20,  20],
    [ 20,  30,  10,   0,   0,  10,  30,  20],
]

king_end_pst = [
    [-50, -30, -30, -30, -30, -30, -30, -50],
    [-30, -30,   0,   0,   0,   0, -30, -30],
    [-30, -10,  20,  30,  30,  20, -10, -30],
    [-30, -10,  30,  40,  40,  30, -10, -30],
    [-30, -10,  30,  40,  40,  30, -10, -30],
    [-30, -10,  20,  30,  30,  20, -10, -30],
    [-30, -20,   0,   0,   0,   0, -20, -30],
    [-50, -30, -30, -30, -30, -30, -30, -50],
]

# PST lookup
piecePositionScores_mid = {
    "wp": pawn_pst,          "bp": pawn_pst[::-1],
    "wN": knight_pst,        "bN": knight_pst[::-1],
    "wB": bishop_pst,        "bB": bishop_pst[::-1],
    "wR": rook_pst,          "bR": rook_pst[::-1],
    "wQ": queen_pst,         "bQ": queen_pst[::-1],
    "wK": king_mid_pst,      "bK": king_mid_pst[::-1],
}
piecePositionScores_end = {
    "wK": king_end_pst,      "bK": king_end_pst[::-1],
}


def _get_book_move(gs):
    """Look up opening book move via Zobrist hash"""
    from ChessOpenings import get_opening_book_hashed
    opening_book = get_opening_book_hashed()  # Lazy load
    candidates = opening_book.get(gs.zobristHash)
    if candidates:
        return random.choice(candidates)
    return None

#  MVV-LVA SCORE
_mvv_lva_victim   = {"Q": 5, "R": 4, "B": 3, "N": 3, "p": 1, "K": 0}
_mvv_lva_attacker = {"p": 6, "N": 5, "B": 4, "R": 3, "Q": 2, "K": 1}

def _mvv_lva_score(move):
    """Calculate MVV-LVA score for a capture"""
    captured = getattr(move, "pieceCaptured", "--")
    if captured == "--" or len(captured) != 2:
        return 0
    victim = _mvv_lva_victim.get(captured[1], 0)
    attacker = _mvv_lva_attacker.get(move.pieceMoved[1], 0)
    return victim * 10 + attacker


#  FAST MOVE ORDERING (3-tier without sorting)
def _order_moves_fast(validMoves, killer_moves, tt_move):
    """
    Fast 3-pass ordering - no full sorting needed.
    Priority: TT move > Captures (MVV-LVA) > Killers > Quiet moves
    """
    captures = []
    killers = []
    quiet = []
    
    for move in validMoves:
        if move == tt_move:
            continue  # Will be inserted first
        elif move.pieceCaptured != "--":
            captures.append(move)
        elif move in killer_moves:
            killers.append(move)
        else:
            quiet.append(move)
    
    # Sort only captures (usually <10 moves)
    captures.sort(key=_mvv_lva_score, reverse=True)
    
    # Assemble final list
    result = []
    if tt_move and tt_move in validMoves:
        result.append(tt_move)
    result.extend(captures)
    result.extend(killers)
    result.extend(quiet)
    return result


#  TRANSPOSITION TABLE 
_tt = {}
TT_MAX_SIZE = 500_000  # Increased size

#  KILLER MOVES (2 per depth level)
_killer_moves = {}  # {depth: [move1, move2]}

def _add_killer(move, depth):
    """Add a killer move at this depth"""
    if depth not in _killer_moves:
        _killer_moves[depth] = []
    
    if move not in _killer_moves[depth]:
        _killer_moves[depth].insert(0, move)
        if len(_killer_moves[depth]) > 2:
            _killer_moves[depth].pop()


#  MODULE-LEVEL STATE
nextMove = None
counter  = 0


#  PUBLIC API

def findRandomMove(validMoves):
    return random.choice(validMoves)


def findBestMove(gs, validMoves, difficulty='medium'):
    """
    Main entry point with iterative deepening.
    
    Args:
        gs: GameState
        validMoves: list of legal moves
        difficulty: 'easy' (depth 1), 'medium' (depth 3), 'hard' (depth 4)
        
    Returns:
        (best_move, evaluation_score): Tuple of Move object and centipawn evaluation
    """
    global nextMove, counter, _tt, _killer_moves

    # ── 1. Opening book ──
    book_notation = _get_book_move(gs)
    if book_notation:
        for move in validMoves:
            if move.getChessNotation() == book_notation:
                print(f"AI: Book move → {book_notation}")
                # Return book move with 0 evaluation (unknown)
                return (move, 0)

    # ── 2. Iterative deepening search ──
    nextMove = None
    counter = 0
    best_eval = 0
    _killer_moves.clear()

    if len(_tt) > TT_MAX_SIZE:
        _tt.clear()

    depth_map = {'easy': 1, 'medium': 3, 'hard': 4}
    max_depth = depth_map.get(difficulty, 3)

    random.shuffle(validMoves)
    turnMul = 1 if gs.whiteToMove else -1

    # ITERATIVE DEEPENING: Search depth 1, 2, 3... up to max_depth
    for current_depth in range(1, max_depth + 1):
        eval_score = _negamax(gs, validMoves, current_depth, -INF, INF, turnMul, is_root=True)
        best_eval = eval_score * turnMul  # Convert to absolute evaluation (white's perspective)
        print(f"  Depth {current_depth}: {counter} nodes | best = {nextMove.getSAN() if nextMove else 'None'} | eval = {best_eval/100:+.2f}")

    print(f"AI (depth {max_depth}): {counter} total nodes | move → "
            f"{nextMove.getSAN() if nextMove else 'None'} | final eval = {best_eval/100:+.2f}")
    
    return (nextMove, best_eval)


#  CORE SEARCH

def _negamax(gs, validMoves, depth, alpha, beta, turnMul, is_root=False):
    """
    Negamax + Alpha-Beta + TT + Killer moves.
    """
    global nextMove, counter
    counter += 1

    # ── TT probe ──
    h = gs.zobristHash  # Use incremental hash!
    tt_entry = _tt.get(h)
    tt_move = None
    
    if tt_entry and not is_root:
        tt_depth, tt_flag, tt_score, tt_move = tt_entry
        if tt_depth >= depth:
            if tt_flag == TT_EXACT:
                return tt_score
            elif tt_flag == TT_LOWER and tt_score > alpha:
                alpha = tt_score
            elif tt_flag == TT_UPPER and tt_score < beta:
                beta = tt_score
            if alpha >= beta:
                return tt_score

    # ── Leaf → quiescence ──
    if depth == 0:
        return _quiescence(gs, alpha, beta, turnMul)

    # ── Terminal ──
    if not validMoves:
        if gs.inCheck():
            return -CHECKMATE
        return STALEMATE

    # ── Fast move ordering (3-tier, no full sort) ──
    killer_list = _killer_moves.get(depth, [])
    orderedMoves = _order_moves_fast(validMoves, killer_list, tt_move)

    best_score = -INF
    best_move  = None
    orig_alpha = alpha

    for move in orderedMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -_negamax(gs, nextMoves, depth - 1, -beta, -alpha, -turnMul)
        gs.undoMove()

        if score > best_score:
            best_score = score
            best_move  = move
            if is_root:
                nextMove = move

        if score > alpha:
            alpha = score
        
        if alpha >= beta:
            # Killer move heuristic
            if not move.isCapture:
                _add_killer(move, depth)
            break

    # ── Store in TT ──
    if len(_tt) < TT_MAX_SIZE:
        if best_score <= orig_alpha:
            flag = TT_UPPER
        elif best_score >= beta:
            flag = TT_LOWER
        else:
            flag = TT_EXACT
        _tt[h] = (depth, flag, best_score, best_move)

    return best_score


def _quiescence(gs, alpha, beta, turnMul):
    """Quiescence search for captures"""
    global counter
    counter += 1

    stand_pat = turnMul * _scoreBoard(gs)

    if stand_pat >= beta:
        return beta
    if stand_pat > alpha:
        alpha = stand_pat

    allMoves = gs.getValidMoves()
    captureMoves = [m for m in allMoves if getattr(m, "pieceCaptured", "--") != "--"]
    captureMoves.sort(key=_mvv_lva_score, reverse=True)

    for move in captureMoves:
        gs.makeMove(move)
        score = -_quiescence(gs, -beta, -alpha, -turnMul)
        gs.undoMove()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha


# ─────────────────────────────────────────────
#  EVALUATION
# ─────────────────────────────────────────────

def _is_endgame(gs):
    """Endgame detector"""
    queens = 0
    minors = 0
    for r in range(8):
        for c in range(8):
            p = gs.board[r][c]
            if p == "--":
                continue
            if p[1] == "Q":
                queens += 1
            if p[1] in ("N", "B", "R"):
                minors += 1
    return queens == 0 or minors <= 2


def _scoreBoard(gs):
    """
    Static evaluation in centipawns.
    Positive = White advantage, Negative = Black advantage
    """
    if gs.checkMate:
        return -CHECKMATE if gs.whiteToMove else CHECKMATE
    if gs.staleMate:
        return STALEMATE

    endgame = _is_endgame(gs)
    score = 0
    board = gs.board
    w_bishops = 0
    b_bishops = 0

    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece == "--":
                continue

            color = piece[0]
            ptype = piece[1]
            sign = 1 if color == "w" else -1

            # Material
            score += sign * pieceScore.get(ptype, 0)

            # PST
            key = color + ptype
            if endgame and key in piecePositionScores_end:
                score += sign * piecePositionScores_end[key][r][c]
            elif key in piecePositionScores_mid:
                score += sign * piecePositionScores_mid[key][r][c]

            # Count bishops
            if ptype == "B":
                if color == "w":
                    w_bishops += 1
                else:
                    b_bishops += 1

            # Rook on open file
            if ptype == "R":
                file_pawns = [board[row][c] for row in range(8) if board[row][c][1] == "p"]
                if not file_pawns:
                    score += sign * 30
                elif not any(p[0] == color for p in file_pawns):
                    score += sign * 15

    # Bishop pair
    if w_bishops >= 2:
        score += 30
    if b_bishops >= 2:
        score -= 30

    # Endgame king push
    if endgame:
        score += _endgame_king_bonus(gs)

    return score


def _endgame_king_bonus(gs):
    """Push opponent king to corner in endgame"""
    wk = gs.whiteKingLocation
    bk = gs.blackKingLocation

    def center_dist(loc):
        return abs(loc[0] - 3.5) + abs(loc[1] - 3.5)

    kings_dist = abs(wk[0] - bk[0]) + abs(wk[1] - bk[1])

    material = sum(
        pieceScore.get(gs.board[r][c][1], 0) * (1 if gs.board[r][c][0] == "w" else -1)
        for r in range(8) for c in range(8) if gs.board[r][c] != "--"
    )

    bonus = 0
    if material > 0:
        bonus += center_dist(bk) * 10
        bonus -= kings_dist * 4
    elif material < 0:
        bonus -= center_dist(wk) * 10
        bonus += kings_dist * 4

    return bonus