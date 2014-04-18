#! /usr/bin/env python

import os
import random
import pygame
import Player
import time

##############################

# randomly selects a player to be it at the start of the game
# the "it" player number is the random number + 1
def choose_it(players):
    it_player = random.randint(0, len(players)-1)
    players[it_player].becomes_it()

#############################

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Get to the red square!")
screen = pygame.display.set_mode((640, 440))

borders = [pygame.Rect(0,0, 640, 1), pygame.Rect(0,0, 1, 440), pygame.Rect(639,0, 1, 440), pygame.Rect(0,439, 640, 1)]

players = []
player1 = Player.Player(32, 32, 1, players) # Create the player
player2 = Player.Player(64, 64, 2, players)

myfont = pygame.font.SysFont("monospace", 16)

running = True
FRAMERATE = 60
clock = pygame.time.Clock()

controls = {pygame.K_LEFT : (-2,0, player1), pygame.K_RIGHT : (2,0, player1), pygame.K_UP : (0,-2, player1), pygame.K_DOWN : (0,2, player1)} # player 1 controls
controls.update({pygame.K_a : (-2,0, player2), pygame.K_d : (2,0, player2), pygame.K_w : (0,-2, player2), pygame.K_s : (0,2, player2)}) # player 2 controls

############ MAIN GAME LOOP ##########################

choose_it(players)

while running:
    clock.tick(FRAMERATE)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    
    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    for pressed in controls:
        if key[pressed]:
            direction = controls.get(pressed)
            direction[2].move(direction[0], direction[1], borders, players)
    
    # Draw the scene
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, player1.color, player1.rect)
    pygame.draw.rect(screen, player2.color, player2.rect)
   
    disclaimertext = myfont.render("Player 1 score: {0}".format(player1.getScore()) , 1, (255,255,255))
    disclaimertext2 = myfont.render("Player 2 score: {0}".format(player2.getScore()) , 1, (255,255,255))
    screen.blit(disclaimertext, (16, 400))
    screen.blit(disclaimertext2, (16, 410))

    pygame.display.flip()
    
