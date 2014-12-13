'''
Created on Nov 14, 2014

@author: Jon
'''
import pygame
from base.Sprite import Sprite

class Human(Sprite):
    xSpeed = 2
    ySpeed = 2
    frames = [(0,0,100,100), (50,0,100,100), (100,0,100,100),(150,0,100,100), #row1
              (0,50,50,50), (50,50,50,50), (100,50,50,50), (150,50,50,50), #row2
              (0,100,50,50), (50,100,50,50), (100,100, 50, 50), (150,100, 50, 50),#row3
              (0,150,50,50), (50,150,50,50), (100, 150, 50, 50), (150, 150,50,50) ] #row4
    currentFrame = frames[0]
    
    def __init__(self):
        self.surface = pygame.image.load("assets/sprites/human.png")
        self.width=200
        self.height=200
        self.offsetX=20
        self.offsetY=0
        #self.surface.scroll(self.offsetX,self.offsetY)
    def moveUp(self):
        self.y-=self.ySpeed
        self.currentFrame = self.frames[2]
    def moveDown(self):
        self.y+=self.ySpeed
        self.currentFrame = self.frames[0]
    def moveLeft(self):
        self.x-=self.xSpeed
        self.currentFrame = self.frames[1]
    def moveRight(self):
        self.x+=self.xSpeed
        self.currentFrame = self.frames[3]
        
    def update(self):
        self.offsetX = self.currentFrame[0]
        self.offsetY = self.currentFrame[1]
        self.width = self.currentFrame[2]
        self.height = self.currentFrame[3]
        
        
    