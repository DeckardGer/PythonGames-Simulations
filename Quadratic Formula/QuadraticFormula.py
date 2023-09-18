import pygame
import math

# Initialise
SCREEN_SIZE = 700
SCREEN = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Quadratic Formula")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def quadratic(force, angle):
    vv = force * math.sin(angle * math.pi / 180)
    vh = force * math.cos(angle * math.pi / 180)
    t = 0
    sh = 0
    while sh < SCREEN_SIZE:
        sv = vv * t - 0.5 * 9.8 * (t ** 2)
        sh = vh * t
        t += 0.05
        pygame.draw.rect(SCREEN, WHITE, ((math.floor(sh), SCREEN_SIZE - math.floor(sv)), (2, 2)), 0)
    pygame.display.update()

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        x, y = pygame.mouse.get_pos()
        angle = math.floor(x * 90 / 700)
        force = (700 - y) / 5
                
        quadratic(force, angle)
    pygame.quit()

if __name__ == "__main__":
    main()