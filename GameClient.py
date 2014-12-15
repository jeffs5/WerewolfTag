#
# python imports
#
from base import Globals
from game.GameModel import GameModel
from game.GameView import GameView
from game.GameController import GameController
from network.ClientHandler import ClientHandler

#
# game objects
#
gameModel = GameModel()
gameView = GameView(gameModel)
clientHandler = ClientHandler(gameModel, Globals.NETWORK_HOST, Globals.NETWORK_PORT)
gameController = GameController(gameModel, clientHandler)

#
# run game client
#
while gameModel.running:
    try:
        # poll client network messages
        clientHandler.poll_messages()
        
        # get user input commands
        message = gameController.get_commands()
        
        # send messages to network
        clientHandler.send_message(message)
        
        # draw game view  display
        gameView.display()

    except KeyboardInterrupt:
        # send close command to other clients
        clientHandler.do_send({'close' : 'close'})
        
        # close network connection
        clientHandler.do_close()
        
        # exit window
        exit()