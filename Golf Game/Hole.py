import pygame
from Object import Object

class Hole:
    SIZE = 26
    
    def __init__(self, position):
        self.position = position
        self.image = pygame.image.load("Resources/Hole.png")
        self.shape = pygame.Rect((self.position[0] * Object.TILE_SIZE + (Object.TILE_SIZE - self.SIZE) / 2, self.position[1] * Object.TILE_SIZE + (Object.TILE_SIZE - self.SIZE) / 2), (Hole.SIZE, Hole.SIZE))
        
    def displayHole(self, display):
        display.blit(self.image, (self.position[0] * Object.TILE_SIZE + (Object.TILE_SIZE - self.SIZE) / 2, self.position[1] * Object.TILE_SIZE + (Object.TILE_SIZE - self.SIZE) / 2 - Hole.SIZE))