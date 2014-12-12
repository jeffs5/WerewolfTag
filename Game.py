'''
Created on Nov 10, 2014

@author: Jon
'''
import pygame
from base.Human import Human
from base.Werewolf import Werewolf
from base.HumanAI import HumanAI

class Game:
    client = None
    humanPlayer = None
    werewolfPlayer=None
    humanAIPlayer = None #for one human bot
    clock = pygame.time.Clock()
    milliseconds = 0

    def __init__(self,client):
        self.client=client
        
    def init(self):
        self.humanPlayer = Human()
        self.werewolfPlayer = Werewolf()
        self.humanAIPlayer = HumanAI() #initialize a Human bot
    
    def update(self,key):
        #start running the clock, limits fps to 60
        #self.milliseconds += self.clock.tick_busy_loop(60) 
        
        if key[pygame.K_LEFT]:     
            self.humanPlayer.moveLeft()
        if key[pygame.K_RIGHT]:     
            self.humanPlayer.moveRight()
        if key[pygame.K_UP]:     
            self.humanPlayer.moveUp()
        if key[pygame.K_DOWN]:   
            self.humanPlayer.moveDown()    
                    
        self.humanAIPlayer.movePath(self.humanPlayer)
                
        self.humanPlayer.update()
        self.werewolfPlayer.update()
        self.humanAIPlayer.update()
        
    def draw(self):
        self.humanPlayer.draw(self.client.window)
        self.werewolfPlayer.draw(self.client.window)
        self.humanAIPlayer.draw(self.client.window)
        
    def end(self):
        pass