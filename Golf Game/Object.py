import pygame

class Object:
    BLACK = (0, 0, 0)
    GREEN = (97, 136, 70)
    TILE_SIZE = 40
    
    def __init__(self, position, size):
        self.position = position
        self.shape = pygame.Rect((position[0] * Object.TILE_SIZE, position[1] * Object.TILE_SIZE), (size[0] * Object.TILE_SIZE, size[1] * Object.TILE_SIZE))
        self.outline = pygame.Rect((position[0] * Object.TILE_SIZE, position[1] * Object.TILE_SIZE), (size[0] * Object.TILE_SIZE, size[1] * Object.TILE_SIZE))
    
    def displayObject(self, display):
        pygame.draw.rect(display, Object.GREEN, self.shape, 0)
        pygame.draw.rect(display, Object.BLACK, self.outline, 4)
        