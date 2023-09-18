import pygame
import random

SCREEN_SIZE = 600
NUM_CELLS = 15
CELL_SIZE = int(SCREEN_SIZE / NUM_CELLS)

BOMB_CHANCE = 8  # Chance a cell has of being a bomb

BLACK = (0, 0, 0)
DARK_GREY = (120, 120, 120)
LIGHT_GREY = (192, 192, 192)
WHITE = (255, 255, 255)


class Grid:
    def __init__(self):
        self.grid = [[Cell() for i in range(NUM_CELLS)]
                     for j in range(NUM_CELLS)]

    # Displays the grid
    def showGrid(self, screen):
        for i in range(NUM_CELLS):
            for j in range(NUM_CELLS):
                rect = pygame.Rect(i * CELL_SIZE, j *
                                   CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.grid[i][j].checkRevealed():  # Darker
                    pygame.draw.rect(screen, DARK_GREY, rect, 0)
                    self.grid[i][j].showImage(
                        screen, i * CELL_SIZE, j * CELL_SIZE)
                else:  # Lighter
                    pygame.draw.rect(screen, LIGHT_GREY, rect, 0)
                    if self.grid[i][j].checkFlag():
                        self.grid[i][j].showFlag(
                            screen, i * CELL_SIZE, j * CELL_SIZE)
                pygame.draw.rect(screen, BLACK, rect, 1)

    # Reveals the selected cell in the grid
    def revealCell(self, x, y):
        self.grid[x][y].reveal()
        if self.grid[x][y].checkBomb():
            pass  # Player loses
        else:
            bombCount = self.getSurroundingBombs(x, y)
            if bombCount > 0:
                self.grid[x][y].setImageNumber(bombCount)
            else:
                self.floodFill(x, y)

    def flagCell(self, x, y):
        self.grid[x][y].addFlag()

    def floodFill(self, x, y):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if x + i >= 0 and x + i < NUM_CELLS and y + j >= 0 and y + j < NUM_CELLS and not self.grid[x + i][y + j].checkRevealed() and not self.grid[x + i][y + j].checkBomb():
                    self.revealCell(x + i, y + j)

    def checkWin(self):
        won = True
        for i in range(NUM_CELLS):
            for j in range(NUM_CELLS):
                if not self.grid[i][j].checkBomb() and not self.grid[i][j].checkRevealed():
                    won = False
                    break
        return won

    def checkLost(self):
        lost = False
        for i in range(NUM_CELLS):
            for j in range(NUM_CELLS):
                if self.grid[i][j].checkBomb() and self.grid[i][j].checkRevealed():
                    lost = True
                    break
        return lost

    # Checks surrounding cells if they are bombs
    def getSurroundingBombs(self, x, y):
        bombCount = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if x + i >= 0 and x + i < NUM_CELLS and y + j >= 0 and y + j < NUM_CELLS and self.grid[x + i][y + j].checkBomb():
                    bombCount += 1
        return bombCount


class Cell:
    def __init__(self):
        self.bomb = random.randint(1, BOMB_CHANCE) == 1
        self.revealed = False
        self.image = None
        self.flag = False
        if self.bomb:
            self.image = pygame.image.load("bomb.png")  # Set Bomb image
            self.image = pygame.transform.scale(
                self.image, (CELL_SIZE, CELL_SIZE))

    # Returns if the cell has been revealed or not
    def checkRevealed(self):
        return self.revealed

    # Returns in the cell is a bomb or not
    def checkBomb(self):
        return self.bomb

    def checkFlag(self):
        return self.flag

    def addFlag(self):
        self.flag = True

    # Reveals the cell
    def reveal(self):
        self.revealed = True

    def setImageNumber(self, bombCount):
        if bombCount == 1:
            self.image = pygame.image.load("1.png")  # Set Bomb image
        elif bombCount == 2:
            self.image = pygame.image.load("2.png")  # Set Bomb image
        elif bombCount == 3:
            self.image = pygame.image.load("3.png")  # Set Bomb image
        elif bombCount == 4:
            self.image = pygame.image.load("4.png")  # Set Bomb image
        elif bombCount == 5:
            self.image = pygame.image.load("5.png")  # Set Bomb image
        elif bombCount == 6:
            self.image = pygame.image.load("6.png")  # Set Bomb image
        elif bombCount == 7:
            self.image = pygame.image.load("7.png")  # Set Bomb image
        elif bombCount == 8:
            self.image = pygame.image.load("8.png")  # Set Bomb image
        if self.image != None:
            self.image = pygame.transform.scale(
                self.image, (CELL_SIZE, CELL_SIZE))

    def showImage(self, screen, x, y):
        if self.image != None:
            screen.blit(self.image, (x, y))

    def showFlag(self, screen, x, y):
        flagImage = pygame.image.load("flag.png")
        flagImage = pygame.transform.scale(flagImage, (CELL_SIZE, CELL_SIZE))
        screen.blit(flagImage, (x, y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Minesweeper")
    pygame.display.set_icon(pygame.image.load("bomb.png"))

    grid = Grid()

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:
                mouseRow, mouseCol = pygame.mouse.get_pos()
                mouseRow = int(mouseRow / CELL_SIZE)
                mouseCol = int(mouseCol / CELL_SIZE)
                grid.revealCell(mouseRow, mouseCol)

            elif pygame.mouse.get_pressed()[2]:
                mouseRow, mouseCol = pygame.mouse.get_pos()
                mouseRow = int(mouseRow / CELL_SIZE)
                mouseCol = int(mouseCol / CELL_SIZE)
                grid.flagCell(mouseRow, mouseCol)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid = Grid()

                elif event.key == pygame.K_f:
                    mouseRow, mouseCol = pygame.mouse.get_pos()
                    mouseRow = int(mouseRow / CELL_SIZE)
                    mouseCol = int(mouseCol / CELL_SIZE)
                    grid.flagCell(mouseRow, mouseCol)

        grid.showGrid(screen)

        if grid.checkWin():
            print("You Win!")
            running = False
        elif grid.checkLost():
            print("You Lose!")
            grid = Grid()
            #running = False

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
