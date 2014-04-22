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
now = time.time()
time_up = now + 60

controls = {pygame.K_LEFT : (-2,0, player1), pygame.K_RIGHT : (2,0, player1), pygame.K_UP : (0,-2, player1), pygame.K_DOWN : (0,2, player1)} # player 1 controls
controls.update({pygame.K_a : (-2,0, player2), pygame.K_d : (2,0, player2), pygame.K_w : (0,-2, player2), pygame.K_s : (0,2, player2)}) # player 2 controls

############ MAIN GAME LOOP ##########################

choose_it(players)

while running:
    if time.time() >= time_up:
        running = False

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
            instruction = controls.get(pressed)
            moving_player = instruction[2]

            # used to know what instruction players are currently going to see if they can be pushed
            # instruction[2].current_dir = (instruction[0], instruction[1])

            #if the player has an attribute check if they can still
            if len(moving_player.attributes) > 0:
                for attribute in moving_player.attributes:
                    if attribute != "transforming":
                        moving_player.move(instruction[0], instruction[1], borders, players)
            else:
                moving_player.move(instruction[0], instruction[1], borders, players)

    # Draw the scene
    screen.fill((0, 0, 0))

    for player in players:
        for attribute in player.attributes:
            if attribute == "transforming":
                if time.time() >= player.transform_complete:
                    player.finish_transform()
                elif player.transform_counter %18 == 1:
                    player.color = (255, 255, 255)
                elif player.transform_counter %6 == 1:
                    player.color = (255, 0, 0)

                player.transform_counter += 1

        player.draw_player(screen)
   
    disclaimertext = myfont.render("Player 1 score: {0}".format(player1.getScore()) , 1, (255,255,255))
    disclaimertext2 = myfont.render("Player 2 score: {0}".format(player2.getScore()) , 1, (255,255,255))
    disclaimertext3 = myfont.render("Time left: {0}".format(round(time_up-time.time(), 2)) , 1, (255,255,255))
    screen.blit(disclaimertext, (16, 400))
    screen.blit(disclaimertext2, (16, 410))
    screen.blit(disclaimertext3, (200, 10))

    pygame.display.flip()
    
