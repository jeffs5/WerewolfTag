from network import Handler, poll
import sys
from threading import Thread
from time import sleep
import os
import random
import pygame
import Player
import time


##################  MODEL ############################


class Model():
    def __init__(self):
        self.players = []
        self.borders = [pygame.Rect(0,0, 640, 1), pygame.Rect(0,0, 1, 440), pygame.Rect(639,0, 1, 440), pygame.Rect(0,439, 640, 1)]
        self.player_numer = None
        self.GAME_LENGTH = 30
        mode = 0
        loading = False
        ready = False
        running = True
        FRAMERATE = 40
        clock = pygame.time.Clock()
        now = time.time()

    def init_game(self, player_msg):

        for player in player_msg.items():
            # player[0] is player_number
            # player[1] is instruction
            # player[2] is player type
            player_info = player[1]
            x_axis = player_info[0]
            y_axis = player_info[1]
            new_player = Player.Player(x_axis, y_axis, player[0])

            if player_info[2] == 'wolf':
                new_player.becomes_it()

            self.players.append(new_player)


##################  VIEW #############################

class View():
    def __init__(self, model):
        self.m = model

        # Initialise pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        # Set up the display
        pygame.display.set_caption("Play Tag!")
        screen = pygame.display.set_mode((640, 440))
        myfont = pygame.font.SysFont("monospace", 16)

    def display(self):
        pygame.display.flip()

    ########## Print Screens ###################

    def print_title():
        title = myfont.render("Werewolf Tag", 1, (255,255,255))
        intro_message = myfont.render("You are player {0}".format(player_number + 1), 1, (255,255,255))
        instructions = myfont.render("Press SPACE to Start Countdown", 1, (255,255,255))
        screen.blit(title, (240, 10))
        screen.blit(intro_message, (210, 190))
        screen.blit(instructions, (160, 210))

    def print_game_stats():
        player_score = myfont.render(
            "Player: {0}, score: {1}".format(display_number, players[player_number].get_score()) , 1, (255,255,255))
        time_left = myfont.render("Time left: {0}".format(int(time_up-time.time()) + 1) , 1, (255,255,255))
        screen.blit(player_score, (16, 400))
        screen.blit(time_left, (220, 10))

    def print_end_game():
        time_up = myfont.render("Time's Up!", 1, (255,255,255))
        winner = select_winner(players)
        winner_number = winner.get_player_number() + 1
        winner_text = myfont.render(
            "The winner is: Player {0} with a score of {1}".format(winner_number, winner.get_score()), 1, (255,255,255))
        your_text = myfont.render("Your score was: {0} ".format(players[player_number].get_score()), 1, (255,255,255))
        restart_text = myfont.render("Press Space to continue", 1, (255,255,255))

        screen.blit(time_up, (240, 10))
        screen.blit(winner_text, (110, 210))
        screen.blit(your_text, (200, 225))
        screen.blit(restart_text, (180, 235))


##################  CONTROLLER #######################

class Controller():
    def __init__(self, model):
        self.m = model
        self.controls = {pygame.K_LEFT : (-1,0), pygame.K_RIGHT : (1,0), pygame.K_UP : (0,-1), pygame.K_DOWN : (0,1)} # player controls

        
    def get_commands(self):
        key = pygame.key.get_pressed()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.m.running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.m.running = False

         #start screen
        if self.m.mode == 0:
            screen.fill((0, 0, 0))
            print_title()

            if key[pygame.K_SPACE]:
                if not self.m.loading:
                    self.m.loading = True
                    client.do_send("load")

        #countdown screen       
        if self.m.mode == 1:
            # clear screen
            screen.fill((0, 0, 0))

            time_up = self.m.now + 5
            if time.time() < time_up:
                instructions = myfont.render("Get Ready to start!", 1, (255,255,255))
                countdown = myfont.render("{0}".format(int(time_up-time.time()) + 1) , 1, (255,255,255))
                screen.blit(instructions, (210, 210))
                screen.blit(countdown, (300, 230))
            elif self.m.ready == False:
                self.m.ready = True
                return "ready"

        #actual game
        if self.m.mode == 2:
            ## change for time
            time_up = now + self.m.GAME_LENGTH
            if time.time() >= time_up:
                self.m.mode = 3

            else:
                clock.tick(self.m.FRAMERATE)

                # Move the player if an arrow key is pressed

                for pressed in self.controls:
                    if key[pressed]:
                        instruction = self.controls.get(pressed)
                        moving_player = self.m.players[self.m.player_number]

                        #if the player has an attribute check if they can still move
                        if len(moving_player.attributes) > 0:
                            for attribute in moving_player.attributes:
                                if attribute != "transforming":
                                   return {'move': self.m.instruction, 'player': self.m.player_number}
                        else:
                            return {'move': self.m.instruction, 'player': self.m.player_number}


                # Draw the scene
                screen.fill((0, 0, 0))


                #check to see if any player is still transforming
                for player in self.m.players:
                    player.increase_score(1)
                    for attribute in player.attributes:
                        if attribute == "transforming":
                            if time.time() >= player.transform_complete:
                                player.finish_transform()

                            #randomly tested modulo numbers were used for the animation
                            elif player.transform_counter % 18 == 1:
                                player.color = (255, 255, 255)
                            elif player.transform_counter % 6 == 1:
                                player.color = (255, 0, 0)

                            #counter used to determine which transformation animation should be shown
                            player.transform_counter += 1

                    player.draw_player(screen)
                display_number = player_number + 1
                print_game_stats()

        #once the time is up!
        if self.m.mode == 3:
            backgroundColor = (0,0,0)
            screen.fill(backgroundColor)
            print_end_game()

            if key[pygame.K_SPACE]:
                self.m.mode = 0


    def move_player(player, instruction):
        player.move(instruction[0], instruction[1], borders, players)

    def select_winner(players):
    winner = players[0]
    for player in players:
        if player.get_score() > winner.get_score():
            winner = player

    return winner

##################  NETWORK CONTROLLER ###############

class NetworkController(Handler): 

    def __init__(self, model, host, port):
        Handler.__init__(self, host, port)
        self.m = model

    def on_close(self):
        pass ## no need for it to do anything
    
    def on_msg(self, msg):

        # updates model
        if 'join' in msg:
            self.m.player_number = msg['join'] 

        elif 'load' in msg:
            self.m.loading = False
            self.m.mode = 1
            self.m.now = time.time()

        elif 'start_state' in msg:
            self.m.init_game(msg['start_state'])
            self.m.mode = 2
            self.m.now = time.time()  

        elif 'move' in msg:
            moved_player = msg['player']
            player = players[moved_player]
            move_player(player, msg['move'])

            #used for error handling
        else:
            print msg

    def send_message(self,message):
        client.do_send(message)

    def poll_messages(self):
        poll(.05)


#################  MAIN LOOP  ####################

host, port = 'localhost', 8888
client = Client(host, port)

m = Model()
v = View(m)
c = Controller(c)
n = NetworkController(m, host, port)

while running:
    try:
        # Network Controller 
        n.poll_messages()
        message = c.get_commands
        n.send_message(message)
        v.display()

    except KeyboardInterrupt:
        client.do_send({'close' : 'close'})
        client.do_close()
        exit()
