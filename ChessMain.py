# This is our main driver file, responsible for handling user input and displaying the current game state.

import pygame as p
import ChessEngine 
# global variable
WIDTH = HEIGHT = 512 # 400 is another option
DIMENSION = 8 #dimensions of chess board is 8x8 
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations later on
IMAGES = {}

# initialize a global dictionary of images. this will be called exactly once in the main, cuz if image is called every time game gonna lag

def loadImages():
    pieces = ['wp','wK','wQ','wN','wB','wR','bp','bK','bQ','bN','bB','bR']
    for piece in pieces:
        # IMAGES[piece] = p.image.load("images_svg/" + piece + ".svg")
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),(SQ_SIZE,SQ_SIZE))
    # Note: we can access the image by saying IMAGES['wp']

'''
THe main driver for our code. This will handle user input and updating the graphics
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock()
    # screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages() #only do this once before the while loop
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

# Draw the squares on the board. The top left square is always light
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):      
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draw the pieces on the board using current GameState.board
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))




if __name__ == "__main__":
    main()