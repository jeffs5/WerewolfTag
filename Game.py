'''
Created on Nov 10, 2014

@author: Jon
'''
import pygame
from base import Globals
from player.Human import Human
from player.Werewolf import Werewolf
from base.EasyHumanAI import EasyHumanAI

class Game:
    client = None
    humanPlayer = None 
    playerList = None
    #werewolfPlayer=None
    easyHumanAI = None #for one human bot
    humanAIPlayer = None  # for one human bot
    
    #clock = pygame.time.Clock()
    #milliseconds = 0
    multiplayerMode = False

    def __init__(self, client):
        self.client = client
        self.speed = 1
        
    def init(self):
        self.humanPlayer = Human()
        self.playerList = [self.humanPlayer, Human(), Human()]
        self.playerList[2].x = 400
        self.playerList[2].y = 300
        if(len(self.playerList) > 1):
            self.multiplayerMode = True
        self.easyHumanAI = EasyHumanAI() #initialize a Human bot
        #self.werewolfPlayer = Werewolf()
    
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
                    
        self.easyHumanAI.movePath(self.humanPlayer, self.playerList, self.multiplayerMode)
        self.werewolfPlayer.update()
        
        self.humanPlayer.update()
        
        for player in self.playerList:
            player.update()
        
        self.easyHumanAI.update()
        
    def draw(self, screenWidth, screenHeight):
        self.humanPlayer.draw(self.client.window)
        
        for player in self.playerList:
            player.draw(self.client.window)
        
        self.easyHumanAI.draw(self.client.window)
        
        while(screenWidth < 640):
            self.humanPlayer.draw(self.client.window)
        
    def end(self):
        pass
