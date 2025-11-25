import random

pieceScore = {"K":0, "Q":9, "R":5, "B":3, "N":3, "p":1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

# Piece Square Tables
pawn_pst = [
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [ 0.2,  0.3,  0.3, -0.1, -0.1,  0.3,  0.3,  0.2],
    [ 0.2,  0.1,  0.0,  0.1,  0.1,  0.0,  0.1,  0.2],
    [ 0.3,  0.3,  0.3,  0.4,  0.4,  0.3,  0.3,  0.3],
    [ 0.4,  0.4,  0.4,  0.5,  0.5,  0.4,  0.4,  0.4],
    [ 0.5,  0.5,  0.5,  0.6,  0.6,  0.5,  0.5,  0.5],
    [ 0.7,  0.7,  0.7,  0.7,  0.7,  0.7,  0.7,  0.7],
    [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
]
knight_pst = [
    [-0.8, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.8],
    [-0.4, -0.2,  0.1,  0.2,  0.2,  0.1, -0.2, -0.4],
    [-0.3,  0.2,  0.3,  0.35, 0.35, 0.3,  0.2, -0.3],
    [-0.3,  0.1,  0.35, 0.45, 0.45, 0.35, 0.1, -0.3],
    [-0.3,  0.1,  0.35, 0.45, 0.45, 0.35, 0.1, -0.3],
    [-0.3,  0.2,  0.3,  0.35, 0.35, 0.3,  0.2, -0.3],
    [-0.4, -0.2,  0.1,  0.2,  0.2,  0.1, -0.2, -0.4],
    [-0.8, -0.4, -0.3, -0.3, -0.3, -0.3, -0.4, -0.8]
]
bishop_pst = [
    [-0.2, -0.1, -0.1, -0.05, -0.05, -0.1, -0.1, -0.2],
    [-0.1,  0.1,  0.15, 0.1,  0.1,  0.15, 0.1, -0.1],
    [-0.1,  0.15, 0.2,  0.2,  0.2,  0.2,  0.15, -0.1],
    [-0.05, 0.1,  0.2,  0.25, 0.25, 0.2,  0.1, -0.05],
    [-0.05, 0.1,  0.2,  0.25, 0.25, 0.2,  0.1, -0.05],
    [-0.1,  0.15, 0.2,  0.2,  0.2,  0.2,  0.15, -0.1],
    [-0.1,  0.1,  0.15, 0.1,  0.1,  0.15, 0.1, -0.1],
    [-0.2, -0.1, -0.1, -0.05, -0.05, -0.1, -0.1, -0.2]
]
rook_pst = [
    [ 0.0,  0.0,  0.05, 0.1,  0.1,  0.05, 0.0,  0.0 ],
    [-0.1, -0.05, 0.0,  0.05, 0.05, 0.0, -0.05, -0.1],
    [-0.1,  0.0,  0.05, 0.1,  0.1,  0.05, 0.0, -0.1 ],
    [-0.1,  0.0,  0.05, 0.1,  0.1,  0.05, 0.0, -0.1 ],
    [-0.1,  0.0,  0.05, 0.1,  0.1,  0.05, 0.0, -0.1 ],
    [-0.1,  0.0,  0.05, 0.1,  0.1,  0.05, 0.0, -0.1 ],
    [ 0.2,  0.25, 0.25, 0.3,  0.3,  0.25, 0.25, 0.2 ],
    [ 0.0,  0.0,  0.05, 0.1,  0.1,  0.05, 0.0,  0.0 ]
]
queen_pst = [
    [-0.2, -0.1, -0.1, -0.05, -0.05, -0.1, -0.1, -0.2],
    [-0.1,  0.0,  0.1,  0.05,  0.05,  0.1,  0.0, -0.1],
    [-0.1,  0.1,  0.15, 0.1,   0.1,  0.15, 0.1, -0.1],
    [-0.05, 0.05, 0.1,  0.15,  0.15, 0.1,  0.05, -0.05],
    [-0.05, 0.05, 0.1,  0.15,  0.15, 0.1,  0.05, -0.05],
    [-0.1,  0.1,  0.15, 0.1,   0.1,  0.15, 0.1, -0.1],
    [-0.1,  0.0,  0.1,  0.05,  0.05,  0.1, 0.0, -0.1],
    [-0.2, -0.1, -0.1, -0.05, -0.05, -0.1, -0.1, -0.2]
]
king_mid_pst = [
    [-0.5, -0.6, -0.6, -0.7, -0.7, -0.6, -0.6, -0.5],
    [-0.5, -0.6, -0.6, -0.7, -0.7, -0.6, -0.6, -0.5],
    [-0.5, -0.6, -0.6, -0.7, -0.7, -0.6, -0.6, -0.5],
    [-0.5, -0.6, -0.6, -0.7, -0.7, -0.6, -0.6, -0.5],
    [-0.3, -0.4, -0.4, -0.5, -0.5, -0.4, -0.4, -0.3],
    [-0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2],
    [ 0.1,  0.2,  0.0,  0.0,  0.0,  0.0,  0.2,  0.1],
    [ 0.2,  0.3,  0.1,  0.0,  0.0,  0.1,  0.3,  0.2]
]
king_end_pst = [
    [-0.2, -0.1,  0.0,  0.1,  0.1,  0.0, -0.1, -0.2],
    [-0.1,  0.0,  0.1,  0.2,  0.2,  0.1,  0.0, -0.1],
    [ 0.0,  0.1,  0.2,  0.3,  0.3,  0.2,  0.1,  0.0],
    [ 0.1,  0.2,  0.3,  0.4,  0.4,  0.3,  0.2,  0.1],
    [ 0.1,  0.2,  0.3,  0.4,  0.4,  0.3,  0.2,  0.1],
    [ 0.0,  0.1,  0.2,  0.3,  0.3,  0.2,  0.1,  0.0],
    [-0.1,  0.0,  0.1,  0.2,  0.2,  0.1,  0.0, -0.1],
    [-0.2, -0.1,  0.0,  0.1,  0.1,  0.0, -0.1, -0.2]
]

piecePositionScores = {
    "p": pawn_pst,
    "B": bishop_pst,
    "N": knight_pst,
    "R": rook_pst,
    "Q": queen_pst,
    "K": king_mid_pst,
}

piecePositionScores_alt = {
    "wp": pawn_pst,
    "bp": pawn_pst[::-1],  # flipped for black
    
    "wN": knight_pst,
    "bN": knight_pst[::-1],

    "wB": bishop_pst,
    "bB": bishop_pst[::-1],

    "wR": rook_pst,
    "bR": rook_pst[::-1],

    "wQ": queen_pst,
    "bQ": queen_pst[::-1],

    "wK": king_mid_pst,
    "bK": king_mid_pst[::-1],
}

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

# Greedy ALgorithm
# def greedyMove(gs, validMoves):
#     turnMultiplier = 1 if gs.whiteToMove else -1
#     maxScore = -CHECKMATE
#     bestMove = None
#     for playerMove in validMoves:
#         gs.makeMove(playerMove)
#         if gs.checkMate:
#             score = -CHECKMATE
#         elif gs.staleMate:
#             score = STALEMATE
#         else:
#             score = turnMultiplier * scoreMaterial(gs.board)
#         if score > maxScore:
#             maxScore = score
#             bestMove = playerMove
#         gs.undoMove()
#     return bestMove

# MinMax Algorithm with no recursion 
# def findMoveMinMaxNoRecursion(gs, validMoves):
#     turnMultiplier = 1 if gs.whiteToMove else -1
#     opponentMinMaxScore = CHECKMATE
#     bestPlayerMove = None
#     random.shuffle(validMoves)
#     for playerMove in validMoves:
#         gs.makeMove(playerMove)
#         opponentsMoves = gs.getValidMoves()
#         if gs.staleMate:
#             opponentMaxScore = STALEMATE
#         elif gs.checkMate:
#             opponentMaxScore = -CHECKMATE
#         else:
#             opponentMaxScore = -CHECKMATE
#             for opponentsMove in opponentsMoves:
#                 gs.makeMove(opponentsMove)
#                 if gs.checkMate:
#                     score = CHECKMATE
#                 elif gs.staleMate:
#                     score = STALEMATE
#                 else:
#                     score = -turnMultiplier * scoreMaterial(gs.board)
#                 if score > opponentMaxScore:
#                     opponentMaxScore = score
#                 gs.undoMove()
#         if opponentMaxScore < opponentMinMaxScore:
#             opponentMinMaxScore = opponentMaxScore
#             bestPlayerMove = playerMove
#         gs.undoMove()
#     return bestPlayerMove

'''
Helper method to make the first recursive call
'''
def findBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    # findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
    return nextMove

# MinMax Algorithm
def findMoveMinMax(gs, validMoves, depth, maximizingPlayer):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return scoreBoard(gs)
    
    if maximizingPlayer:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

# NegaMax Algorithm 
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # move ordering - checks, captures, attacks (implement later)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

# NegaMax Algorithm with Alpha Beta Pruning
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # move ordering - checks, captures, attacks (implement later)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                # print(move, score)
        gs.undoMove()
        if maxScore > alpha: #pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

'''
A positive score is good for white, negative score is good for black
'''
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE #black wins
        else:
            return CHECKMATE #white wins
    elif gs.staleMate:
        return STALEMATE
    
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            piece = gs.board[row][col]
            if piece != "--":
                # score it positionally
                piecePositionScore = 0
                if piece[1] == "N":
                    piecePositionScore = piecePositionScores["N"][row][col]

                
                # Material Score
                if piece[0] == 'w':
                    score += pieceScore[piece[1]] + piecePositionScore
                elif piece[0] == 'b':
                    score -= pieceScore[piece[1]] + piecePositionScore

                # Piece-Square bonus
                # pst = piecePositionScores[piece]  # piece is like "wp", "bN", etc.
                # score += pst[row][col]  # use row and col, not r and c
                
                # Piece-Square bonus
                # pst = piecePositionScores[piece]
                # if piece[0] == 'w':
                #     score += pst[r][c]
                # else:
                #     score -= pst[r][c]
    return score

# '''
# Score the board based on material
# '''
# def scoreMaterial(board):
#     score = 0
#     for row in board:
#         for square in row:
#             if square[0] == 'w':
#                 score += pieceScore[square[1]]
#             elif square[0] == 'b':
#                 score -= pieceScore[square[1]]
#     return score
