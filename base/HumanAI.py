'''
Created on Nov 16, 2014

@author: Jon
'''
import pygame
from base.Sprite import Sprite

#ai
class HumanAI(Sprite):
    xSpeed = 1
    ySpeed = 1
    frames = [(0,0,100,100), (50,0,100,100), (100,0,100,100),(150,0,100,100), #row1
              (0,50,50,50), (50,50,50,50), (100,50,50,50), (150,50,50,50), #row2
              (0,100,50,50), (50,100,50,50), (100,100, 50, 50), (150,100, 50, 50),#row3
              (0,150,50,50), (50,150,50,50), (100, 150, 50, 50), (150, 150,50,50) ] #row4
    currentFrame = frames[0]
    
    def __init__(self):
        self.surface = pygame.image.load("assets/sprites/human.png")
        self.x = 200
        self.y = 100
        self.width=100
        self.height=100
        self.offsetX=20
        self.offsetY=0
    
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

    def movePath(self, humanPlayer):
        #also check to see if the ai is in the transform state first
        
        if(self.x - humanPlayer.x == 0): #ww and human on same column
            if(self.y - humanPlayer.y > 0):
                self.moveUp()
            elif(self.y - humanPlayer.y < 0):
                self.moveDown()
        elif(self.y - humanPlayer.y == 0): #ww and human on same row
            if(self.x - humanPlayer.x > 0):
                self.moveLeft()
            elif(self.x - humanPlayer.x < 0):
                self.moveRight()
        elif(self.x - humanPlayer.x > 0): #ww is to the right of the player
            if(self.y - humanPlayer.y > 0): #ww is south of player, move northwest
                self.moveUp()
                self.moveLeft()
            else: #move southwest
                self.moveDown()
                self.moveLeft()
        else:
            if(self.y - humanPlayer.y > 0): #move northeast
                self.moveUp()
                self.moveRight()
            else: #move southeast
                self.moveDown()
                self.moveRight()

    def getSlope(self, x1, y1, x2, y2):
        m = (y2-y1) / (x2-x1) #slope
        return m
        
    def getYIntercept(self, slope, p1, p2):
        b = p2 - (slope) * (p1)
        return b

    def update(self):
        pass