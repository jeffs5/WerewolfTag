#
# python imports
#
import pygame

#
# Sprite Class Module
#
class Sprite:
    #
    # default constructor
    #
    def __init__(self):
        self.offsetX = 0
        self.offsetY = 0
        self.rect = pygame.Rect(0, 0, 0, 0) 
        self.surface = None
        
    #
    # draw sprite
    #
    def draw(self, screen):
        # validate drawing surface
        if self.surface != None:
            # draw surface to screen
            screen.blit(self.surface, (self.rect.x, self.rect.y), pygame.Rect(self.offsetX, self.offsetY, self.rect.width, self.rect.height))
            
    # 
    # update frame helper method
    #
    def updateFrame(self, frame):
        # update sprite frame
        self.offsetX = frame[0]
        self.offsetY = frame[1]
        self.rect.width = frame[2]
        self.rect.height = frame[3]
