#! /usr/bin/env python

import os
import random
import pygame

# Class for the orange dude
class Player(object):

    def __init__(self, x, y, value):
        self.playerNumber = value
        players.append(self)
        self.rect = pygame.Rect(x, y, 16, 16)

    def move(self, dx, dy):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):
        
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
                        raise SystemExit, "You tagged " + str(self.playerNumber)

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Get to the red square!")
screen = pygame.display.set_mode((640, 440))

borders = [pygame.Rect(0,0, 640, 1), pygame.Rect(0,0, 1, 440), pygame.Rect(639,0, 1, 440), pygame.Rect(0,439, 640, 1)]

players = []
player = Player(32, 32, 1) # Create the player
player2 = Player(64, 64, 2)


running = True
while running:
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    
    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if key[pygame.K_UP]:
        player.move(0, -2)
    if key[pygame.K_DOWN]:
        player.move(0, 2)

    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()

    if key[pygame.K_a]:
        player2.move(-2, 0)
    if key[pygame.K_d]:
        player2.move(2, 0)
    if key[pygame.K_w]:
        player2.move(0, -2)
    if key[pygame.K_s]:
        player2.move(0, 2)
    
    # Draw the scene
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 200, 0), player.rect)
    pygame.draw.rect(screen, (255, 200, 255), player2.rect)
    pygame.display.flip()