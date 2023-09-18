import pygame

width = 700
height = 700

timestep = 100000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (10, 242, 247)
DARK_BLUE = (16, 34, 230)


class Block:
    def __init__(self, x, size, mass, velocity, colour):
        self.x = x
        self.size = size
        self.mass = mass
        self.velocity = velocity
        self.colour = colour

    def drawBlock(self, screen):
        rect = pygame.Rect(self.x, 100, self.size, self.size)
        pygame.draw.rect(screen, self.colour, rect, 0)

    def move(self):
        self.x = self.x + self.velocity

    def getX(self):
        return self.x

    def getMass(self):
        return self.mass

    def getVelocity(self):
        return self.velocity

    def setVelocity(self, newVelocity):
        self.velocity = newVelocity

    def collide(self, block):
        return self.x + self.size >= block.getX()

    def bounceBlock(self, block):
        sumM = self.mass + block.getMass()
        newV = (self.mass - block.getMass()) / sumM * self.velocity
        newV += (2 * block.getMass() / sumM) * block.getVelocity()
        return newV

    def bounceWall(self):
        if self.x <= 0:
            self.velocity *= -1
            return True
        return False


def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("PI Estimation")
    font = pygame.font.SysFont('Comic Sans MS', 30)

    block1 = Block(100, 20, 1, 0, LIGHT_BLUE)
    block2 = Block(200, 100, 10000000000, -1, DARK_BLUE)

    collisionCount = 0

    gameRunning = True
    while gameRunning:
        # Fill black screen
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRunning = False

        for i in range(timestep):
            block1.drawBlock(screen)
            block2.drawBlock(screen)

            if block1.collide(block2):
                v1 = block1.bounceBlock(block2)
                v2 = block2.bounceBlock(block1)

                block1.setVelocity(v1)
                block2.setVelocity(v2)

                collisionCount += 1

            if block1.bounceWall():
                collisionCount += 1

            block1.move()
            block2.move()

        textSurface = font.render(str(collisionCount), False, WHITE)

        screen.blit(textSurface, (5, 5))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
