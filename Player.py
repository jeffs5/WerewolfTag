import os
import random
import pygame

class Player(object):

    def __init__(self, x, y, value, players):
        self.playerNumber = value
        players.append(self)
        self.rect = pygame.Rect(x, y, 16, 16)

    def move(self, dx, dy, borders, players):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0, borders, players)
        if dy != 0:
            self.move_single_axis(0, dy, borders, players)
    
    def getScore(self):
        return int(self.playerNumber)

    def move_single_axis(self, dx, dy, borders, players):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for border in borders:
            if self.rect.colliderect(border):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = border.left
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = border.right
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = border.top
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = border.bottom

        for player in players:
                if self != player:
                    if self.rect.colliderect(player.rect):
                        raise SystemExit, "Player" + str(self.playerNumber) + " Has tagged the other player"

        # self.playerNumber += 1 to add score we must add another parameter in the player object for playerScore