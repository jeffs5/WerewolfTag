import random
import pygame
from base import Globals
from player.WerewolfAIPlayer import WerewolfAIPlayer
from player.HumanAIPlayer import HumanAIPlayer
from player.SinglePlayer import SinglePlayer

class Game:
   
    def __init__(self, client):        
        self.client = client
        self.ai = WerewolfAIPlayer(Globals.AI_EASY_MODE)
        self.ai.currentSprite.rect.x = random.randint(0, 640)
        self.ai.currentSprite.rect.y = random.randint(0, 440)
        self.humanAi = HumanAIPlayer(Globals.AI_EASY_MODE)
        self.humanAi.currentSprite.rect.x = random.randint(0,640)
        self.humanAi.currentSprite.rect.y = random.randint(0,440)
        self.player = SinglePlayer()
        self.player.currentSprite.rect.x = random.randint(0,640)
        self.player.currentSprite.rect.y = random.randint(0,440)
        self.secondHumanAi = HumanAIPlayer(Globals.AI_EASY_MODE)
        self.secondHumanAi.currentSprite.rect.x = random.randint(0,640)
        self.secondHumanAi.currentSprite.rect.y = random.randint(0,440)
        self.thirdHumanAi = HumanAIPlayer(Globals.AI_EASY_MODE)
        self.thirdHumanAi.currentSprite.rect.x = random.randint(0,640)
        self.thirdHumanAi.currentSprite.rect.y = random.randint(0,440)
        self.fourthHumanAi = HumanAIPlayer(Globals.AI_EASY_MODE)
        self.fourthHumanAi.currentSprite.rect.x = random.randint(0,640)
        self.fourthHumanAi.currentSprite.rect.y = random.randint(0,440)
        self.fifthHumanAi = HumanAIPlayer(Globals.AI_EASY_MODE)
        self.fifthHumanAi.currentSprite.rect.x = random.randint(0,640)
        self.fifthHumanAi.currentSprite.rect.y = random.randint(0,440)
        self.playerList = {self.player, self.humanAi, self.secondHumanAi, 
                           self.thirdHumanAi, self.fourthHumanAi, self.fifthHumanAi}
        
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
            
        self.ai.update(self.player, self.playerList)
        self.humanAi.update(self.ai)
        self.secondHumanAi.update(self.ai)
        self.thirdHumanAi.update(self.ai)
        self.fourthHumanAi.update(self.ai)
        self.fifthHumanAi.update(self.ai)
        
    def draw(self):
        self.player.draw(self.client.window)
        self.ai.draw(self.client.window)
        self.humanAi.draw(self.client.window)
        self.secondHumanAi.draw(self.client.window)
        self.thirdHumanAi.draw(self.client.window)
        self.fourthHumanAi.draw(self.client.window)
        self.fifthHumanAi.draw(self.client.window)
        
    def end(self):
        pass
