from network import Listener, Handler, poll
import Player
from time import sleep
import time
import random

handlers = {}  # map client handler to user name
running_handlers = {}
players = {}
players_ready = 0
player_scores = {}
game_running = False

#########################################

#sent to the players who are in the game
def distribute_msg(msg):
    for handler in running_handlers:
        handler.do_send(msg)

#sent to everyone
def msg_everyone(msg):
    for handler in handlers:
        handler.do_send(msg)

def create_players():
    for player in running_handlers:
        x_axis = random.randint(0, 624)
        y_axis = random.randint(0, 424)
        while colliding(x_axis, y_axis):
            x_axis = random.randint(0, 624)
            y_axis = random.randint(0, 424)
            # print "colliding: " + str(x_axis) + ", " + str(y_axis)
        player_number = running_handlers[player] 
        players[player_number] = [x_axis, y_axis, "human"]

# randomly selects a player to be it at the start of the game
# the "it" player number is the random number + 1
def choose_wolf():
    it_player = random.randint(0, len(players) - 1)
    player_list = []

    # puts the dictionary in a list so we don't get and index out of range
    # when a player leaves and their number is selected
    for player in players:
        player_list.append(player)
    it_player_number = player_list[it_player]

    players[it_player_number][2] = 'wolf'

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
        global players_ready, players, handlers, game_running
        if self in handlers:
            del(handlers[self])
        if self in handlers:
            del(running_handlers[self])
        players = {}
        players_ready = 0
        if len(handlers) <= 0:
            game_running = False
    
    def on_msg(self, msg):
        global players_ready, players, handlers, game_running, running_handlers

        if 'move' in msg:
            distribute_msg(msg)
        elif 'load' in msg:
            game_running = True
            for handler in handlers:
                running_handlers[handler] = handlers[handler]
            distribute_msg(msg)
        elif 'ready' in msg:
            #once all clients have finished counting down/are ready, 
            #the players will be "created" and sent out
            players_ready += 1
            if players_ready == len(running_handlers):
                create_players()
                choose_wolf()
                distribute_msg({"start_state": players})
        elif 'score' in msg:
            player_scores[msg['player_number']] = msg['score']

        elif 'restart' in msg:
           game_running = False
           msg_everyone({"restart": 'restart'})
           handlers = {}  # map client handler to user name
           running_handlers = {}
           players = {}
           players_ready = 0

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
        