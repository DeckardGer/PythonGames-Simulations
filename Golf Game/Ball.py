import pygame
import math

class Ball:
    FRICTION = 0.97
    SIZE = 26
    MAX_POWER = 3000
    STILL = 0
    TAKING_SHOT = 1
    MOVING = 2
    
    # Create a ball
    def __init__(self, position):
        self.position = position
        self.velocity = {'x': 0, 'y': 0}
        self.shape = pygame.Rect((position['x'], position['y']), (Ball.SIZE, Ball.SIZE))
        self.state = self.STILL
        self.powerLvl = 0
        self.arrowPosition = (position['x'] + Ball.SIZE / 2, position['y'] + Ball.SIZE / 2)
        self.image = pygame.image.load("Resources/GolfBall.png")
        
    # Update the balls position if it's moving  
    def updateBall(self, dt, objects):
        # If the ball is moving
        if self.state == Ball.MOVING:
            # Check the balls position for the next frame
            newPositionX = {'x': self.position['x'] + self.velocity['x'] * dt, 'y': self.position['y']}
            newPositionY = {'x': self.position['x'], 'y': self.position['y'] + self.velocity['y'] * dt}
            
            # Check if the ball collides with any object
            for object in objects:
                if pygame.Rect.colliderect(pygame.Rect((newPositionX['x'], newPositionX['y']), (Ball.SIZE, Ball.SIZE)), object.shape):
                    self.velocity['x'] *= -1
                if pygame.Rect.colliderect(pygame.Rect((newPositionY['x'], newPositionY['y']), (Ball.SIZE, Ball.SIZE)), object.shape):
                    self.velocity['y'] *= -1
                    
            # Update position
            self.position = {'x': self.position['x'] + self.velocity['x'] * dt, 'y': self.position['y'] + self.velocity['y'] * dt}
            self.shape = pygame.Rect((self.position['x'], self.position['y']), (Ball.SIZE, Ball.SIZE))

            # Update velocity
            self.velocity = {'x': self.velocity['x'] * Ball.FRICTION, 'y': self.velocity['y'] * Ball.FRICTION}
            
            if math.sqrt(self.velocity['x']**2 + self.velocity['y']**2) < 15:
                self.arrowPosition = (self.position['x'] + Ball.SIZE / 2, self.position['y'] + Ball.SIZE / 2)
                self.state = Ball.STILL

    # Display the ball on the screen
    def displayBall(self, display):
        display.blit(self.image, (self.position['x'], self.position['y']))