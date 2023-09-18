import pygame
import math
from Ball import Ball
from Levels import Levels
from Hole import Hole

class Game:
    POWER_LVL_BACKGROUND_SIZE = (40, 110)
    MAX_POWER_DISTANCE = 200
    ARROW_LENGTH = 80
    
    # Create the games components
    def __init__(self, display):
        self.display = display
        self.ball = Ball({'x': 200, 'y': 200})
        self.levels = Levels()
        self.level = self.levels.getNextLevel()
        self.hole = Hole((2, 4))
        self.background = pygame.image.load("Resources/Background.png")
        
    # Start the game
    def start(self, fps):
        clock = pygame.time.Clock()
        running = True
                
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                # If the ball is still and the mouse button is clicked, check if the mouse
                # is over the ball and if so, set the state to taking a shot
                if self.ball.state == Ball.STILL and event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.ball.shape.collidepoint(pos[0], pos[1]):
                        self.ball.state = Ball.TAKING_SHOT
                # If the state of the ball is taking the shot
                elif self.ball.state == Ball.TAKING_SHOT:
                    pos = pygame.mouse.get_pos()
                    
                    velocity = [self.ball.position['x'] + (Ball.SIZE / 2) - pos[0], self.ball.position['y'] + (Ball.SIZE / 2) - pos[1]]
                    distance = math.sqrt(velocity[0]**2 + velocity[1]**2)
                    distanceScale = distance / self.MAX_POWER_DISTANCE
                    self.ball.powerLvl = min(1, distanceScale)
                    
                    angle = math.pi / 2 - math.atan2(velocity[0], velocity[1]) 
                    self.ball.arrowPosition = (self.ball.position['x'] + (Ball.SIZE / 2) + self.ARROW_LENGTH * math.cos(angle),
                                               self.ball.position['y'] + (Ball.SIZE / 2) + self.ARROW_LENGTH * math.sin(angle))
                    
                    if event.type == pygame.MOUSEBUTTONUP:
                        if distanceScale > 1:
                            velocity[0] /= distanceScale
                            velocity[1] /= distanceScale
                        velocity[0] *= (Ball.MAX_POWER / self.MAX_POWER_DISTANCE)
                        velocity[1] *= (Ball.MAX_POWER / self.MAX_POWER_DISTANCE)
                        self.ball.velocity = {'x': velocity[0], 'y': velocity[1]}
                        self.ball.powerLvl = 0
                        self.ball.state = Ball.MOVING
                        
            # Update and display the game every frame
            dt = clock.tick(fps) / 1000
            self.updateGame(dt)
            self.displayGame()
            pygame.display.update()
              
        # Quit the game          
        pygame.quit()
        
    # Update the games components every frame
    def updateGame(self, dt):
        self.ball.updateBall(dt, self.level)
    
    # Displays the games components every frame
    def displayGame(self):
        # Display the background
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.background, (480, 0))
        self.display.blit(self.background, (960, 0))
        self.display.blit(self.background, (0, 480))
        self.display.blit(self.background, (480, 480))
        self.display.blit(self.background, (960, 480))
        
        # Display the hole
        self.hole.displayHole(self.display)
        
        # Display all the objects on the map
        for object in self.level:
            object.displayObject(self.display)
            
        # Display the power level of the ball and arrow
        if self.ball.state == Ball.TAKING_SHOT:
            powerLevelX, powerLevelY = None, None
            ballPos = {'x': self.ball.position['x'] + Ball.SIZE / 2, 'y': self.ball.position['y'] + Ball.SIZE / 2}
            if ballPos['x'] < 1440 - self.POWER_LVL_BACKGROUND_SIZE[0] - Ball.SIZE * 2.5:
                powerLevelX = ballPos['x'] + Ball.SIZE * 1.5
            else:
                powerLevelX = ballPos['x'] - Ball.SIZE * 1.5 - self.POWER_LVL_BACKGROUND_SIZE[0]
            if ballPos['y'] < 786 - self.POWER_LVL_BACKGROUND_SIZE[1] - Ball.SIZE * 2.5:
                powerLevelY = ballPos['y'] + Ball.SIZE * 1.5
            else:
                powerLevelY = ballPos['y'] - Ball.SIZE * 1.5 - self.POWER_LVL_BACKGROUND_SIZE[1]

            powerLvlBackground = pygame.Rect((powerLevelX, powerLevelY), (self.POWER_LVL_BACKGROUND_SIZE[0], self.POWER_LVL_BACKGROUND_SIZE[1]))
            pygame.draw.rect(self.display, (0, 0, 0), powerLvlBackground, 0, 5)
            
            powerLevelBarY = math.floor(100 * self.ball.powerLvl)
            powerLvlRect = pygame.Rect((powerLevelX + 5, powerLevelY + 5 + (100 - powerLevelBarY)), (30, powerLevelBarY))
            pygame.draw.rect(self.display, (0, 255, 0), powerLvlRect, 0)
            
            pygame.draw.line(self.display, (0, 0, 0), (self.ball.position['x'] + Ball.SIZE / 2, self.ball.position['y'] + Ball.SIZE / 2), self.ball.arrowPosition, 4)
            
        # Display the ball
        self.ball.displayBall(self.display)