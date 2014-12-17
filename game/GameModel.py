#
# python imports
#
import time
import pygame
from base import Globals
from player.Player import Player

#
# Game Model Class Module
#
class GameModel():
    def __init__(self):
        self.players = {}
        self.powerups = []
        self.placeables = []
        self.board_x = Globals.BORDER_WIDTH
        self.board_y = Globals.BORDER_HEIGHT
        self.borders = []
        self.player_number = 0
        self.GAME_LENGTH = Globals.GAME_LENGTH
        self.mode = 0
        self.loading = False
        self.running = True
        self.FRAMERATE = 60
        self.clock = pygame.time.Clock()
        self.now = time.time()
        self.game_running = False
        self.score_sent = False
        self.winner_number = 99
        self.winner_score = -99
        self.music_mode = 0
        

    def init_game(self, player_msg, board):

        self.players = {}
        self.loading = False
        self.running = True

        for border in board:
            self.borders.append(pygame.Rect(border[0], border[1], border[2], border[3]))

        for player in player_msg.items():
            # player[0] is player_number
            # player[1] is instruction
            # player[2] is player type
            player_info = player[1]
            x_axis = player_info[0]
            y_axis = player_info[1]
            new_player = Player(x_axis, y_axis, player[0])

            if player_info[2] == 'wolf':
                new_player.becomes_it()

            self.players[player[0]] = new_player
