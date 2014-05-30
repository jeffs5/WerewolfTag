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
        self.player_number = 0
        self.GAME_LENGTH = 30
        self.mode = 0
        self.loading = False
        self.ready = False
        self.running = True
        self.FRAMERATE = 60
        self.clock = pygame.time.Clock()
        self.now = time.time()

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
        self.screen = pygame.display.set_mode((640, 440))
        self.myfont = pygame.font.SysFont("monospace", 16)

    def display(self):

                 #start screen
        if self.m.mode == 0:
            self.screen.fill((0, 0, 0))
            self.print_title()

        #countdown screen       
        elif self.m.mode == 1:
            # clear screen
            self.screen.fill((0, 0, 0))

            time_up = self.m.now + 5
            if time.time() < time_up:
                instructions = self.myfont.render("Get Ready to start!", 1, (255,255,255))
                countdown = self.myfont.render("{0}".format(int(time_up-time.time()) + 1) , 1, (255,255,255))
                self.screen.blit(instructions, (210, 210))
                self.screen.blit(countdown, (300, 230))

        #actual game
        elif self.m.mode == 2:
            ## change for time
            time_up = self.m.now + self.m.GAME_LENGTH
            if time.time() >= time_up:
                self.m.mode = 3

            else:
                # take out?
                # clock.tick(self.m.FRAMERATE)


                # Draw the scene
                self.screen.fill((0, 0, 0))


                #check to see if any player is still transforming
                for player in self.m.players:
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

                    player.draw_player(self.screen)
                display_number = self.m.player_number + 1
                self.print_game_stats(time_up)

        #once the time is up!
        if self.m.mode == 3:
            backgroundColor = (0,0,0)
            self.screen.fill(backgroundColor)
            self.print_end_game()

        pygame.display.flip()

    ########## Print Screens ###################

    def print_title(self):
        title = self.myfont.render("Werewolf Tag", 1, (255,255,255))
        intro_message = self.myfont.render("You are player {0}".format(self.m.player_number + 1), 1, (255,255,255))
        instructions = self.myfont.render("Press SPACE to Start Countdown", 1, (255,255,255))
        self.screen.blit(title, (240, 10))
        self.screen.blit(intro_message, (210, 190))
        self.screen.blit(instructions, (160, 210))

    def print_game_stats(self, time_up):
        display_number = self.m.player_number + 1

        player_score = self.myfont.render(
            "Player: {0}, score: {1}".format(display_number, self.m.players[self.m.player_number].get_score()), 1, (255,255,255))
        time_left = self.myfont.render("Time left: {0}".format(time_up-time.time() + 1), 1, (255,255,255))
        self.screen.blit(player_score, (16, 400))
        self.screen.blit(time_left, (220, 10))

    def print_end_game(self):
        time_up = self.myfont.render("Time's Up!", 1, (255,255,255))
        winner = self.select_winner(self.m.players)
        winner_number = winner.get_player_number() + 1
        winner_text = self.myfont.render(
            "The winner is: Player {0} with a score of {1}".format(winner_number, winner.get_score()), 1, (255,255,255))
        your_text = self.myfont.render("Your score was: {0} ".format(self.m.players[self.m.player_number].get_score()), 1, (255,255,255))
        restart_text = self.myfont.render("Press Space to continue", 1, (255,255,255))

        self.screen.blit(time_up, (240, 10))
        self.screen.blit(winner_text, (110, 210))
        self.screen.blit(your_text, (200, 225))
        self.screen.blit(restart_text, (180, 235))

    def select_winner(self, players):
        winner = self.m.players[0]
        for player in self.m.players:
            if player.get_score() > winner.get_score():
                winner = player

        return winner


##################  CONTROLLER #######################

class Controller():
    def __init__(self, model, network):
        self.m = model
        self.n = network
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

            if key[pygame.K_SPACE]:
                if not self.m.loading:
                    self.m.loading = True
                    return "load"

        #countdown screen       
        elif self.m.mode == 1:

            self.m.time_up = self.m.now + 5

            if not self.m.ready:
                self.m.ready = True
                return "ready"

        #actual game
        elif self.m.mode == 2:
            ## change for time
            time_up = self.m.now + self.m.GAME_LENGTH
            if time.time() >= time_up:
                self.m.mode = 3

            else:
                self.m.clock.tick(self.m.FRAMERATE)

                # Move the player if an arrow key is pressed

                for pressed in self.controls:
                    if key[pressed]:
                        instruction = self.controls.get(pressed)
                        moving_player = self.m.players[self.m.player_number]

                        #if the player has an attribute check if they can still move
                        if len(moving_player.attributes) > 0:
                            for attribute in moving_player.attributes:
                                if attribute != "transforming":
                                    ##problem since it returns on the first one
                                   n.do_send({'move': instruction, 'player': self.m.player_number})
                        else:
                            n.do_send({'move': instruction, 'player': self.m.player_number})

                #check to see if any player is still transforming
                for player in self.m.players:
                    player.increase_score(1)
                    for attribute in player.attributes:
                        if attribute == "transforming":
                            if time.time() >= player.transform_complete:
                                player.finish_transform()

                            #counter used to determine which transformation animation should be shown
                            player.transform_counter += 1

        #once the time is up!
        elif self.m.mode == 3:

            if key[pygame.K_SPACE]:
                self.m.mode = 0

        return "no message"


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
            player = self.m.players[moved_player]
            self.move_player(player, msg['move'])

            #used for error handling
        else:
            print msg

    def move_player(self, player, instruction):
        player.move(instruction[0], instruction[1], self.m.borders, self.m.players)

    def send_message(self, message):
        self.do_send(message)

    def poll_messages(self):
        poll()
        sleep(.05)


#################  MAIN LOOP  ####################

host, port = 'localhost', 8888

m = Model()
v = View(m)
n = NetworkController(m, host, port)
c = Controller(m,n )

while m.running:
    try:
        # Network Controller 
        n.poll_messages()
        message = c.get_commands()
        n.send_message(message)
        v.display()

    except KeyboardInterrupt:
        n.do_send({'close' : 'close'})
        n.do_close()
        exit()
