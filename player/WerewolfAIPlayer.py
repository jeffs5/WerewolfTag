import math
import sys
import os
from base import Globals
from player.Human import Human
from player.Werewolf import Werewolf


class WerewolfAIPlayer(object):
    
    def __init__(self, aiMode):
        self.xSpeed = 1
        self.ySpeed = 1
        self.aiMode = aiMode
        self.humanSprite = Human()
        self.werewolfSprite = Werewolf()
        self.currentSprite = self.werewolfSprite
    
    def restart_program(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)
         
    def update(self, humanPlayer, playerList):
        # also check to see if the ai is in the transform state first
        shortestDistance = 1000  # know how big the board is
        currentPlayer = humanPlayer
        
        for player in playerList:
            playerDistance = self.calculateDistance(player)
            if playerDistance < shortestDistance:
                shortestDistance = playerDistance
                currentPlayer = player
        
        for player in playerList:
            distance = self.calculateDistance(player)
            if(distance < 20):
                self.restart_program()
            #self.swap_sprite(self.humanSprite)
         
        if(self.currentSprite.rect.x - currentPlayer.currentSprite.rect.x == 0):  # ww and human on same column
            if(self.currentSprite.rect.y - currentPlayer.currentSprite.rect.y > 0):
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_UP)
                self.currentSprite.update()
                self.currentSprite.rect.y -= self.ySpeed
            
            elif(self.currentSprite.rect.y - currentPlayer.currentSprite.rect.y < 0):
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_DOWN)
                self.currentSprite.update()
                self.currentSprite.rect.y += self.ySpeed
                
        elif(self.currentSprite.rect.y - currentPlayer.currentSprite.rect.y == 0):  # ww and human on same row
            if(self.currentSprite.rect.x - currentPlayer.currentSprite.rect.x > 0):
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_LEFT)
                self.currentSprite.update()
                self.currentSprite.rect.x -= self.xSpeed
                
            elif(self.currentSprite.rect.x - currentPlayer.currentSprite.rect.x < 0):
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_RIGHT)
                self.currentSprite.update()
                self.currentSprite.rect.x += self.xSpeed
       
        elif(self.currentSprite.rect.x - currentPlayer.currentSprite.rect.x > 0):  # ww is to the right of the player
            if(self.currentSprite.rect.y - currentPlayer.currentSprite.rect.y > 0):  # ww is south of player, move northwest
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_UP)
                self.currentSprite.update()
                self.currentSprite.rect.y -= self.ySpeed
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_LEFT)
                self.currentSprite.update()
                self.currentSprite.rect.x -= self.xSpeed
                 
            else:  # move southwest
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_DOWN)
                self.currentSprite.update()
                self.currentSprite.rect.y += self.ySpeed
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_LEFT)
                self.currentSprite.update()
                self.currentSprite.rect.x -= self.xSpeed
        else:
            if(self.currentSprite.rect.y - currentPlayer.currentSprite.rect.y > 0):  # move northeast
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_UP)
                self.currentSprite.update()
                self.currentSprite.rect.y -= self.ySpeed
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_RIGHT)
                self.currentSprite.update()
                self.currentSprite.rect.x += self.xSpeed
            else:  # move southeast
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_DOWN)
                self.currentSprite.update()
                self.currentSprite.rect.y += self.ySpeed
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_RIGHT)
                self.currentSprite.update()
                self.currentSprite.rect.x += self.xSpeed

    def draw(self, screen):
        self.currentSprite.draw(screen)
        
    def calculateDistance(self, humanPlayer):
        xDistance = self.currentSprite.rect.x - humanPlayer.currentSprite.rect.x
        yDistance = self.currentSprite.rect.y - humanPlayer.currentSprite.rect.y
        return math.sqrt((xDistance ** 2) + (yDistance ** 2))
