from network import Handler, poll
import sys
from threading import Thread
from time import sleep
import os
import random
import pygame
import Player
import time

players = []
borders = []
player = None 

def create_player(msg):
    global players
    #might not work
    player = Player.Player(random.randint(0,640), random.randint(0,440), msg['join'], players)
    print "player created" + len(players)
    while hit_player(player):
        player = Player.Player(random.randint(0,640), random.randint(0,440), msg['join'], players)

    client.do_send({'added_player' : player})

class Client(Handler):
    

    def on_close(self):
        pass
    
    def on_msg(self, msg):
        global players
        global borders

        if 'join' in msg:
            print 'player number ' + str(msg['join']) + ' joined'
            create_player(msg)
        if 'added_player' in msg:
            players.append(msg['added_player'])
        if 'move' in msg:
            instructions = msg['move']
            player_number = msg['player_number']
            player = find_player(player_number)
                #can return None
            player.move(instructions[0], instructions[1], borders, players)
        
host, port = 'localhost', 8888
client = Client(host, port)

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds
  

def hit_player(self, player):
    global border
    global players

    for border in borders:
        if player.rect.colliderect(border):
            return True

    for current_player in players:
        if player.rect.colliderect(current_player):
            return True

    return False

def find_player(self, player_number):
    global players

    for current_player in players:
        if current_player.get_player_number() == player_number:
            return current_player

    return None

##############################

# randomly selects a player to be it at the start of the game
# the "it" player number is the random number + 1
def choose_it(players):
    print len(players)
    it_player = random.randint(0, len(players)-1)
    players[it_player].becomes_it()

#############################

def select_winner(players):
    winner_player = players[0]
    for player in players:
        if player.get_score() > winner_player.get_score():
            winner_player = player

    return winner_player

############################

def init_game(num_players, players):
    for x in range (0, num_players):
        x_axis = 100 * (x + 1)
        y_axis = 100 * (x + 1)
        player = Player.Player(x_axis, y_axis, x+1 , players)

    choose_it(players)


############ MAIN GAME LOOP ##########################

thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()

###########################

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Play Tag!")
screen = pygame.display.set_mode((640, 440))

mode = 0

borders = [pygame.Rect(0,0, 640, 1), pygame.Rect(0,0, 1, 440), pygame.Rect(639,0, 1, 440), pygame.Rect(0,439, 640, 1)]

myfont = pygame.font.SysFont("monospace", 16)

running = True
FRAMERATE = 60
clock = pygame.time.Clock()

controls = {pygame.K_LEFT : (-1,0), pygame.K_RIGHT : (1,0), pygame.K_UP : (0,-1), pygame.K_DOWN : (0,1)} # player controls

while running:
    try:
        key = pygame.key.get_pressed()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False

        #start screen
        if mode == 0:
            title = myfont.render("Werewolf Tag", 1, (255,255,255))
            instructions = myfont.render("Press SPACE to Start", 1, (255,255,255))
            screen.blit(title, (240, 10))
            screen.blit(instructions, (210, 210))

            if key[pygame.K_SPACE]:
                mode = 1
                now = time.time()
                sleep(1)
                choose_it(players)

        #actual game
        if mode == 1:
            time_up = now + 60
            if time.time() >= time_up:
                mode = 2

            clock.tick(FRAMERATE)
            
            # Move the player if an arrow key is pressed
            
            for pressed in controls:
                if key[pressed]:
                    instruction = controls.get(pressed)
                    moving_player = player

                    # used to know what instruction players are currently going to see if they can be pushed
                    # instruction[2].current_dir = (instruction[0], instruction[1])

                    #if the player has an attribute check if they can still move
                    if len(moving_player.attributes) > 0:
                        for attribute in moving_player.attributes:
                            if attribute != "transforming":
                                moving_player.move(instruction[0], instruction[1], borders, players)
                    else:
                        moving_player.move(instruction[0], instruction[1], borders, players)
                        client.do_send({'move': instruction, 'player': player.get_player_number()})
                            

            # Draw the scene
            screen.fill((0, 0, 0))


            #check to see if any player is still transforming
            for player in players:
                player.increase_score(1)
                for attribute in player.attributes:
                    if attribute == "transforming":
                        if time.time() >= player.transform_complete:
                            player.finish_transform()

                        #randomly tested modulo numbers were used for the animation
                        elif player.transform_counter %18 == 1:
                            player.color = (255, 255, 255)
                        elif player.transform_counter %6 == 1:
                            player.color = (255, 0, 0)

                        #counter used to determine which transformation animation should be shown
                        player.transform_counter += 1

                player.draw_player(screen)
           
            disclaimertext = myfont.render("Player 1 score: {0}".format(players[0].get_score()) , 1, (255,255,255))
            disclaimertext3 = myfont.render("Time left: {0}".format(round(time_up-time.time(), 2)) , 1, (255,255,255))
            screen.blit(disclaimertext, (16, 400))
            screen.blit(disclaimertext3, (200, 10))

        #once the time is up!
        if mode == 2:
            backgroundColor = (0,0,0)
            screen.fill(backgroundColor)

            time_up = myfont.render("Time's Up!", 1, (255,255,255))
            winner = select_winner(players)
            winner_text = myfont.render("The winner is: Player " + str(winner.get_player_number()), 1, (255,255,255))
            restart_text = myfont.render("Press Space to continue", 1, (255,255,255))

            screen.blit(time_up, (240, 10))
            screen.blit(winner_text, (210, 210))
            screen.blit(restart_text, (210, 220))

            if key[pygame.K_SPACE]:
                players = []
                mode = 0

        pygame.display.flip()
        

    except KeyboardInterrupt:
        client.do_send({'close' : 'close'})
        client.do_close()
        exit()
   # mytxt = sys.stdin.readline().rstrip()
   # client.do_send({'speak': myname, 'txt': mytxt})
