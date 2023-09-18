import pygame
import random as rand
from math import dist
from math import sin

# Initialisation
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

EDGE_GAP = 5
LINE_DIST = 70
ACCELERATION_MULTI = 20
PARTICLE_SIZE = 4

# Colours
DARK_PURPLE = (12, 5, 28)
LIGHT_PURPLE = (195, 179, 232)

class Particle:
    def __init__(self):
        self.posX = rand.randint(0, SCREEN_WIDTH - 1)
        self.posY = rand.randint(0, SCREEN_HEIGHT - 1)
        self.velX = rand.randint(-10, 10) / 10
        self.velY = rand.randint(-10, 10) / 10
        self.accX = 0
        self.accY = 0
        self.size = PARTICLE_SIZE
        
    def draw(self):
        dot = pygame.Rect((self.posX, self.posY), (self.size, self.size))
        pygame.draw.ellipse(SCREEN, LIGHT_PURPLE, dot, 0)
        
    def drawLine(self, pos):
        if dist(pos, (self.posX, self.posY)) < LINE_DIST:
            pygame.draw.line(SCREEN, LIGHT_PURPLE, pos, (self.posX + self.size / 2, self.posY + self.size / 2), 1)
            distance = dist(pos, (self.posX, self.posY))
            self.accX = (pos[0] - self.posX) / (distance * ACCELERATION_MULTI)
            self.accY = (pos[1] - self.posY) / (distance * ACCELERATION_MULTI)
        else:
            self.accX = 0
            self.accY = 0
            
    def updateSize(self, pos):
        self.size = -1 * dist(pos, (self.posX, self.posY)) / 220 + 6
        
    def update(self):
        self.posX += self.velX
        self.posY += self.velY
        self.velX += self.accX
        self.velY += self.accY
        if self.posX < 0 - EDGE_GAP: self.posX = SCREEN_WIDTH - 1 + EDGE_GAP
        elif self.posX >= SCREEN_WIDTH + EDGE_GAP: self.posX = 0 - EDGE_GAP
        if self.posY < 0 - EDGE_GAP: self.posY = SCREEN_HEIGHT - 1 + EDGE_GAP
        elif self.posY >= SCREEN_HEIGHT + EDGE_GAP: self.posY = 0 - EDGE_GAP
        
class ParticleSystem:
    def __init__(self, amount):
        self.amount = amount
        self.particles = []
        self.createParticles()
    
    def createParticles(self):
        for i in range(self.amount):
            self.particles.append(Particle())
            
    def drawParticles(self):
        SCREEN.fill(DARK_PURPLE)
        for particle in self.particles:
            particle.draw()
            
    def drawLines(self, pos):
        for particle in self.particles:
            particle.drawLine(pos)
            
    def updateSizes(self, pos):
        for particle in self.particles:
            particle.updateSize(pos)
    
    def updateParticles(self):
        for particle in self.particles:
            particle.update()

def main():
    particleSystem = ParticleSystem(200)
    
    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        particleSystem.drawParticles()
        particleSystem.drawLines(pygame.mouse.get_pos())
        particleSystem.updateSizes(pygame.mouse.get_pos())
        particleSystem.updateParticles()
                
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()