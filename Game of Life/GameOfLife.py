import pygame

# Initialise the pygame
pygame.init()

# Create the Screen
width = 1400
height = 700
screen = pygame.display.set_mode((width, height))

# Set Caption
pygame.display.set_caption("The Game of Life")

# Sets the pixel size
pixel_size = 5

pause = False

num_horizontal_boxes = int(width / pixel_size)
num_vertical_boxes = int(height / pixel_size)

present_grid = [[0] * num_horizontal_boxes for i in range(num_vertical_boxes)]
future_grid = [[0] * num_horizontal_boxes for i in range(num_vertical_boxes)]

present_grid[5][5] = 1
present_grid[5][6] = 1
present_grid[5][7] = 1
present_grid[4][7] = 1
present_grid[3][6] = 1

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def checkAlive(row, col):
    alive = 0
    if (present_grid[row][col] == 1):
        alive = 1
    return alive


def checkCell(row, col):
    numAlive = 0
    if (row - 1 >= 0 and col - 1 >= 0):
        numAlive += checkAlive(row - 1, col - 1)
    if (row - 1 >= 0):
        numAlive += checkAlive(row - 1, col)
    if (row - 1 >= 0 and col + 1 < num_horizontal_boxes):
        numAlive += checkAlive(row - 1, col + 1)
    if (col + 1 < num_horizontal_boxes):
        numAlive += checkAlive(row, col + 1)
    if (row + 1 < num_vertical_boxes and col + 1 < num_horizontal_boxes):
        numAlive += checkAlive(row + 1, col + 1)
    if (row + 1 < num_vertical_boxes):
        numAlive += checkAlive(row + 1, col)
    if (row + 1 < num_vertical_boxes and col - 1 >= 0):
        numAlive += checkAlive(row + 1, col - 1)
    if (col - 1 >= 0):
        numAlive += checkAlive(row, col - 1)
    return numAlive


def checkCells():
    for row in range(num_vertical_boxes):
        for col in range(num_horizontal_boxes):
            numAlive = checkCell(row, col)
            if (present_grid[row][col] == 1):
                if (numAlive <= 1 or numAlive >= 4):
                    future_grid[row][col] = 0
                else:
                    future_grid[row][col] = 1
            else:
                if (numAlive != 3):
                    future_grid[row][col] = 0
                else:
                    future_grid[row][col] = 1


def drawNextGen():
    for row in range(num_vertical_boxes):
        for col in range(num_horizontal_boxes):
            if (future_grid[row][col] == 1):
                pygame.draw.rect(
                    screen, WHITE, [col * pixel_size, row * pixel_size, pixel_size, pixel_size], 0)


# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_column, mouse_row = pygame.mouse.get_pos()
            mouse_row = int(mouse_row / pixel_size)
            mouse_column = int(mouse_column / pixel_size)
            if (present_grid[mouse_row][mouse_column] == 0):
                present_grid[mouse_row][mouse_column] = 1
                pygame.draw.rect(screen, WHITE, [
                                 mouse_column * pixel_size, mouse_row * pixel_size, pixel_size, pixel_size], 0)
            else:
                present_grid[mouse_row][mouse_column] = 0
                pygame.draw.rect(screen, BLACK, [
                                 mouse_column * pixel_size, mouse_row * pixel_size, pixel_size, pixel_size], 0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause

    if (not pause):
        screen.fill(BLACK)
        checkCells()
        drawNextGen()

        for row in range(num_vertical_boxes):
            for col in range(num_horizontal_boxes):
                present_grid[row][col] = future_grid[row][col]

    pygame.display.flip()
pygame.quit()
