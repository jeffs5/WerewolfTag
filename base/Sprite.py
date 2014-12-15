'''
Created on Nov 10, 2014

@author: Jon, Angel
'''
import pygame

class Sprite:
    x = 0
    y = 0
    width = 0
    height = 0
    offsetX = 0
    offsetY = 0
    surface = None
    def __init__(self):
        pass  # load in sprite later here
    def draw(self, window):
        if self.surface != None:
            window.blit(self.surface, (self.x, self.y), pygame.Rect(self.offsetX, self.offsetY, self.width, self.height))
    
    
