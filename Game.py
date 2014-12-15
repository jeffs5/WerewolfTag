'''
Created on Nov 10, 2014

@author: Jon
'''
import pygame
from base import Globals
from player.Human import Human
from player.Werewolf import Werewolf
from player.HumanAI import HumanAI

class Game:
    client = None
    humanPlayer = None
    werewolfPlayer = None
    humanAIPlayer = None  # for one human bot
    clock = pygame.time.Clock()
    milliseconds = 0

    def __init__(self, client):
        self.client = client
        self.speed = 1
        
    def init(self):
        self.humanPlayer = Human()
        self.werewolfPlayer = Werewolf()
        self.humanAIPlayer = HumanAI()  # initialize a Human bot
    
    def update(self, key):
        # start running the clock, limits fps to 60
        # self.milliseconds += self.clock.tick_busy_loop(60) 
        
        if key[pygame.K_LEFT]:
            self.humanPlayer.rect.x -= self.speed     
            self.humanPlayer.setAnimation(Globals.ANIMATION_MOVE_LEFT)
            self.humanPlayer.update()
        if key[pygame.K_RIGHT]:
            self.humanPlayer.rect.x += self.speed      
            self.humanPlayer.setAnimation(Globals.ANIMATION_MOVE_RIGHT)
            self.humanPlayer.update()
        if key[pygame.K_UP]:
            self.humanPlayer.rect.y -= self.speed      
            self.humanPlayer.setAnimation(Globals.ANIMATION_MOVE_UP)
            self.humanPlayer.update()
        if key[pygame.K_DOWN]:
            self.humanPlayer.rect.y += self.speed    
            self.humanPlayer.setAnimation(Globals.ANIMATION_MOVE_DOWN)  
            self.humanPlayer.update()
                    
        self.humanAIPlayer.movePath(self.humanPlayer)
        self.werewolfPlayer.update()
        self.humanAIPlayer.update()
        
    def draw(self):
        self.humanPlayer.draw(self.client.window)
        self.werewolfPlayer.draw(self.client.window)
        self.humanAIPlayer.draw(self.client.window)
        
    def end(self):
        pass
