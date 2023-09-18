import pygame
import math
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Boundary:
    # Creates two points on the screen
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        
    # Connects the two points with a line, creating a wall
    def show(self, screen):
        pygame.draw.line(screen, WHITE, self.p1, self.p2)
        
    # Returns the first point of the wall
    def get_p1(self):
        return self.p1
    
    # Returns the second point of the wall
    def get_p2(self):
        return self.p2
        
class Ray:
    # Creates a ray that starts at a position and heads in a direction
    def __init__(self, pos, dir):
        self.pos = pos
        self.dir = dir
        
    # Updates the position and direction of the
    def update(self, pos):
        self.dir = (self.dir[0] - self.pos[0] + pos[0], self.dir[1] - self.pos[1] + pos[1])
        self.pos = pos
        
    # Returns a point if a ray touches a wall
    def cast(self, wall_p1, wall_p2):
        wall_x1, wall_y1 = wall_p1
        wall_x2, wall_y2 = wall_p2
        
        ray_x1, ray_y1 = self.pos
        ray_x2, ray_y2 = self.dir
        
        denominator = (wall_x1 - wall_x2) * (ray_y1 - ray_y2) - (wall_y1 - wall_y2) * (ray_x1 - ray_x2)
        if denominator != 0:
            t = ((wall_x1 - ray_x1) * (ray_y1 - ray_y2) - (wall_y1 - ray_y1) * (ray_x1 - ray_x2)) / denominator
            u = -((wall_x1 - wall_x2) * (wall_y1 - ray_y1) - (wall_y1 - wall_y2) * (wall_x1 - ray_x1)) / denominator
            if t > 0 and t < 1 and u > 0:
                px = wall_x1 + t * (wall_x2 - wall_x1)
                py = wall_y1 + t * (wall_y2 - wall_y1)
                return (px, py)
        return None

class Particle:
    # Creates a particle which has a position and emits rays in every direction
    def __init__(self):
        self.pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.rays = []
        for a in range(0, 360, 1):
            self.rays.append(Ray(self.pos, getDir(self.pos, a)))
            
    # Displays the light source
    def show(self, screen):
        pygame.draw.ellipse(screen, WHITE, [self.pos[0] - 3, self.pos[1] - 3, 6, 6], 0)
            
    # Updates the position of the particle
    def update(self, pos):
        self.pos = pos
        for ray in self.rays:
            ray.update(pos)
            
    # Searches through every ray and tests if it collides with a wall. It must collide with the closest wall
    def search(self, walls, screen):
        for ray in self.rays:
            closest = None
            smallest = SCREEN_WIDTH + SCREEN_HEIGHT
            for wall in walls:
                point = ray.cast(wall.get_p1(), wall.get_p2())
                if point != None:
                    dist = math.sqrt(((self.pos[0] - point[0]) * (self.pos[0] - point[0])) + ((self.pos[1] - point[1]) * (self.pos[1] - point[1])))
                    if dist < smallest:
                        smallest = dist
                        closest = point
            if closest != None:
                pygame.draw.line(screen, WHITE, self.pos, closest)
  
# Returns the vector for a direction given the position and angle
def getDir(pos, angle):
    return (pos[0] + math.cos(angle / 180 * math.pi), pos[1] + math.sin(angle / 180 * math.pi))

def createWalls():
    walls = []
    
    for i in range(5):
        w_p1 = (random.randint(1, SCREEN_WIDTH - 1), random.randint(1, SCREEN_HEIGHT - 1))
        w_p2 = (random.randint(1, SCREEN_WIDTH - 1), random.randint(1, SCREEN_HEIGHT - 1))
        walls.append(Boundary(w_p1, w_p2))
        
    walls.append(Boundary((-1, 0), (-1, SCREEN_HEIGHT)))
    walls.append(Boundary((-1, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT)))
    walls.append(Boundary((SCREEN_WIDTH, SCREEN_HEIGHT), (SCREEN_WIDTH, 0)))
    walls.append(Boundary((SCREEN_WIDTH, 0), (-1, 0)))
    
    return walls

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2D Raycasting")
    
    walls = createWalls()
    
    particle = Particle()
    
    running = True
    while running:
        # Fills the screen in black
        screen.fill(BLACK)
        
        # Goes through every wall and shows them
        for wall in walls:
            wall.show(screen)
            
        # Shows the particle and every ray from it
        particle.show(screen)
        
        # Looks for any walls the particles rays collide with
        particle.search(walls, screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    walls = createWalls()
                    
        # Updates the particles location every frame
        mouseRow, mouseCol = pygame.mouse.get_pos()
        particle.update((mouseRow, mouseCol))
        
        pygame.display.flip()
    pygame.quit()
            
if __name__ == "__main__":
    main()