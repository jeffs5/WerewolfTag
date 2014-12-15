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
        clientHandler.poll_messages()
        message = gameController.get_commands()
        clientHandler.send_message(message)
        gameView.display()

    except KeyboardInterrupt:
        clientHandler.do_send({'close' : 'close'})
        clientHandler.do_close()
        exit()

