import os
import random
import pygame
import time

class Trap(object):

    def __init__(self, x, y, effect):
        self.effect = effect
        self.rect = pygame.Rect(x, y, 8, 8)
        self.color = (122,122,122)

    def applyEffect(self, player):
    	if self.effect == boost:
    		player.speed *= 2