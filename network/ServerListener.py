from time import sleep
from network.NetworkListener import NetworkListener
from network.NetworkHandler import poll
from network.ServerHandler import ServerHandler, determine_powerup


class ServerListener(NetworkListener):
    handlerClass = ServerHandler
    def poll_messages(self):
        poll()
        determine_powerup()
        sleep(0.05)
        
        
        