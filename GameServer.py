#
# python imports
#
from base import Globals
from network.ServerListener import ServerListener

#
# server listener objects
#
serverListener = ServerListener(Globals.NETWORK_PORT)

#
# run game server
#
while 1:
    try:
        serverListener.poll_messages()
    except KeyboardInterrupt:
        serverListener.close()
        exit("\n")
