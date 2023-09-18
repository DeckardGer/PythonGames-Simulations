import pygame
from math import sqrt

# Initialisation
pygame.font.init()
SCREEN_SIZE = 450
GAP = 50
SCREEN = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE + GAP))
FONT = pygame.font.SysFont("comicsans", 40)
pygame.display.set_caption("Sudoku Solver")

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 255, 0)

class Grid:
    origBoard = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    def __init__(self):
        self.board = self.origBoard # 2D array used to store values
        self.size = len(self.board) # The size of the board
        self.innerSize = int(sqrt(self.size)) # The size of each internal grid
        self.emptySpaces = self.findEmpty() # A list of all the empty spaces on the board
        self.numEmptySpaces = len(self.emptySpaces) # The number of empty spaces on the board
        self.tileSize = int(SCREEN_SIZE / self.size) # The size a tile is on the screen
        self.selectedSpace = None # The current selected tile
        self.selectedSpaceMark = True # If the mode is to mark or draw the value in the square
        
    # Draws the board to the GUI including the thin lines, bolder lines, timer and numbers
    def draw(self):
        SCREEN.fill(WHITE)
        # Create grid
        for lineNum in range(self.size + 1):
            if lineNum % self.innerSize == 0 or lineNum == 0:
                pygame.draw.line(SCREEN, BLACK, (0, lineNum * self.tileSize + GAP), (SCREEN_SIZE, lineNum * self.tileSize + GAP), 5)
                pygame.draw.line(SCREEN, BLACK, (lineNum * self.tileSize, 0 + GAP), (lineNum * self.tileSize, SCREEN_SIZE + GAP), 5)
            else:
                pygame.draw.line(SCREEN, BLACK, (0, lineNum * self.tileSize + GAP), (SCREEN_SIZE, lineNum * self.tileSize + GAP), 2)
                pygame.draw.line(SCREEN, BLACK, (lineNum * self.tileSize, 0 + GAP), (lineNum * self.tileSize, SCREEN_SIZE + GAP), 2)
                
        # Display numbers
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] != 0:
                    text = FONT.render(str(self.board[y][x]), 1, BLACK)
                    SCREEN.blit(text, (x * self.tileSize + self.tileSize / 3, y * self.tileSize + GAP + self.tileSize / 3))
                    
        if self.selectedSpace:
            selectedRect = pygame.Rect(self.selectedSpace[0] * self.tileSize + 1, self.selectedSpace[1] * self.tileSize + GAP + 1, self.tileSize, self.tileSize)
            pygame.draw.rect(SCREEN, RED, selectedRect, 2)
                
    # Uses recursion to solve every empty space on the grid until it
    # hits an invalid configuration. It then back-tracks until it finds
    # a different approach then continues 
    def solveGrid(self, emptyIndex):
        if emptyIndex >= self.numEmptySpaces:
            return True

        for num in range(1, self.size + 1):
            if self.checkValid(self.emptySpaces[emptyIndex], num):
                col, row = self.emptySpaces[emptyIndex]
                self.board[row][col] = num

                emptyIndex += 1

                if self.solveGrid(emptyIndex):
                    return True
                else:
                    emptyIndex -= 1

                self.board[row][col] = 0
        return False
    
    # Finds every empty space on the board and stores them to be used later
    def findEmpty(self):
        emptySpaces = []
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] == 0:
                    emptySpaces.append((x, y))
        return emptySpaces

    # Checks if a number can be entered at a specific position
    def checkValid(self, pos, num):
        # Horizontal Check
        for x in range(self.size):
            if self.board[pos[1]][x] == num and x != pos[0]:
                return False

        # Vertical Check
        for y in range(self.size):
            if self.board[y][pos[0]] == num and y != pos[0]:
                return False

        # Inner Grid Check
        innerGrid_X = pos[0]//self.innerSize
        innerGrid_Y = pos[1]//self.innerSize

        for y in range(innerGrid_Y * self.innerSize, innerGrid_Y * self.innerSize + self.innerSize):
            for x in range(innerGrid_X * self.innerSize, innerGrid_X * self.innerSize + self.innerSize):
                if self.board[y][x] == num and (x, y) != pos:
                    return False
        return True
    
    def mark(self, num):
        if self.selectedSpace:
            self.board[self.selectedSpace[1]][self.selectedSpace[0]] = num
            
        print(self.origBoard[self.selectedSpace[1]][self.selectedSpace[0]], self.board[self.selectedSpace[1]][self.selectedSpace[0]])
    
    # Selects a space on the board that is allowed to be selected and takes away the selection if it's on the same space
    def selectSpace(self, pos):
        if self.selectedSpace != pos:
            self.selectedSpace = pos
            if self.origBoard[self.selectedSpace[1]][self.selectedSpace[0]] != 0:
                self.selectedSpace = None
        else:
            self.selectedSpace = None

def main():
    grid = Grid()
    
    running = True
    if SCREEN_SIZE % grid.size != 0:
        running = False
        print(f"\nThe screen size must be a value divisible by {grid.size}\n")
        
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouseRow, mouseCol = pygame.mouse.get_pos()
                mouseRow = int(mouseRow / grid.tileSize)
                mouseCol = int(mouseCol / grid.tileSize)
                if mouseCol > 0:
                    grid.selectSpace((mouseRow, mouseCol - 1))
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid.solveGrid(0)
                elif event.key == pygame.K_1:
                    grid.mark(1)
                elif event.key == pygame.K_2:
                    grid.mark(2)
                elif event.key == pygame.K_3:
                    grid.mark(3)
                elif event.key == pygame.K_4:
                    grid.mark(4)
                elif event.key == pygame.K_5:
                    grid.mark(5)
                elif event.key == pygame.K_6:
                    grid.mark(6)
                elif event.key == pygame.K_7:
                    grid.mark(7)
                elif event.key == pygame.K_8:
                    grid.mark(8)
                elif event.key == pygame.K_9:
                    grid.mark(9)
                
        grid.draw()       
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()