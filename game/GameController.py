#
# python imports
#
import time
import random
import pygame
from base import Globals

#
# Game Controller Class Module
#
class GameController():
    #
    # default constructor
    #
    def __init__(self, model, network):
        self.m = model
        self.n = network
        self.controls = {pygame.K_LEFT : (-1, 0, Globals.DIRECTION_LEFT), pygame.K_RIGHT : (1, 0, Globals.DIRECTION_RIGHT), pygame.K_UP : (0, -1, Globals.DIRECTION_UP), pygame.K_DOWN : (0, 1, Globals.DIRECTION_DOWN), pygame.K_c : (1, 1, Globals.DIRECTION_NONE)}
    
    #
    # get commands
    #
    def get_commands(self):
        # get key pressed
        key = pygame.key.get_pressed()
        
        # loop through events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.m.running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.m.running = False

        # game is still running
        if not self.m.game_running:
            # start screen
            if self.m.mode == 0:
                if key[pygame.K_SPACE]:
                    if not self.m.loading:
                        self.m.loading = True
                        return "load"
                   
            # countdown screen       
            elif self.m.mode == 1:
                time_up = self.m.now + 5
                if time.time() >= time_up:
                    return "ready"

            # actual game
            elif self.m.mode == 2:
                # # change for time
                time_up = self.m.now + self.m.GAME_LENGTH
                if time.time() >= time_up:
                    self.m.mode = 3

                else:
                    self.m.clock.tick(self.m.FRAMERATE)

                    # Move the player if an arrow key is pressed
                    for pressed in self.controls:
                        if key[pressed]:
                            if pressed == pygame.K_c: 
                                if not (self.m.players[str(self.m.player_number)]).is_it:
                                    # instruction = self.controls.get(pressed)
                                    moving_player = self.m.players[str(self.m.player_number)]
                                    placeable = moving_player.place_placeable()
                                    # change for correct placeing
                                    self.n.do_send({'place': True, 'x': random.randint(0, self.m.board_x - 30), 'y': random.randint(0, self.m.board_y - 30), 'name': placeable})
                            else:
                                instruction = self.controls.get(pressed)
                                moving_player = self.m.players[str(self.m.player_number)]

                                if not moving_player.transforming:
                                    self.n.do_send({'move': instruction, 'player': self.m.player_number})

                    # check to see if any player is still transforming
                    for player in self.m.players.values():
                        if not player.is_it and not player.transforming:
                            player.increase_score(1)
                        if player.transforming:
                            # update player transforming animation
                            player.on_transforming()
                            
                            if time.time() >= player.transform_complete:
                                player.finish_transform()

                                # counter used to determine which transformation animation should be shown
                                player.transform_counter += 1

                    for powerup in self.m.powerups:
                        if not powerup.active:
                            self.m.powerups.remove(powerup)

                    for placeable in self.m.placeables:
                        if not placeable.active:
                            self.m.placeables.remove(placeable)

            # once the time is up!
            elif self.m.mode == 3:
                if not self.m.score_sent:
                    self.m.score_sent = True
                    self.n.do_send({'player_number': self.m.player_number, 'score': self.m.players[str(self.m.player_number)].get_score()})
                    
                if key[pygame.K_SPACE]:
                    self.running = False
                    return "restart"
                
        # no messages to send
        return "no message"
