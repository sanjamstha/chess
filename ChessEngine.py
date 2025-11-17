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


    # Takes a move as parameter and executes it ( doesnt work for castling, en-passant, and pawn promotion )
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move to undo later or dipslay game history
        self.whiteToMove = not self.whiteToMove # swap players
        # update the king's location 
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        
        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
        
        # enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--' # capturing pawn
        
        #update enpassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: #2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()

    
    # Undo the last move made 
    def undoMove(self): 
        if len(self.moveLog) != 0: #make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            # update the king's location 
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            
            #undo enpassant move
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' #leave landing sqaure blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            # undo a 2 square pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()
    
    #All moves considering checks
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        # Naive Algorithm
        # 1. generate all possible moves
        moves = self.getAllPossibleMoves()
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
        enemy_color = 'b' if self.whiteToMove else 'w'
        # # for mvoes/captures to the right, code has to repeat for all 4 directions
        # step = 1
        # while (c+step<=7):
        #     nxtSq = self.board[r][c+step]
        #     if nxtSq == "--":
        #         moves.append(Move((r,c),(r,c+step),self.board))
        #     else:
        #         if nxtSq[0] == enemy_color:
        #             moves.append(Move((r,c),(r,c+step),self.board))
        #         break
        #     step += 1

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
                    if nxtSq[0] == enemy_color:
                        moves.append(Move((r, c), (end_r, end_c), self.board))
                    break

                step += 1

    # Get all the Bishop moves for the bishop located at rol, col and add these moves to the list 
    def getBishopMoves(self,r,c,moves):
        enemy_color = 'b' if self.whiteToMove else 'w'
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
                    if nxtSq[0] == enemy_color:
                        moves.append(Move((r, c), (end_r, end_c), self.board))
                    break
                step += 1

    # Get all the queen moves for the queen located at rol, col and add these moves to the list 
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    # Get all the king moves for the king located at rol, col and add these moves to the list 
    def getKingMoves(self,r,c,moves):
        enemy_color = 'b' if self.whiteToMove else 'w'

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
                if nxtSq[0] == enemy_color:
                    moves.append(Move((r, c), (end_r, end_c), self.board))
                continue  # blocked by piece

    # Get all the knight moves for the knight located at rol, col and add these moves to the list 
    def getKnightMoves(self,r,c,moves):
        enemy_color = 'b' if self.whiteToMove else 'w'
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
                if nxtSq[0] == enemy_color:
                    moves.append(Move((r,c),(end_r,end_c),self.board))
                continue

class Move():
    # map keys to value 
    # key: value 
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,"5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d":3,"e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startsq, endsq, board, isEnpassantMove = False):
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # pawn promotion
        self.isPawnPromotion =  (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7) #alternative for if statement

        # en passant
        self.isEnpassantMove =  isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

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