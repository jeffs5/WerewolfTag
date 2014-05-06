from network import Listener, Handler, poll
import Player
from time import sleep


handlers = {}  # map client handler to user name
players = []

def distribute_msg(msg):
	for handler in handlers:
		handler.do_send(msg)

def create_players():
	for player in handlers:
		handlers[player] = Player.Player(random.randint(0,100), random.randint(0,100), handlers[player], players)


class MyHandler(Handler):
    
    # def send_all(message):
    #     for i in 
    def on_open(self):
    	player_number = len(handlers) + 1
    	handlers[self] = player_number
        distribute_msg({'join': player_number})
        print player_number
        
    def on_close(self):
        del(handlers[self])
    
    def on_msg(self, msg):
        if 'move' in msg:
            distribute_msg(msg)
        if 'load' in msg:
            distribute_msg(msg)


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

