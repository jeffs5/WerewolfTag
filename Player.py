import os
import random
import pygame
import time

class Player(object):

    def __init__(self, x, y, value, players):
        self.playerNumber = value
        players.append(self)
        self.rect = pygame.Rect(x, y, 16, 16)
        self.color = (255,255,255)
        self.is_it = False
        self.score = 0
        self.current_dir = (0,0)
        self.transform_complete = time.time()
        self.attributes = []
        self.transform_counter = 0 #used to know which animation to display during transformation

    def move(self, dx, dy, borders, players):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0, borders, players)
        if dy != 0:
            self.move_single_axis(0, dy, borders, players)

        return players

    def get_player_number(self):
        return self.playerNumber
    
    def get_score(self):
        return self.score

    def increase_score(self, score):
        self.score += score

    def becomes_it(self):
        self.start_transform()

        return self
        #set speed to faster!

    def becomes_not_it(self):
        self.color = (255, 255, 255)
        self.is_it = False

        return self

    #starts transformation into wolf, if they are just tagged, 
    #they cannot move for 3 seconds
    def start_transform(self):
        self.attributes.append("transforming")
        self.transform_complete = time.time() + 3

    #completes the werewolf transformation, should be called only
    #when the global/main clock notices that 3+ seconds have
    #passed and the player is not done transforming
    def finish_transform(self):
        self.attributes.remove("transforming")
        self.is_it = True
        self.color = (255, 0, 0)
        transform_counter = 0

    def move_single_axis(self, dx, dy, borders, players):
        
        # Move the rect
        collide = False
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall
        for border in borders:
            if self.rect.colliderect(border):
                collide = True
                if dx > 0: 
                    self.rect.right = border.left
                if dx < 0: 
                    self.rect.left = border.right
                if dy > 0: 
                    self.rect.bottom = border.top
                if dy < 0: 
                    self.rect.top = border.bottom

        for player in players:
                if self != player:
                    if self.rect.colliderect(player.rect):
                        collide = True

                        if dx > 0: 
                            self.rect.right = player.rect.left
                        if dx < 0: 
                            self.rect.left = player.rect.right
                        if dy > 0: 
                            self.rect.bottom = player.rect.top
                        if dy < 0: 
                            self.rect.top = player.rect.bottom

                        #add transform period where it player cannot move and no one can be tagged
                        if self.is_it:
                            player = player.becomes_it()
                            self = self.becomes_not_it()
                        elif self.is_it != True and player.is_it:
                            player = player.becomes_not_it()
                            self = self.becomes_it()
        if not collide:
            self.score -=1;
       # if collide == False and self.is_it != True:
       #     self.score -=1

    def draw_player(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def is_it(self):
        return is_it
