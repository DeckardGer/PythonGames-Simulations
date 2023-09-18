import pygame
from Game import Game

WIDTH = 1440
HEIGHT = 786
FPS = 60

if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Golf Game")
    game = Game(display)
    game.start(FPS)