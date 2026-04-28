# responsible for storing all information about current game state. responsible for determining the valid moves at current state. also keep move log
class GameState():
    def __init__(self):
        # board is a 8x8 2d list, each element of the list has 2 characters.
        # the first character represents the color of the piece "b" or "w".
        # the second character represents the chess piece : K,Q,B,N,R,P
        # "--" represents an empty space with no pieces.
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                                'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = () #coordinates for the square where en passant is possible
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRight = castleRights(True, True, True, True)
        self.castleRightsLog = [castleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                            self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]
        
        # ── DRAW TRACKING (50-move rule & threefold repetition) ──
        self.halfMoveClock = 0  # Increments each move, resets on pawn move or capture
        self.positionHistory = []  # List of Zobrist hashes for repetition detection
        self.drawByFiftyMoves = False
        self.drawByRepetition = False
        
        # ── INCREMENTAL ZOBRIST HASH (for fast TT lookups) ──
        self.zobristHash = self._calculate_initial_hash()


    # Takes a move as parameter and executes it ( doesnt work for castling, en-passant, and pawn promotion )
    def makeMove(self, move):
        # ── INCREMENTAL ZOBRIST UPDATE (BEFORE move) ──
        from SmartMoveFinder import ZOBRIST_TABLE, ZOBRIST_SIDE
        
        # XOR out old piece position
        old_sq = move.startRow * 8 + move.startCol
        self.zobristHash ^= ZOBRIST_TABLE[move.pieceMoved][old_sq]
        
        # XOR out captured piece (if any)
        if move.pieceCaptured != "--":
            cap_sq = move.endRow * 8 + move.endCol
            self.zobristHash ^= ZOBRIST_TABLE[move.pieceCaptured][cap_sq]
        
        # ── MAKE THE MOVE ──
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move to undo later or dipsplay game history
        self.whiteToMove = not self.whiteToMove # swap players
        
        # ── 50-MOVE RULE: Reset clock on pawn move or capture ──
        if move.pieceMoved[1] == 'p' or move.isCapture:
            self.halfMoveClock = 0
        else:
            self.halfMoveClock += 1
        
        # update the king's location 
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        
        # pawn promotion
        if move.isPawnPromotion:
            # XOR out pawn, XOR in queen
            promoted_piece = move.pieceMoved[0] + 'Q'
            new_sq = move.endRow * 8 + move.endCol
            self.zobristHash ^= ZOBRIST_TABLE[move.pieceMoved][new_sq]
            self.zobristHash ^= ZOBRIST_TABLE[promoted_piece][new_sq]
            self.board[move.endRow][move.endCol] = promoted_piece
        else:
            # XOR in new piece position (normal move)
            new_sq = move.endRow * 8 + move.endCol
            self.zobristHash ^= ZOBRIST_TABLE[self.board[move.endRow][move.endCol]][new_sq]
        
        # enpassant move
        if move.isEnpassantMove:
            # XOR out the captured pawn on different square
            captured_pawn_row = move.startRow
            captured_pawn_col = move.endCol
            captured_pawn_sq = captured_pawn_row * 8 + captured_pawn_col
            captured_pawn_piece = self.board[captured_pawn_row][captured_pawn_col]
            self.zobristHash ^= ZOBRIST_TABLE[captured_pawn_piece][captured_pawn_sq]
            self.board[captured_pawn_row][captured_pawn_col] = '--' # capturing pawn
        
        #update enpassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: #2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()
        
        # Append to enpassant log
        self.enpassantPossibleLog.append(self.enpassantPossible)

        #castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #kingside castle
                # Move rook
                rook_old_sq = move.endRow * 8 + (move.endCol + 1)
                rook_new_sq = move.endRow * 8 + (move.endCol - 1)
                rook_piece = self.board[move.endRow][move.endCol+1]
                self.zobristHash ^= ZOBRIST_TABLE[rook_piece][rook_old_sq]
                self.zobristHash ^= ZOBRIST_TABLE[rook_piece][rook_new_sq]
                
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] #moves the rook
                self.board[move.endRow][move.endCol+1] = '--' #erase the old rook
            else: #queenside castle
                # Move rook
                rook_old_sq = move.endRow * 8 + (move.endCol - 2)
                rook_new_sq = move.endRow * 8 + (move.endCol + 1)
                rook_piece = self.board[move.endRow][move.endCol-2]
                self.zobristHash ^= ZOBRIST_TABLE[rook_piece][rook_old_sq]
                self.zobristHash ^= ZOBRIST_TABLE[rook_piece][rook_new_sq]
                
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] #moves the rook
                self.board[move.endRow][move.endCol-2] = '--' #erase old rook

        # update castling rights - whenever its a rook / king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(castleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                            self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
        
        # ── TOGGLE SIDE TO MOVE ──
        self.zobristHash ^= ZOBRIST_SIDE
        
        # ── RECORD POSITION FOR THREEFOLD REPETITION ──
        self.positionHistory.append(self.zobristHash)
    
    # Undo the last move made 
    def undoMove(self): 
        if len(self.moveLog) != 0: #make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            
            # ── UNDO 50-MOVE CLOCK ──
            # We need to recalculate it by looking at move history
            # Simple approach: decrement (not perfect but works for undo)
            if self.halfMoveClock > 0:
                self.halfMoveClock -= 1
            
            # ── UNDO POSITION HISTORY (and restore hash) ──
            if len(self.positionHistory) > 0:
                self.positionHistory.pop()
            
            # Restore previous Zobrist hash
            if len(self.positionHistory) > 0:
                self.zobristHash = self.positionHistory[-1]
            else:
                self.zobristHash = self._calculate_initial_hash()
            
            # update the king's location 
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            
            #undo enpassant move
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' #leave landing sqaure blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured #puts the pawn back on the correct square it was captured from
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]
            
            # undo castling rights 
            self.castleRightsLog.pop() #get rid of new castle rights from the move we are undoing
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = castleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            #undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: #kingside
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else: #queenside
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'

            self.checkMate = False
            self.stalemate = False
    
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: #left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False
        # if a rook is captured
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False

    #All moves considering checks
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = castleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                        self.currentCastlingRight.wqs, self.currentCastlingRight.bqs) #copy the current castling rights
        # Naive Algorithm
        # 1. generate all possible moves    
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
            
        # 2. for each move, make the move 
        for i in range(len(moves)-1,-1,-1): #when removing from a list, go backwards
            self.makeMove(moves[i])
            # 3. generate all opponent's moves
            # 4. for each oop's move, see if they attack your king
            self.whiteToMove = not self.whiteToMove #switch turn back bcoz after making move it switches turns
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove #switchback
            self.undoMove()
        if len(moves) == 0: #either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
                print("Game Over by Checkmate!")
            else:
                self.staleMate = True
                print("Game Over by Stalemate!")

        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves
    
    '''
    Determine if the current player is in check
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
    '''
    Determine if the enemy can attack the square (r,c)
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch to oppo's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #square is under attack
                return True
        return False
    
    '''
    Check for 50-move rule draw
    '''
    def checkFiftyMoveRule(self):
        if self.halfMoveClock >= 100:  # 100 half-moves = 50 full moves
            self.drawByFiftyMoves = True
            print("Game Over by Fifty-Move Rule!")
            return True
        return False
    
    '''
    Check for threefold repetition draw
    '''
    def checkThreefoldRepetition(self):
        if len(self.positionHistory) < 3:
            return False
        
        # Current position hash is already in positionHistory
        current_hash = self.zobristHash
        
        # Count occurrences of current position in history
        count = self.positionHistory.count(current_hash)
        
        if count >= 3:
            self.drawByRepetition = True
            print("Game Over by Threefold Repetition!")
            return True
        return False

    # All moves without considering checks
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):     # number of rows 
            for c in range(len(self.board[r])): # number of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) # calls the appropriate move functions based on the piece type
                    # if piece == 'p':
                    #     self.getPawnMoves(r,c, moves)
                    # elif piece == 'R':
                    #     self.getRookMoves(r,c,moves)
        return moves
                    
    # Get all the pawn moves for the pawn located at rol, col and add these moves to the list 
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == "--": #1 sqaure pawn advance
                moves.append(Move((r,c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c),(r-2,c), self.board))
            if c-1 >= 0: # captures to the left
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture
                    moves .append(Move((r,c),(r-1,c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r-1,c-1),self.board, isEnpassantMove=True))

            if c+1 <= 7: # capture to the right
                if self.board[r-1][c+1][0] == 'b': # enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r-1, c+1),self.board, isEnpassantMove=True))


        else:   # black pawn moves
            if self.board[r+1][c] == "--": # 1sq pawn advance
                moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] == "--": # 2sq pawn advance
                    moves.append(Move((r,c),(r+2,c),self.board))

            if c-1 >= 0: # capture to the left
                if self.board[r+1][c-1][0] == 'w': # enemy piece to capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r+1, c-1),self.board, isEnpassantMove=True))

            if c+1 <= 7: # captures to the right 
                if self.board[r+1][c+1][0] == 'w': #enemy piece to capture
                    moves.append(Move((r,c),(r+1,c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r,c),(r+1, c+1),self.board, isEnpassantMove=True))

    # Get all the rook moves for the rook located at rol, col and add these moves to the list 
    def getRookMoves(self, r, c, moves):
        # rook moves in all 4 directions, use for/while loop, stop conditions are 2: edge of board, or piece on square, and if enemy piece its a valid move
        enemyColor = 'b' if self.whiteToMove else 'w'
        
        # (dr, dc) for right, left, down, up
        directions = [
            (0, 1),   # right
            (0, -1),  # left
            (1, 0),   # down
            (-1, 0),  # up
        ]

        for dr, dc in directions:
            step = 1
            while True:
                end_r = r + dr * step
                end_c = c + dc * step

                # edge of board stop
                if not (0 <= end_r <= 7 and 0 <= end_c <= 7):
                    break

                nxtSq = self.board[end_r][end_c]

                if nxtSq == "--":
                    moves.append(Move((r, c), (end_r, end_c), self.board))

                else:
                    if nxtSq[0] == enemyColor:
                        moves.append(Move((r, c), (end_r, end_c), self.board))
                    break

                step += 1

    # Get all the Bishop moves for the bishop located at rol, col and add these moves to the list 
    def getBishopMoves(self,r,c,moves):
        enemyColor = 'b' if self.whiteToMove else 'w'
        directions = [
            (-1,1), # top right
            (1,1), # bottom right
            (-1,-1), # top left
            (1,-1) # bottom left
        ]
        for dr, dc in directions:
            step = 1
            while True:
                end_r = r + dr * step
                end_c = c + dc * step
                if not (0 <= end_r <=7 and 0 <= end_c <=7):
                    break
                nxtSq = self.board[end_r][end_c]
                if nxtSq == "--":
                    moves.append(Move((r,c),(end_r,end_c),self.board))
                else:
                    if nxtSq[0] == enemyColor:
                        moves.append(Move((r, c), (end_r, end_c), self.board))
                    break
                step += 1

    # Get all the queen moves for the queen located at rol, col and add these moves to the list 
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    # Get all the knight moves for the knight located at rol, col and add these moves to the list 
    def getKnightMoves(self,r,c,moves):
        enemyColor = 'b' if self.whiteToMove else 'w'
        directions = [
            (-2,1),
            (-1,2),
            (1,2),
            (2,1),
            (2,-1),
            (1,-2),
            (-1,-2),
            (-2,-1)
        ]
        for dr, dc in directions:
            end_r = r + dr 
            end_c = c + dc 

            if not (0 <= end_r <= 7 and 0 <= end_c <= 7):
                continue
            nxtSq = self.board[end_r][end_c]
            if nxtSq == "--":
                moves.append(Move((r,c),(end_r,end_c),self.board))
            else:
                if nxtSq[0] == enemyColor:
                    moves.append(Move((r,c),(end_r,end_c),self.board))
                continue

    # Get all the king moves for the king located at rol, col and add these moves to the list 
    def getKingMoves(self,r,c,moves):
        enemyColor = 'b' if self.whiteToMove else 'w'

        # 8 directions = rook + bishop
        directions = [
            (-1, 1),   # top right
            (0, 1),    # right
            (1, 1),    # bottom right
            (1, 0),    # down
            (1, -1),   # bottom left
            (0, -1),   # left
            (-1, -1),  # top left
            (-1, 0)    # up
        ]

        for dr, dc in directions:
            end_r = r + dr 
            end_c = c + dc 

            # Stop if outside board
            if not (0 <= end_r <= 7 and 0 <= end_c <= 7):
                continue

            nxtSq = self.board[end_r][end_c]

            if nxtSq == "--":
                # empty square → valid move
                moves.append(Move((r, c), (end_r, end_c), self.board))
            else:
                # capture only if enemy piece
                if nxtSq[0] == enemyColor:
                    moves.append(Move((r, c), (end_r, end_c), self.board))
                continue  # blocked by piece

    '''
    Generate all valid castle moves for king  at (r,c) and add them to the list of moves
    '''
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r,c):
            return #cant castle if we are in check
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(r, c, moves)
    
    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board, isCastleMove=True))

    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r,c-2):
                moves.append(Move((r,c),(r,c-2),self.board, isCastleMove=True))
    
    def _calculate_initial_hash(self):
        """Calculate Zobrist hash for initial board position"""
        from SmartMoveFinder import ZOBRIST_TABLE, ZOBRIST_SIDE
        h = 0
        for r in range(8):
            for c in range(8):
                piece = self.board[r][c]
                if piece != "--":
                    sq = r * 8 + c
                    h ^= ZOBRIST_TABLE[piece][sq]
        
        if self.whiteToMove:
            h ^= ZOBRIST_SIDE
        
        return h

class castleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
    # map keys to value 
    # key: value 
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,"5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d":3,"e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startsq, endsq, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # pawn promotion
        self.isPawnPromotion =  (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7) #alternative for if statement
        #castle move
        self.isCastleMove = isCastleMove
        # en passant
        self.isEnpassantMove =  isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

        self.isCapture = self.pieceCaptured != '--'
        # Move ID 
        self.moveID = self.startRow *1000 + self.startCol *100 + self.endRow*10 + self.endCol
        # print(self.moveID)

    # Overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    # Overriding the str() function
    def __str__(self):
        #castle move
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"
        endSquare = self.getRankFile(self.endRow, self.endCol)
        #pawn moves
        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare
            
            #pawn promotion

        # two of the same type of piece movint to a square
        # also adding + for check move, and '#' for checkmate move

        #piece moves
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += 'x'
        return moveString + endSquare
    
    def getSAN(self, gs=None, is_check=False, is_checkmate=False):
        """
        Get Standard Algebraic Notation (proper chess notation)
        E.g., Nf3, Bxe5, O-O, e4, exd5, Qh5+, Nxf7#
        
        Args:
            gs: GameState object (optional, for disambiguation)
            is_check: Whether this move resulted in check
            is_checkmate: Whether this move resulted in checkmate
        """
        # Castling
        if self.isCastleMove:
            notation = "O-O" if self.endCol == 6 else "O-O-O"
            # Add check/checkmate symbols
            if is_checkmate:
                notation += "#"
            elif is_check:
                notation += "+"
            return notation
        
        endSquare = self.getRankFile(self.endRow, self.endCol)
        piece = self.pieceMoved[1]  # p, N, B, R, Q, K
        
        # Pawn moves
        if piece == 'p':
            if self.isCapture:
                # Pawn capture: exd5
                notation = self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                # Pawn advance: e4
                notation = endSquare
            
            # Pawn promotion
            if self.isPawnPromotion:
                notation += "=Q"  # Always promote to Queen for now
            
            # Add check/checkmate symbol
            if is_checkmate:
                notation += "#"
            elif is_check:
                notation += "+"
            
            return notation
        
        # Piece moves (Knight, Bishop, Rook, Queen, King)
        notation = piece.upper()  # N, B, R, Q, K
        
        # ── DISAMBIGUATION ──
        if gs and piece in ('N', 'B', 'R', 'Q'):  # King never needs disambiguation
            notation += self._getDisambiguation(gs)
        
        # Capture symbol
        if self.isCapture:
            notation += "x"
        
        notation += endSquare
        
        # ── CHECK/CHECKMATE SYMBOLS ──
        if is_checkmate:
            notation += "#"
        elif is_check:
            notation += "+"
        
        return notation
    
    def _getDisambiguation(self, gs):
        """
        Returns disambiguation string (e.g., 'd' for Nbd7, '1' for R1a3, 'd1' for Qd1e2)
        Only called for N, B, R, Q pieces
        """
        piece = self.pieceMoved[1]
        color = self.pieceMoved[0]
        
        # Find all pieces of same type that can move to the same square
        candidates = []
        for r in range(8):
            for c in range(8):
                if gs.board[r][c] == self.pieceMoved:
                    # This is a piece of same type
                    # Check if it can legally move to our destination
                    testMove = Move((r, c), (self.endRow, self.endCol), gs.board)
                    
                    # Generate all valid moves for this square
                    tempMoves = []
                    if piece == 'N':
                        gs.getKnightMoves(r, c, tempMoves)
                    elif piece == 'B':
                        gs.getBishopMoves(r, c, tempMoves)
                    elif piece == 'R':
                        gs.getRookMoves(r, c, tempMoves)
                    elif piece == 'Q':
                        gs.getQueenMoves(r, c, tempMoves)
                    
                    # Check if this piece can reach the destination
                    for move in tempMoves:
                        if move.endRow == self.endRow and move.endCol == self.endCol:
                            candidates.append((r, c))
                            break
        
        # If only one piece can move there (this one), no disambiguation needed
        if len(candidates) <= 1:
            return ""
        
        # Disambiguation logic:
        # 1. Try file (column) first
        # 2. If files are same, use rank (row)
        # 3. If both same (shouldn't happen), use both
        
        same_file = any(c == self.startCol for r, c in candidates if (r, c) != (self.startRow, self.startCol))
        same_rank = any(r == self.startRow for r, c in candidates if (r, c) != (self.startRow, self.startCol))
        
        if not same_file:
            # File is unique, use it
            return self.colsToFiles[self.startCol]
        elif not same_rank:
            # Rank is unique, use it
            return self.rowsToRanks[self.startRow]
        else:
            # Both needed (rare)
            return self.colsToFiles[self.startCol] + self.rowsToRanks[self.startRow]
    
    def _getCheckSymbol(self, gs):
        """
        Returns '+' for check, '#' for checkmate, '' for neither
        This method analyzes what WOULD happen if this move were played
        """
        # Create a simple test by making/unmaking the move
        # Save the move in case it's already in moveLog
        was_in_log = self in gs.moveLog
        
        if not was_in_log:
            # Make the move temporarily
            gs.makeMove(self)
            
            # Check if opponent is in check
            in_check = gs.inCheck()
            
            # Generate opponent's valid moves
            opponent_moves = gs.getValidMoves()
            
            # Undo the move
            gs.undoMove()
            
            # Determine symbol
            if len(opponent_moves) == 0 and in_check:
                return "#"  # Checkmate
            elif in_check:
                return "+"  # Check
            else:
                return ""   # Neither
        else:
            # Move already in log - this is being called for historical notation
            # Check next position in moveLog
            move_index = gs.moveLog.index(self)
            
            # We need to replay up to this move to check
            # For simplicity, just return empty (this case rarely happens)
            # TODO: Improve this for move log display
            return ""