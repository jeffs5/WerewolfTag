#
# python imports
#
import time
import pygame
from player.Human import Human
from player.Werewolf import Werewolf

#
# Player Class Module
#
class Player(object):
    #
    #  default constructor
    #
    def __init__(self, x, y, value):
        # set player sprite
        self.humanSprite = Human()
        self.werewolfSprite = Werewolf()
        self.currentSprite = self.humanSprite
        self.currentSprite.rect.x = x
        self.currentSprite.rect.y = y
        
        self.playerNumber = int(value)
        # self.rect = pygame.Rect(x, y, 50, 50) 
        self.color = (255, 255, 255)
        self.is_it = False
        self.score = 0
        self.current_dir = (0, 0)
        self.transforming = False
        self.transform_complete = time.time()
        self.speed = 2
        self.speed_timer = time.time()
        self.shovel = False
        self.in_hole = False
        self.in_hole_timer = time.time()
        self.wall = False
        self.transform_counter = 0

    #
    # add parameter for power ups later
    #
    def move(self, dx, dy, direction, borders, players, powerups, placeables):
        # Move each axis separately. Note that this checks for collisions both times.
        if not self.in_hole: 
            if len(borders) == 4:
                if dx != 0:
                    self.move_single_axis(dx * self.speed, 0, direction, borders,
                            players, powerups, placeables)
                if dy != 0:
                    self.move_single_axis(0, dy * self.speed, direction, borders,
                            players, powerups, placeables)
        return players

    def get_player_number(self):
        return self.playerNumber

    def start_speed(self, speed):
        self.speed = speed
        self.speed_timer = time.time() + 5

    def end_speed(self):
        self.speed = 2

    def start_hole(self):
        self.in_hole = True
        # stuck in hole for two seconds
        self.in_hole_timer = time.time() + 2

    def end_hole(self):
        self.in_hole = False

    def place_placeable(self):
        if self.shovel:
            self.shovel = False
            return 'hole'   

        elif self.wall:
            self.wall = False
            return 'wall'

    def get_score(self):
        return self.score

    def increase_score(self, score):
        self.score += score

    def becomes_it(self):
        self.start_transform()
        return self

    # set speed to faster!
    def becomes_not_it(self):
        self.color = (255, 255, 255)
        self.is_it = False

        return self

    # starts transformation into wolf, if they are just tagged,
    # they cannot move for 3 seconds
    def start_transform(self):
        self.transforming = True
        self.transform_complete = time.time() + 3

    # completes the werewolf transformation, should be called only
    # when the global/main clock notices that 3+ seconds have
    # passed and the player is not done transforming
    def finish_transform(self):
        self.transforming = False
        self.is_it = True
        self.color = (255, 0, 0)
        self.transform_counter = 0

    #
    # is player it?
    #
    def is_it(self):
        return self.is_it
    
    #
    # move player on the screen
    #
    def move_single_axis(self, dx, dy, direction, borders, players, powerups, placeables):
        # set sprite animation
        self.currentSprite.setAnimation(direction)
        
        # update sprite
        self.currentSprite.update()
         
        # Move the rect
        collide = False
        self.currentSprite.rect.x += dx
        self.currentSprite.rect.y += dy
     
        # If you collide with a wall
        for border in borders:
            if self.currentSprite.rect.colliderect(border):
                collide = True
                if dx > 0:
                    self.currentSprite.rect.right = border.left
                if dx < 0:
                    self.currentSprite.rect.left = border.right
                if dy > 0:
                    self.currentSprite.rect.bottom = border.top
                if dy < 0:
                    self.currentSprite.rect.top = border.bottom

        for player in players:
            if self != player:
                if self.currentSprite.rect.colliderect(player.rect):
                    collide = True
                    if dx > 0:
                        self.currentSprite.rect.right = player.rect.left
                    if dx < 0:
                        self.currentSprite.rect.left = player.rect.right
                    if dy > 0:
                        self.currentSprite.rect.bottom = player.rect.top
                    if dy < 0:
                        self.currentSprite.rect.top = player.rect.bottom
                    if self.is_it:
                        player = player.becomes_it()
                        self = self.becomes_not_it()
                    elif self.is_it != True and player.is_it:
                        player = player.becomes_not_it()
                        self = self.becomes_it()

        for powerup in powerups:
            if self.currentSprite.rect.colliderect(powerup):
                powerup.apply_powerup(self)
                powerups.remove(powerup)

        for placeable in placeables:
            if self.currentSprite.rect.colliderect(placeable):
                if placeable.type == 'hole':
                    self.start_hole()
                    placeables.remove(placeable)
                    pygame.mixer.Sound("Music/Placeable.wav").play()

                elif placeable.type == 'wall':
                    pygame.mixer.Sound("Music/Placeable.wav").play()
                    collide = True
                    if dx > 0:
                        self.rect.right = placeable.rect.left
                    if dx < 0:
                        self.rect.left = placeable.rect.right
                    if dy > 0:
                        self.rect.bottom = placeable.rect.top
                    if dy < 0:
                        self.rect.top = placeable.rect.bottom

        if not collide:
            if self.score >= 0 and not self.is_it:
                self.score -= 1
            else:
                self.score = 0
                 
    #
    # draw player 
    #
    def draw_player(self, screen):
        self.currentSprite.draw(screen)
