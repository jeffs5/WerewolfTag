"""
Simple JSON wrapper on top of asyncore TCP sockets. 
Provides on_open, on_close, on_msg, do_send, and do_close callbacks.

Public domain

With inspiration from:
http://pymotw.com/2/asynchat/
http://code.google.com/p/podsixnet/
http://docstore.mik.ua/orelly/other/python/0596001886_pythonian-chp-19-sect-3.html


#################
# Echo server:
#################
from network import Listener, Handler, poll

class MyHandler(Handler):
    def on_msg(self, data):
        self.do_send(data)
        
class EchoServer(Listener):
    handlerClass = MyHandler

server = EchoServer(8888)
while 1:
    poll()


#################
# One-message client:
#################
from network import Handler, poll

done = False

class Client(Handler):
    def on_open(self):
        self.do_send({'a': [1,2], 5: 'hi'})
        global done
        done = True

client = Client('localhost', 8888)
while not done:
    poll()
client.do_close()

"""

from network.NetworkHandler import NetworkHandler
import asyncore
import socket

class NetworkListener(asyncore.dispatcher):
    
    handlerClass = NetworkHandler  # override this class by your own
    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
        self.bind(('', port))
        self.listen(5)  # max 5 incoming connections at once (Windows' limit)

    def handle_accept(self):  # called on the passive side
        sock, (host, port) = self.accept()
        h = self.handlerClass(host, port, sock)
        self.on_accept(h)
        h.on_open()
    
    # API you can use
    def stop(self):
        self.close()

    # callbacks you override
    def on_accept(self, h):
        pass
