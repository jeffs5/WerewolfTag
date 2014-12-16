'''
Created on Nov 21, 2014

@author: Jon
'''

import pygame
from base.Sprite import Sprite

class Werewolf(Sprite):
    alphaColor = (12, 95, 63)
    xSpeed = 2
    ySpeed = 2
    frames = [ (9, 84, 31, 41), (71, 87, 37, 41), (148, 85, 36, 42), (226, 86, 31, 41),
               (289, 86, 31, 41), (354, 86, 33, 43) ]
    currentFrame = frames[0]
    
    def __init__(self):
        Sprite.__init__(self)
        self.surface = pygame.image.load("assets/sprites/werewolf.png")
        self.surface.set_colorkey(self.alphaColor)
        # self.surface.set_alpha(5)
        # self.surface.scroll(self.offsetX,self.offsetY)
    def moveUp(self):
        self.y -= self.ySpeed
        self.currentFrame = self.frames[2]
    def moveDown(self):
        self.y += self.ySpeed
        self.currentFrame = self.frames[0]
    def moveLeft(self):
        self.x -= self.xSpeed
        self.currentFrame = self.frames[1]
    def moveRight(self):
        self.x += self.xSpeed
        self.currentFrame = self.frames[3]
        
    def update(self):
        self.offsetX = self.currentFrame[0]
        self.offsetY = self.currentFrame[1]
        self.width = self.currentFrame[2]
        self.height = self.currentFrame[3]
        
        

    
