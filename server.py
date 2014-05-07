from network import Listener, Handler, poll
import Player
import Trap
from time import sleep


handlers = {}  # map client handler to user name
players = []
traps = []

def distribute_msg(msg):
	for handler in handlers:
		handler.do_send(msg)

def create_players():
	global players

	# creates one player for each handler
	for player in handlers:
		player_spot_occupied = False
		while not player_spot_occupied:
			player_number = handlers[player]
			players.append(Player.Player(random.randint(0,100), random.randint(0,100), player_number))

			# checks if newly created player occupies same space as pany previously created palyer
			for existing_player in players:
				if player is not existing_player:
					if self.rect.colliderect(player.rect):
						players.remove(player)
						player_spot_occupied = True

def create_traps():
	global traps

def countdown():
    now = time.time()
    time_up = now + 5

    while time.time() < time_up:
        time_left = time_up-time.time()
        sleep(0.05)  # seconds
        distribute_msg({'countdown': time_left})

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
            countdown()
            create_players()
            create_traps()
            distribute_msg("start")

		# 	# distribute_msg({'players': players, 'traps' : traps})


class Serv(Listener):
    handlerClass = MyHandler


port = 8888
server = Serv(port)

now = time.time()

while 1:
	try:
	    poll()
	    sleep(0.05)  # seconds
	except KeyboardInterrupt:
		server.close()
		exit("\n")

