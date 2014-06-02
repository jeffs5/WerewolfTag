import pygame
import time
from Player import Player

class Model():
    def __init__(self):
        self.players = {}
        self.borders = [pygame.Rect(0,0, 640, 1), pygame.Rect(0,0, 1, 440), pygame.Rect(639,0, 1, 440), pygame.Rect(0,439, 640, 1)]
        self.player_number = 0
        self.GAME_LENGTH = 20
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

    def init_game(self, player_msg):

        self.players = {}
        self.loading = False
        self.running = True

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
