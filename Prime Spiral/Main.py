import pygame
from math import sqrt

WIDTH = 1400
HEIGHT = 760
FPS = 60
TILE_SIZE = 1
PRIMECOUNT = 2_000_000

# This simulation takes a long time to load. Please be patient.
# If you want to lower the prime count, also increase the tile size.

# Checks if a given number is prime


def checkPrime(checkNum):
    isPrime = True
    if checkNum == 1:
        isPrime = False
    else:
        for num in range(2, int(sqrt(checkNum)) + 1):
            if checkNum % num == 0:
                isPrime = False
    return isPrime

# Returns a boolean value for every number in a given range


def getPrimes(value):
    primes = []
    for num in range(1, value + 1):
        primes.append(checkPrime(num))
    return primes


def drawSpiral(screen, primes):
    pos = (WIDTH / 2 - TILE_SIZE / 2, HEIGHT / 2 - TILE_SIZE / 2)
    nextStepCount = 1
    steps = 0
    numTurns = 0
    dir = (1, 0)
    for prime in primes:
        if prime:
            rect = pygame.Rect(pos, (TILE_SIZE, TILE_SIZE))
            pygame.draw.ellipse(screen, (255, 255, 255), rect, 0)
        pos = (pos[0] + TILE_SIZE * dir[0], pos[1] + TILE_SIZE * dir[1])
        steps += 1
        if steps == nextStepCount:
            numTurns += 1
            steps = 0
            dir = turn(dir)
            if numTurns == 2:
                numTurns = 0
                nextStepCount += 1


def turn(dir):
    if dir == (1, 0):
        dir = (0, -1)
    elif dir == (0, -1):
        dir = (-1, 0)
    elif dir == (-1, 0):
        dir = (0, 1)
    elif dir == (0, 1):
        dir = (1, 0)
    return dir

# Main loop for drawing/updating the spiral


def main():
    pygame.init()
    pygame.display.set_caption("Prime Spiral")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    primes = getPrimes(PRIMECOUNT)
    drawSpiral(screen, primes)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


# Start
if __name__ == "__main__":
    main()
