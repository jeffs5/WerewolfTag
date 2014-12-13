import pygame
import os
import random
import pygame
import time
from Powerup import Powerup

class Placeable(object):

    def __init__(self, x, y, type):
    	self.rect = pygame.Rect(x, y, 25, 25)
    	self.type = type
    	self.active = True
    	self.color = (0,0, 0)

    	if self.type == 'hole':
    		self.color = (125, 125, 125)

    	if self.type == 'wall':
    		self.color = (125, 0, 125)

    def draw_placeable(self, screen):
    		pygame.draw.rect(screen, self.color, self.rect)

    def trigger_hole(self):
        self.active = False