from network import Listener, Handler, poll
import Player
from time import sleep
import time
import random

handlers = {}  # map client handler to user name
players = {}
players_ready = 0
game_running = False

#########################################

def distribute_msg(msg):
    for handler in handlers:
        handler.do_send(msg)

def create_players():
    for player in handlers:
        x_axis = random.randint(0, 624)
        y_axis = random.randint(0, 424)
        while colliding(x_axis, y_axis):
            x_axis = random.randint(0, 624)
            y_axis = random.randint(0, 424)
            # print "colliding: " + str(x_axis) + ", " + str(y_axis)
        player_number = handlers[player] 
        players[player_number] = [x_axis, y_axis, "human"]

# randomly selects a player to be it at the start of the game
# the "it" player number is the random number + 1
def choose_wolf():
    it_player = random.randint(0, len(players) - 1)
    players[it_player][2] = 'wolf'

def colliding(x1, y1):
    width = 16
    height = 16
    for player in players.items():
        x2 = player[1][0]
        y2 = player[1][1]
        # print str(x1) + ", " + str(y1) + ": " + str(x2) + ", " + str(y2)
        return x1 < x2 + width and y1 < y2 + height and x2 < x1 + width and y2 < y1 + height

###########################################

class MyHandler(Handler):
    
    # def send_all(message):
    #     for i in 
    def on_open(self):
        global handlers, game_running
        player_number = len(handlers)
        handlers[self] = player_number
        self.do_send({'join': player_number, 'game_running': game_running})
        
    def on_close(self):
        global players_ready, players, handlers
        del(handlers[self])
        players = {}
        players_ready = 0
    
    def on_msg(self, msg):
        global players_ready, players, game_running

        if 'move' in msg:
            distribute_msg(msg)
        elif 'load' in msg:
            distribute_msg(msg)
        elif 'ready' in msg:
            #once all clients have finished counting down/are ready, 
            #the players will be "created" and sent out
            players_ready += 1
            if players_ready == len(handlers):
                create_players()
                choose_wolf()
                game_running = True
                distribute_msg({"start_state": players})
        elif 'restart' in msg:
           game_running = False
           distribute_msg({"restart": 'restart'})
           handlers = {}  # map client handler to user name
           players = {}
           players_ready = 0
        else:
            print msg

#########################################

class Serv(Listener):
    handlerClass = MyHandler


port = 8888
server = Serv(port)
while 1:
    try:
        poll()
        sleep(0.05)  # seconds
    except KeyboardInterrupt:
        server.close()
        exit("\n")
        