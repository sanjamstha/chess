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
    # Takes a move as parameter and executes it ( doesnt work for castling, en-passant, and pawn promotion )
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move to undo later or dipslay game history
        self.whiteToMove = not self.whiteToMove # swap players
    
    # Undo the last move made 
    def undoMove(self): 
        if len(self.moveLog) != 0: #make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
    
    #All moves considering checks
    def getValidMoves(self):
        return self.getAllPossibleMoves() #for now we wont worry about checks

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

            if c+1 <= 7: # capture to the right
                if self.board[r-1][c+1][0] == 'b': # enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))

        else:   # black pawn moves
            if self.board[r+1][c] == "--": # 1sq pawn advance
                moves.append(Move((r,c),(r+1,c),self.board))
                if r == 1 and self.board[r+2][c] == "--": # 2sq pawn advance
                    moves.append(Move((r,c),(r+2,c),self.board))

            if c+1 <= 7: # captures to the left 
                if self.board[r+1][c+1][0] == 'w': #enemy piece to capture
                    moves.append(Move((r,c),(r+1,c+1), self.board))

            if c-1 >= 0: # capture to the right
                if self.board[r+1][c-1][0] == 'w': # enemy piece to capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))
    
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
            step = 1
            while True:
                end_r = r + dr * step
                end_c = c + dc * step

                # Stop if outside board
                if not (0 <= end_r <= 7 and 0 <= end_c <= 7):
                    break

                nxtSq = self.board[end_r][end_c]

                if nxtSq == "--":
                    # empty square → valid move
                    moves.append(Move((r, c), (end_r, end_c), self.board))
                else:
                    # capture only if enemy piece
                    if nxtSq[0] == enemy_color:
                        moves.append(Move((r, c), (end_r, end_c), self.board))
                    break  # blocked by piece

                step += 1

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
        pass

    




    
class Move():
    # map keys to value 
    # key: value 
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,"5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d":3,"e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startsq, endsq, board):
        self.startRow = startsq[0]
        self.startCol = startsq[1]
        self.endRow = endsq[0]
        self.endCol = endsq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
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