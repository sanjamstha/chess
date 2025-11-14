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
        moves = [Move((6,4),(4,4), self.board)]
        for r in range(len(self.board)):     # number of rows 
            for c in range(len(self.board[r])): # number of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) and (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r,c, moves)
                    elif piece == 'r':
                        self.getRookMoves(r,c,moves)
        return moves
                    
    # Get all the pawn moves for the pawn located at rol, col and add these moves to the list 
    def getPawnMoves(self, r, c, moves):
        pass

    
    # Get all the rook moves for the rook located at rol, col and add these moves to the list 
    def getRookMoves(self, r, c, moves):
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
        print(self.moveID)

    # Overriding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]