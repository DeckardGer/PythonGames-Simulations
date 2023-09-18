import pygame
import random
import math

# Initialise

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
BOID_SIZE = 8 # 8
MAX_SPEED = 5 # 5
ALLIGNMENT_MULT = 0.05 # 0.05
COHESION_MULT = 0.02 # 0.02
SEPERATION_MULT = 0.03 # 0.03
PERCEPTION_RADIUS = 50 # 50
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Boids")

SURFACE = pygame.Surface((15, 15)).convert()
DEBUG = False

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 100, 50)
BLUE = (3, 223, 252)
RED = (252, 4, 3)
PURPLE = (123, 3, 252)

class Boid:
    def __init__(self): # Creates a boid with a random position
        self.position = (random.randint(0, SCREEN_WIDTH - 1), random.randint(0, SCREEN_HEIGHT - 1))
        angle = random.randint(0, 359) * math.pi / 180
        self.velocity = (MAX_SPEED * math.cos(angle), MAX_SPEED * math.sin(angle))
        self.acceleration = (0, 0)
        
    def show(self): # Displays the boid on the screen
        if not DEBUG:
            pygame.draw.polygon(SURFACE, WHITE, ((7,0), (13,14), (7,11), (1,14), (7,0)))
            angle = 0
            if self.velocity[0] != 0 and self.velocity[1] != 0:
                angle = -1 * math.degrees(math.atan2(math.radians(self.velocity[1]), math.radians(self.velocity[0])))
            SCREEN.blit(pygame.transform.rotate(SURFACE, angle - 90), (self.position[0] - 7, self.position[1] - 7))
        
    def update(self): # Updates the boids movement every frame
        self.velocity = (self.velocity[0] + self.acceleration[0], self.velocity[1] + self.acceleration[1])
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        self.acceleration = (0, 0)
        
    def checkEdges(self): # If a boid is on the edge, set its velocity to push it away
        x, y = self.velocity
        if self.position[0] > SCREEN_WIDTH - 150 : x -= 0.1
        elif self.position[0] < 150 : x += 0.1
        if self.position[1] > SCREEN_HEIGHT - 150 : y -= 0.1
        elif self.position[1] < 150 : y += 0.1
        self.velocity = (x, y)
        
    def getCloseBoids(self, boids): # Returns the boids in its perception radius
        closeBoids = []
        for boid in boids:
            if distance(self.position, boid.position) < PERCEPTION_RADIUS and self != boid:
                closeBoids.append(boid)
        return closeBoids
    
    def allignment(self, closeBoids): # Allign the boid with all the other boids
        steerX, steerY = 0, 0
        for boid in closeBoids:
            steerX += boid.velocity[0]
            steerY += boid.velocity[1]
        steerX /= len(closeBoids)
        steerY /= len(closeBoids)
        steerMag = math.sqrt(math.pow(steerX, 2) + math.pow(steerY, 2))
        steerX *= MAX_SPEED / steerMag
        steerY *= MAX_SPEED / steerMag
        steerX -= self.velocity[0]
        steerY -= self.velocity[1]
        return (steerX, steerY)
    
    def cohesion(self, closeBoids): # Make the boid go close to all the other boids
        pointX, pointY = 0, 0
        for boid in closeBoids:
            pointX += boid.position[0]
            pointY += boid.position[1]
        pointX /= len(closeBoids)
        pointY /= len(closeBoids)
        steerX = pointX - self.position[0]
        steerY = pointY - self.position[1]
        steerMag = math.sqrt(math.pow(steerX, 2) + math.pow(steerY, 2))
        steerX *= MAX_SPEED / steerMag
        steerY *= MAX_SPEED / steerMag
        steerX -= self.velocity[0]
        steerY -= self.velocity[1]
        return (steerX, steerY)
    
    def seperation(self, closeBoids): # If a boid gets too close, push the boid away
        steerX, steerY = 0, 0
        for boid in closeBoids:
            dist = distance(self.position, boid.position)
            diffX = self.position[0] - boid.position[0]
            diffY = self.position[1] - boid.position[1]
            diffX /= (dist * dist)
            diffY /= (dist * dist)
            steerX += diffX
            steerY += diffY
        steerX /= len(closeBoids)
        steerY /= len(closeBoids)
        steerMag = math.sqrt(math.pow(steerX, 2) + math.pow(steerY, 2))
        steerX *= MAX_SPEED / steerMag
        steerY *= MAX_SPEED / steerMag
        steerX -= self.velocity[0]
        steerY -= self.velocity[1]
        return (steerX, steerY)
        
    def flock(self, boids): # Run the 3 different boid actions and update the boids acceleration
        closeBoids = self.getCloseBoids(boids)
        
        if len(closeBoids) > 0:
            allignment = self.allignment(closeBoids)
            cohesion = self.cohesion(closeBoids)
            seperation = self.seperation(closeBoids)
            
            if DEBUG:
                for boid in closeBoids:
                    pygame.draw.line(SCREEN, GREEN, self.position, boid.position, 1)
                    pygame.draw.line(SCREEN, BLUE, self.position, (self.position[0] + allignment[0] * 10, self.position[1] + allignment[1] * 10), 1)
                    pygame.draw.line(SCREEN, RED, self.position, (self.position[0] + cohesion[0] * 10, self.position[1] + cohesion[1] * 10), 1)
                    pygame.draw.line(SCREEN, PURPLE, self.position, (self.position[0] + seperation[0] * 10, self.position[1] + seperation[1] * 10), 1)
            
            self.acceleration = (self.acceleration[0] + allignment[0] * ALLIGNMENT_MULT, self.acceleration[1] + allignment[1] * ALLIGNMENT_MULT)
            self.acceleration = (self.acceleration[0] + cohesion[0] * COHESION_MULT, self.acceleration[1] + cohesion[1] * COHESION_MULT)
            self.acceleration = (self.acceleration[0] + seperation[0] * SEPERATION_MULT, self.acceleration[1] + seperation[1] * SEPERATION_MULT)
            
def distance(p1, p2):
    return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))

def main():
    boids = [Boid() for x in range(200)]
    
    running = True
    while running:
        
        SCREEN.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        for boid in boids:  
            boid.checkEdges()
            boid.flock(boids)
        for boid in boids:
            boid.update()
            boid.show()
                
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()