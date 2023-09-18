import pygame

# Sets the sizes used in the game
SIZE = 600
NUM_TILES = 3
TILE_WIDTH = int(SIZE / NUM_TILES)

# X and O images
X_IMAGE = pygame.image.load("X.png")
X_IMAGE = pygame.transform.scale(X_IMAGE, (200, 200))
O_IMAGE = pygame.image.load("O.png")
O_IMAGE = pygame.transform.scale(O_IMAGE, (200, 200))

# Sets up player 1 and player 2
PLAYER1 = 1
PLAYER2 = 2

# Creates colours used in the game
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Board:
    # Initialises a board object
    def __init__(self):
        self.board = [[None for x in range(NUM_TILES)] for y in range(NUM_TILES)]
        self.playerTurn = PLAYER1

    # Displays the board and background
    def displayBoard(self, screen):
        screen.fill(WHITE)
        for x in range(0, SIZE, TILE_WIDTH):
            for y in range(0, SIZE, TILE_WIDTH):
                rect = pygame.Rect(x, y, TILE_WIDTH, TILE_WIDTH)
                pygame.draw.rect(screen, BLACK, rect, 10)
                
    # Displays the symbols on the board
    def displaySymbols(self, screen):
        for x in range(NUM_TILES):
            for y in range(NUM_TILES):
                if self.board[x][y] == "X":
                    screen.blit(X_IMAGE, (x * TILE_WIDTH, y * TILE_WIDTH))
                elif self.board[x][y] == "O":
                    screen.blit(O_IMAGE, (x * TILE_WIDTH, y * TILE_WIDTH))
                
    # Attempts to mark the board with the respective symbol
    def attemptMark(self, x, y):
        if self.board[x][y] == None:
            if self.playerTurn == PLAYER1:
                self.board[x][y] = "X"
                self.playerTurn = PLAYER2
            else:
                self.board[x][y] = "O"
                self.playerTurn = PLAYER1
            return True
        return False

    # Checks if anyone has won
    def checkWon(self, symbol):
        for x in range(NUM_TILES):
            won = True
            for y in range(NUM_TILES):
                if self.board[x][y] != symbol:
                    won = False
                    break
            if won:
                return True
        for y in range(NUM_TILES):
            won = True
            for x in range(NUM_TILES):
                if self.board[x][y] != symbol:
                    won = False
                    break
            if won:
                return True
        won = True
        for i in range(NUM_TILES):
            if self.board[i][i] != symbol:
                won = False
                break
        if won:
            return True
        won = True
        for i in range(NUM_TILES):
            if self.board[i][NUM_TILES - i - 1] != symbol:
                won = False
                break
        if won:
            return True
        return False

def main():
    # Initialise the settings
    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption("TIC TAC TOE")
    
    # Create the board
    board = Board()
    
    gameFinish = False
    
    # Enter the game loop
    gameRunning = True
    while gameRunning:
        
        board.displayBoard(screen)
        board.displaySymbols(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not gameFinish:
                    mouseRow, mouseCol = pygame.mouse.get_pos()
                    mouseRow = int(mouseRow / TILE_WIDTH)
                    mouseCol = int(mouseCol / TILE_WIDTH)
                
                    if board.attemptMark(mouseRow, mouseCol):
                        if board.checkWon("X"):
                            gameFinish = True
                            print("X Wins")
                        elif board.checkWon("O"):
                            gameFinish = True
                            print("O Wins")
                            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = Board()
                    gameFinish = False
        
        # Update the screen every frame
        pygame.display.flip()
        
    # After gameRunning is set to false, quit the game
    pygame.quit()

if __name__ == "__main__":
    main()