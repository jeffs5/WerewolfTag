import os
import random
import pygame

class Player(object):

    score = 0

    def __init__(self, x, y, value, players):
        self.playerNumber = value
        players.append(self)
        self.rect = pygame.Rect(x, y, 16, 16)
        self.color = (255,255,255)
        self.is_it = False

    def move(self, dx, dy, borders, players):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0, borders, players)
            if self.is_it == False:
                self.score = self.score + 1
        if dy != 0:
            self.move_single_axis(0, dy, borders, players)
            if self.is_it == False:
                self.score = self.score + 1
    
    def getScore(self):
        return self.score

    def becomes_it(self):
        self.color = (255, 0, 0)
        self.is_it = True
        #set speed to faster!

    def becomes_not_it(self):
        self.color = (255, 255, 255)
        self.is_it = False

    def is_it(self):
        return is_it

    def move_single_axis(self, dx, dy, borders, players):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall
        for border in borders:
            if self.rect.colliderect(border):
                if dx > 0: 
                    self.rect.right = border.left
                if dx < 0: 
                    self.rect.left = border.right
                if dy > 0: 
                    self.rect.bottom = border.top
                if dy < 0: 
                    self.rect.top = border.bottom

        for player in players:
                if self != player:
                    if self.rect.colliderect(player.rect):
                        raise SystemExit, "Player" + str(self.playerNumber) + " Has tagged the other player"

        # self.playerNumber += 1 to add score we must add another parameter in the player object for playerScore