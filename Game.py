
import pygame
from base import Globals
from player.AIPlayer import AIPlayer
from player.SinglePlayer import SinglePlayer

class Game:
   
    def __init__(self, client):
        self.client = client
        self.multiplayerMode = False
        self.ai = AIPlayer(Globals.AI_EASY_MODE)
        self.player = SinglePlayer()
        self.player.currentSprite.rect.x = 100
        self.player.currentSprite.rect.y = 100
        
    def update(self, key):
        # start running the clock, limits fps to 60
        # self.milliseconds += self.clock.tick_busy_loop(60) 
    
        if key[pygame.K_LEFT]:
            self.player.update(-2, 0, Globals.DIRECTION_LEFT)
        if key[pygame.K_RIGHT]:
            self.player.update(2, 0, Globals.DIRECTION_RIGHT)
        if key[pygame.K_UP]:
            self.player.update(0, -2, Globals.DIRECTION_UP)
        if key[pygame.K_DOWN]:
            self.player.update(0, 2, Globals.DIRECTION_DOWN)
            
        self.ai.update(self.player, {}, self.multiplayerMode)
        
    def draw(self):
        self.player.draw(self.client.window)
        self.ai.draw(self.client.window)
        
    def end(self):
        pass
