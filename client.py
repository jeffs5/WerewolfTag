from network import Handler, poll
import sys
from threading import Thread
from time import sleep
import os
import random
import pygame
import Player
import time

players = []
player_number = None 

class Client(Handler): 

    def on_close(self):
        pass
    
    def on_msg(self, msg):
        global players, mode, now, player_number

        if 'join' in msg:
            player_number = msg['join'] 

        elif 'load' in msg:
            mode = 1
            now = time.time()

        elif 'start_state' in msg:
            init_game(msg['start_state'])
            mode = 2
            now = time.time()  

        elif 'move' in msg:
            moved_player = msg['player']
            player = players[moved_player]
            move_player(player, msg['move'])

        else:
            print msg

        
host, port = 'localhost', 8888
client = Client(host, port)

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds
  

#############################

def select_winner(players):
    winner_player = players[0]
    for player in players:
        if player.get_score() > winner_player.get_score():
            winner_player = player

    return winner_player

############################

def init_game(player_msg):
    number = 1
    for player in player_msg.items():
        player_info = player[1]
        x_axis = player_info[0]
        y_axis = player_info[1]
        new_player = Player.Player(x_axis, y_axis, number , players)

        if player_info[2] == 'wolf':
            new_player.becomes_it()

        number += 1

        players.append(new_player)

#############################

def move_player(player, instruction):
    player.move(instruction[0], instruction[1], borders, players)

############ MAIN GAME LOOP ##########################

# thread = Thread(target=periodic_poll)
# thread.daemon = True  # die when the main thread dies 
# thread.start()

###########################

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Play Tag!")
screen = pygame.display.set_mode((640, 440))

mode = 0
ready = False

borders = [pygame.Rect(0,0, 640, 1), pygame.Rect(0,0, 1, 440), pygame.Rect(639,0, 1, 440), pygame.Rect(0,439, 640, 1)]

myfont = pygame.font.SysFont("monospace", 16)

running = True
FRAMERATE = 60
clock = pygame.time.Clock()
now = time.time()

controls = {pygame.K_LEFT : (-1,0), pygame.K_RIGHT : (1,0), pygame.K_UP : (0,-1), pygame.K_DOWN : (0,1)} # player controls

while running:
    try:
        poll()
        key = pygame.key.get_pressed()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False

        #start screen
        if mode == 0:
            title = myfont.render("Werewolf Tag", 1, (255,255,255))
            intro_message = myfont.render("You are player " + str(player_number), 1, (255,255,255))
            instructions = myfont.render("Press SPACE to Start Countdown", 1, (255,255,255))
            screen.blit(title, (240, 10))
            screen.blit(intro_message, (210, 190))
            screen.blit(instructions, (160, 210))

            if key[pygame.K_SPACE]:
                client.do_send("load")

        #get ready stage        
        if mode == 1:
            # clear screen
            screen.fill((0, 0, 0))

            time_up = now + 5
            if time.time() < time_up:
                instructions = myfont.render("Get Ready to start!", 1, (255,255,255))
                countdown = myfont.render("{0}".format(int(time_up-time.time()) + 1) , 1, (255,255,255))
                screen.blit(instructions, (210, 210))
                screen.blit(countdown, (300, 230))
            elif ready == False:
                ready = True
                client.do_send("ready")

        #actual game
        if mode == 2:
            time_up = now + 60
            if time.time() >= time_up:
                mode = 3

            else:
                clock.tick(FRAMERATE)

                # Move the player if an arrow key is pressed

                for pressed in controls:
                    if key[pressed]:
                        instruction = controls.get(pressed)
                        moving_player = players[player_number]

                        #if the player has an attribute check if they can still move
                        if len(moving_player.attributes) > 0:
                            for attribute in moving_player.attributes:
                                if attribute != "transforming":
                                    client.do_send({'move': instruction, 'player': moving_player.get_player_number()})
                        else:
                            client.do_send({'move': instruction, 'player': moving_player.get_player_number()})


                # Draw the scene
                screen.fill((0, 0, 0))


                #check to see if any player is still transforming
                for player in players:
                    player.increase_score(1)
                    for attribute in player.attributes:
                        if attribute == "transforming":
                            if time.time() >= player.transform_complete:
                                player.finish_transform()

                            #randomly tested modulo numbers were used for the animation
                            elif player.transform_counter %18 == 1:
                                player.color = (255, 255, 255)
                            elif player.transform_counter %6 == 1:
                                player.color = (255, 0, 0)

                            #counter used to determine which transformation animation should be shown
                            player.transform_counter += 1

                    player.draw_player(screen)

                disclaimertext = myfont.render("Player 1 score: {0}".format(players[0].get_score()) , 1, (255,255,255))
                disclaimertext3 = myfont.render("Time left: {0}".format(round(time_up-time.time(), 2)) , 1, (255,255,255))
                screen.blit(disclaimertext, (16, 400))
                screen.blit(disclaimertext3, (200, 10))

        #once the time is up!
        if mode == 3:
            backgroundColor = (0,0,0)
            screen.fill(backgroundColor)

            time_up = myfont.render("Time's Up!", 1, (255,255,255))
            winner = select_winner(players)
            winner_text = myfont.render("The winner is: Player " + str(winner.get_player_number()), 1, (255,255,255))
            restart_text = myfont.render("Press Space to continue", 1, (255,255,255))

            screen.blit(time_up, (240, 10))
            screen.blit(winner_text, (210, 210))
            screen.blit(restart_text, (210, 220))

            if key[pygame.K_SPACE]:
                players = []
                mode = 0

        pygame.display.flip()


    except KeyboardInterrupt:
        client.do_send({'close' : 'close'})
        client.do_close()
        exit()