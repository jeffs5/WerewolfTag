#
# python imports
#
import sys
import os
import time
from time import sleep
from powerups.Powerup import Powerup
from powerups.Placeable import Placeable
from network.NetworkHandler import NetworkHandler, poll

#
# Client Handler Class Module
#
class ClientHandler(NetworkHandler): 
    
    #
    # default constructor
    #
    def __init__(self, model, host, port):
        NetworkHandler.__init__(self, host, port)
        self.m = model

    #
    # poll messages
    #
    def poll_messages(self):
        poll()
        sleep(.02)
        
    #
    # send message out
    #
    def send_message(self, message):
        self.do_send(message)
        
    #
    # on close event
    #
    def on_close(self):
        pass
    
    #
    # on message event
    #
    def on_msg(self, msg):
        # updates model
        if 'join' in msg:
            self.m.player_number = msg['join']
            self.m.game_running = msg['game_running']

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
            player = self.m.players[str(moved_player)]
            self.move_player(player, msg['move'])

        elif 'powerup' in msg:
            self.m.powerups.append(Powerup (msg['x'], msg['y'], msg['name']))

        elif 'place' in msg:
            if msg['name'] is not None:
                self.m.placeables.append(Placeable (msg['x'], msg['y'], msg['name']))

        elif 'winner_number' in msg:
            self.m.winner_number = msg['winner_number']
            self.m.winner_score = msg['winner_score']

        elif 'restart' in msg:
            python = sys.executable
            os.execl(python, python, * sys.argv)
            sys.exit()
        else:
            print msg

    #
    # move player helper method
    #
    def move_player(self, player, instruction):
        player.move(instruction[0], instruction[1], instruction[2], self.m.borders, self.m.players.values(), self.m.powerups, self.m.placeables)
