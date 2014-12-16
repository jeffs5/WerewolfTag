import random
from base import Globals
from network.NetworkHandler import NetworkHandler

handlers = {}  # map client handler to user name
running_handlers = {}
players = {}
players_ready = 0
player_scores = {}
board_x = Globals.WINDOW_WIDTH
board_y = Globals.WINDOW_HEIGHT
board = []
scores_received = 0
game_running = False

# sent to the players who are in the game
def distribute_msg(msg):
    for handler in running_handlers:
        handler.do_send(msg)

# sent to everyone
def msg_everyone(msg):
    for handler in handlers:
        handler.do_send(msg)

def create_board():
    global board, board_x, board_y
    if len(board) != 0:
        board = []
    board.append([0, 0, board_x, 1])
    board.append([0, 0, 1, board_y])
    board.append([board_x - 1, 0, 1, board_y])
    board.append([0, board_y - 1, board_x, 1])
    # [pygame.Rect(0, 0, board_x, 1), pygame.Rect(0, 0, 1, board_y),
    #  pygame.Rect(board_x - 1, 0, 1, board_y), pygame.Rect(0, board_y - 1, board_x, 1)]


def create_players():
    for player in running_handlers:
        # 50 is the size of the player box
        x_axis = random.randint(0, board_x - 50)
        y_axis = random.randint(0, board_y - 50)
        while colliding(x_axis, y_axis, 50, 50):
            x_axis = random.randint(0, board_x)
            y_axis = random.randint(0, board_y)
            # print "colliding: " + str(x_axis) + ", " + str(y_axis)
        player_number = running_handlers[player] 
        players[player_number] = [x_axis, y_axis, "human"]

# randomly selects a player to be it at the start of the game
# the "it" player number is the random number + 1
def choose_wolf():
    it_player = random.randint(0, len(players) - 1)
    player_list = []

    # puts the dictionary in a list so we don't get and index out of range
    # when a player leaves and their number is selected
    for player in players:
        player_list.append(player)
    it_player_number = player_list[it_player]

    players[it_player_number][2] = 'wolf'

def determine_powerup():
    if game_running:
        # .01 works well as a value
        if random.random() < .01:
            # 25 is the size of the powerup box
            x = random.randint(0, board_x - 25)
            y = random.randint(0, board_y - 25)
            rand_val = random.random() 
            name = 'speed'
            if rand_val > .33 and rand_val < .66:
                name = 'wall'
            elif rand_val > .66:
                name = 'shovel'
            # replace x and y with random values
            distribute_msg({'powerup': True, 'name': name, 'x' : x, 'y' : y})


def colliding(x1, y1, width, height):
    for player in players.items():
        x2 = player[1][0]
        y2 = player[1][1]
        # print str(x1) + ", " + str(y1) + ": " + str(x2) + ", " + str(y2)
        if x1 < x2 + width and y1 < y2 + height and x2 < x1 + width and y2 < y1 + height:
            return x1 < x2 + width and y1 < y2 + height and x2 < x1 + width and y2 < y1 + height

    return False

def determine_winner(player_scores):
    # player
    for player in player_scores:
        if player_scores[player] == player_scores[player]:
            winner = (player, player_scores[player])

    for player in player_scores:
        if player_scores[player] >= winner[1]:
            winner = (player, player_scores[player])

    return winner


class ServerHandler(NetworkHandler):
    
    # def send_all(message):
    #     for i in 
    def on_open(self):
        global handlers, game_running
        player_number = len(handlers)
        handlers[self] = player_number
        self.do_send({'join': player_number, 'game_running': game_running})
        
    def on_close(self):
        global players_ready, players, handlers, game_running, running_handlers
        if self in handlers:
            # print "deleted from handler list"
            del(handlers[self])
        if self in running_handlers:
            del(running_handlers[self])
        players = {}
        players_ready = 0
        if len(handlers) <= 0:
            game_running = False
    
    def on_msg(self, msg):
        global players_ready, players, handlers, game_running, running_handlers, player_scores, scores_received, board

        if 'move' in msg or 'place' in msg:
            distribute_msg(msg)

        elif 'load' in msg:
            game_running = True
            for handler in handlers:
                running_handlers[handler] = handlers[handler]
            distribute_msg(msg)
        elif 'ready' in msg:
            # once all clients have finished counting down/are ready, 
            # the players will be "created" and sent out
            players_ready += 1
            if players_ready == len(running_handlers):
                create_board()
                create_players()
                choose_wolf()
                distribute_msg({"start_state": players, "board": board})
        elif 'score' in msg:
            scores_received += 1
            player_scores[msg['player_number']] = msg['score']
            
            if scores_received == len(running_handlers):
                scores_received = 0
                winner = determine_winner(player_scores)
                player_scores = {}
                distribute_msg({'winner_number': winner[0], 'winner_score': winner[1]})

        elif 'restart' in msg:
            game_running = False
            msg_everyone({"restart": 'restart'})
            handlers = {}  # map client handler to user name
            running_handlers = {}
            players = {}
            players_ready = 0
            player_scores = {}
            scores_received = 0
