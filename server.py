from network import Listener, Handler, poll
from time import sleep


handlers = {}  # map client handler to user name

def distribute_msg(msg):
	for handler in handlers:
		handler.do_send(msg)

class MyHandler(Handler):
    
    def on_open(self):
    	player_number = len(handlers) + 1
    	handlers[self] = player_number
        for i in handlers:
            i.do_send({'join': player_number})
        print player_number
        
    def on_close(self):
        del(handlers[self])
    
    def on_msg(self, msg):
                if 'move' in msg:
                        print(msg['move'])
                        distribute_msg(msg)
                if 'added_player' in msg:
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

