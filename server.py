from network import Listener, Handler, poll
import Player
from time import sleep
import time
import random

handlers = {}  # map client handler to user name
players = {}
players_ready = 0

#########################################

def distribute_msg(msg):
    for handler in handlers:
        handler.do_send(msg)

def create_players():
    for player in handlers:
        x_axis = random.randint(0, 640)
        y_axis = random.randint(0, 440)
        player_number = handlers[player] 
        players[player_number] = [x_axis, y_axis, "human"]

# randomly selects a player to be it at the start of the game
# the "it" player number is the random number + 1
def choose_wolf():
    it_player = random.randint(0, len(players))
    players[it_player][2] = 'wolf'

###########################################

class MyHandler(Handler):
    
    # def send_all(message):
    #     for i in 
    def on_open(self):
        player_number = len(handlers) + 1
        handlers[self] = player_number
        distribute_msg({'join': player_number})
        
    def on_close(self):
        global players_ready, players
        del(handlers[self])
        players = {}
        players_ready = 0
    
    def on_msg(self, msg):
        global players_ready, players

        if 'move' in msg:
            distribute_msg(msg)
        if 'load' in msg:
            distribute_msg(msg)
        if 'ready' in msg:
            #once all clients have finished counting down/are ready, the players will be "created" and sent out
            players_ready += 1
            if players_ready == len(handlers):
                create_players()
                choose_wolf()
                distribute_msg({"start_state": players})
                #send who is it



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
        