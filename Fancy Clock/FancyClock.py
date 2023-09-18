import pygame
import math
import datetime as dt

SCREEN_SIZE = 500
CLOCK_DISTANCE = 40
SCALE = 4

CENTER = SCREEN_SIZE / 2
SEC_D = SCREEN_SIZE - CLOCK_DISTANCE
MIN_D = SCREEN_SIZE - CLOCK_DISTANCE * 2
HOUR_D =  SCREEN_SIZE - CLOCK_DISTANCE * 3

BLACK = (0, 0, 0)
PINK = (222, 92, 147)
PURPLE = (128, 81, 222)
GREEN = (176, 246, 126)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Fancy Clock")
    image = pygame.image.load("Clock.png")
    pygame.display.set_icon(image)
    
    running = True
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        now = dt.datetime.now()
        sec = now.second
        min = now.minute
        hour = now.hour % 12 # 12 hour clock
        
        if sec == 0:
            sec = 60
        if min == 0:
            min = 60
        if hour == 0:
            hour = 12
            
        secAngle = sec * math.pi / 30
        minAngle = min * math.pi / 30
        hourAngle = hour * math.pi / 6
        
        pygame.draw.arc(screen, PINK, [CLOCK_DISTANCE / 2, CLOCK_DISTANCE / 2, SEC_D, SEC_D], 0, secAngle, SCALE)
        pygame.draw.arc(screen, PURPLE, [CLOCK_DISTANCE, CLOCK_DISTANCE, MIN_D, MIN_D], 0, minAngle, SCALE)
        pygame.draw.arc(screen, GREEN, [CLOCK_DISTANCE / 2 * 3, CLOCK_DISTANCE / 2 * 3, HOUR_D, HOUR_D], 0, hourAngle, SCALE)
        
        pygame.draw.line(screen, GREEN, (CENTER, CENTER), (CENTER + math.cos(hourAngle) * ((HOUR_D) / 2), CENTER + math.sin(hourAngle) * -((HOUR_D) / 2)), SCALE)
        pygame.draw.line(screen, PURPLE, (CENTER, CENTER), (CENTER + math.cos(minAngle) * ((MIN_D) / 2), CENTER + math.sin(minAngle) * -((MIN_D) / 2)), SCALE)
        pygame.draw.line(screen, PINK, (CENTER, CENTER), (CENTER + math.cos(secAngle) * ((SEC_D ) / 2), CENTER + math.sin(secAngle) * -((SEC_D) / 2)), SCALE)

        screen.blit(pygame.transform.rotate(screen, 90), (math.sin(sec * math.pi / 30), 0))
        screen.blit(pygame.transform.flip(screen, True, False), (0, 0))
                
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()