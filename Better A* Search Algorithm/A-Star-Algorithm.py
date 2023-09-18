import pygame
from queue import PriorityQueue

# Initialise
SCREEN_SIZE = 700
NUM_TILES = 50
TILE_SIZE = int(SCREEN_SIZE / NUM_TILES)
SCREEN = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("A* Search Algorithm")
pygame.display.set_icon(pygame.image.load("A-Star-Image.png"))

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (117, 251, 77)
RED = (234, 51, 35)
ORANGE = (242, 168, 60)
BLUE = (96, 183, 173)
DARK_BLUE = (50, 52, 168)

# Grid Values
EMPTY = 0
WALL = 1
OPEN = 2
CLOSED = 3
START = 4
GOAL = 5
PATH = 6


class Grid:
    def __init__(self):
        self.grid = [[EMPTY for x in range(NUM_TILES)] for y in range(
            NUM_TILES)]  # Generates a 2D grid of 0's

    def getGridPos(self, pos):
        return (int(pos[0] / TILE_SIZE), int(pos[1] / TILE_SIZE))

    def setStart(self, x, y):
        self.grid[y][x] = START

    def setGoal(self, x, y):
        self.grid[y][x] = GOAL

    def setWall(self, x, y):
        self.grid[y][x] = WALL

    def setClosed(self, x, y):
        self.grid[y][x] = CLOSED

    def setOpen(self, x, y):
        self.grid[y][x] = OPEN

    def setPath(self, x, y):
        self.grid[y][x] = PATH

    def resetTile(self, x, y):
        self.grid[y][x] = EMPTY

    def drawGrid(self):
        SCREEN.fill(WHITE)
        for x in range(NUM_TILES):
            for y in range(NUM_TILES):
                self.drawTiles(x, y)
                rect = pygame.Rect(
                    (x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(SCREEN, BLACK, rect, 1)
        pygame.display.update()

    def drawTiles(self, x, y):
        if self.grid[y][x] != EMPTY:
            if self.grid[y][x] == WALL:
                rect = pygame.Rect(
                    (x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(SCREEN, BLACK, rect, 0)
            if self.grid[y][x] == CLOSED:
                rect = pygame.Rect(
                    (x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(SCREEN, RED, rect, 0)
            if self.grid[y][x] == OPEN:
                rect = pygame.Rect(
                    (x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(SCREEN, GREEN, rect, 0)
            if self.grid[y][x] == START:
                rect = pygame.Rect(
                    (x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(SCREEN, ORANGE, rect, 0)
            if self.grid[y][x] == GOAL:
                rect = pygame.Rect(
                    (x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(SCREEN, BLUE, rect, 0)
            if self.grid[y][x] == PATH:
                rect = pygame.Rect(
                    (x * TILE_SIZE, y * TILE_SIZE), (TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(SCREEN, DARK_BLUE, rect, 0)

    def getNeighbors(self, x, y):
        neighbors = []
        up = False
        down = False
        left = False
        right = False
        if y > 0 and self.grid[y - 1][x] != WALL:  # Check UP
            neighbors.append((x, y - 1))
            up = True
        if y < NUM_TILES - 1 and self.grid[y + 1][x] != WALL:  # CHECK DOWN
            neighbors.append((x, y + 1))
            down = True
        if x > 0 and self.grid[y][x - 1] != WALL:  # CHECK LEFT
            neighbors.append((x - 1, y))
            left = True
        if x < NUM_TILES - 1 and self.grid[y][x + 1] != WALL:  # CHECK RIGHT
            neighbors.append((x + 1, y))
            right = True
        # CHECK UPPER LEFT
        if x > 0 and y > 0 and self.grid[y - 1][x - 1] != WALL and not (not up and not left):
            neighbors.append((x - 1, y - 1))
        # CHECK LOWER LEFT
        if x > 0 and y < NUM_TILES - 1 and self.grid[y + 1][x - 1] != WALL and not (not down and not left):
            neighbors.append((x - 1, y + 1))
        # CHECK UPPER RIGHT
        if x < NUM_TILES - 1 and y > 0 and self.grid[y - 1][x + 1] != WALL and not (not up and not right):
            neighbors.append((x + 1, y - 1))
        # CHECK LOWER RIGHT
        if x < NUM_TILES - 1 and y < NUM_TILES - 1 and self.grid[y + 1][x + 1] != WALL and not (not down and not right):
            neighbors.append((x + 1, y + 1))
        return neighbors

    def reset(self):
        for x in range(NUM_TILES):
            for y in range(NUM_TILES):
                if self.grid[y][x] != 1:
                    self.grid[y][x] = 0


def A_Star_Algorithm(grid, start, goal):
    iteration = 0
    openSet = PriorityQueue()
    # fScore, iteration, start
    openSet.put((heuristic(start, goal), iteration, start))
    cameFrom = {}
    gScore = {(x, y): float("inf") for y in range(NUM_TILES)
              for x in range(NUM_TILES)}
    gScore[start] = 0  # Initial G Score is 0
    fScore = {(x, y): float("inf") for y in range(NUM_TILES)
              for x in range(NUM_TILES)}
    # Initial F Score is just the heuristic
    fScore[start] = heuristic(start, goal)
    openSetStorage = {start}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Retrieves and deletes the next item on the queue
        currentNode = openSet.get()[2]
        openSetStorage.remove(currentNode)

        if currentNode == goal:  # Reached the end
            reconstructPath(grid, currentNode, cameFrom)
            grid.setStart(start[0], start[1])
            grid.setGoal(goal[0], goal[1])
            print(f"{iteration} Iterations")
            return True

        for neighbor in grid.getNeighbors(currentNode[0], currentNode[1]):
            # To remove diagonals, make distance 1
            tempGScore = gScore[currentNode] + \
                distCurrentNode(currentNode, neighbor)

            if tempGScore < gScore[neighbor]:
                cameFrom[neighbor] = currentNode
                gScore[neighbor] = tempGScore
                fScore[neighbor] = tempGScore + heuristic(neighbor, goal)
                if neighbor not in openSetStorage:
                    iteration += 1
                    openSet.put((fScore[neighbor], iteration, neighbor))
                    openSetStorage.add(neighbor)
                    grid.setOpen(neighbor[0], neighbor[1])

        grid.drawGrid()

        if currentNode != start:
            grid.setClosed(currentNode[0], currentNode[1])

    return False


def reconstructPath(grid, currentNode, cameFrom):
    numNodes = 0
    while currentNode in cameFrom:
        currentNode = cameFrom[currentNode]
        numNodes += 1
        grid.setPath(currentNode[0], currentNode[1])
        grid.drawGrid()
    print(f"{numNodes} long")


def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (abs(x2 - x1) + abs(y2 - y1)) * 10  # To remove diagonals, remove 10


def distCurrentNode(p1, p2):
    if (p1[0] - p2[0] - p1[1] + p2[1]) % 2 == 0:
        return 14
    else:
        return 10


def main():
    grid = Grid()
    start = None
    goal = None

    running = True

    if SCREEN_SIZE % NUM_TILES != 0:  # Check if screen is right size
        running = False
        print("\nThe screen is a right size, please change it\n")

    while running:

        grid.drawGrid()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Left Mouse Button to add squares
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x, y = grid.getGridPos(pos)

                if not start and (x, y) != goal:
                    grid.setStart(x, y)
                    start = (x, y)
                elif not goal and (x, y) != start:
                    grid.setGoal(x, y)
                    goal = (x, y)
                elif (x, y) != start and (x, y) != goal:
                    grid.setWall(x, y)

            # Right Mouse Button to remove squares
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                x, y = grid.getGridPos(pos)

                if (x, y) == start:
                    start = None
                elif (x, y) == goal:
                    goal = None
                grid.resetTile(x, y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and start and goal:  # Starts the algorithm
                    A_Star_Algorithm(grid, start, goal)

                elif event.key == pygame.K_c:  # Clears the grid
                    grid = Grid()
                    start = None
                    goal = None

                elif event.key == pygame.K_r:  # Resets the grid
                    grid.reset()
                    start = None
                    goal = None

    pygame.quit()


if __name__ == "__main__":
    main()
