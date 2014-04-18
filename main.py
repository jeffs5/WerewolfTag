#! /usr/bin/env python

import os
import random
import pygame

# Class for the orange dude

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

myfont = pygame.font.SysFont("monospace", 16)

running = True
FRAMERATE = 60
clock = pygame.time.Clock()

while running:
    clock.tick(FRAMERATE)
    
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
   
    disclaimertext = myfont.render("Player 1 score: {0}".format(player.getScore()) , 1, (255,255,255))
    disclaimertext2 = myfont.render("Player 2 score: {0}".format(player2.getScore()) , 1, (255,255,255))
    screen.blit(disclaimertext, (16, 400))
    screen.blit(disclaimertext2, (16, 410))

    pygame.display.flip()
    
