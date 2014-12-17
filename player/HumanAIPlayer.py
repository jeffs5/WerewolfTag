import math
import random
from base import Globals
from player.Human import Human
from player.Werewolf import Werewolf

class HumanAIPlayer(object):
    
    def __init__(self, aiMode):
        self.xSpeed = 1
        self.ySpeed = 1
        self.aiMode = aiMode
        self.humanSprite = Human()
        self.currentSprite = self.humanSprite
        
    def update(self, werewolf): 
        if(self.danger):
            TD = self.threat_direction(werewolf) 
            if( (self.currentSprite.rect.x <= 40 or self.currentSprite.rect.x >=600) and 
                (self.currentSprite.rect.y > 40 and self.currentSprite.rect.y < 440) ):
                if(werewolf.currentSprite.rect.y > self.currentSprite.rect.y):
                    self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_UP)
                    self.currentSprite.update()
                    self.currentSprite.rect.y -= self.ySpeed
                else:
                    self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_DOWN)
                    self.currentSprite.update()
                    self.currentSprite.rect.y += self.ySpeed
            elif( (self.currentSprite.rect.y <=40 or self.currentSprite.rect.y >= 440) and 
                  (self.currentSprite.rect.x > 40 and self.currentSprite.rect.x < 600) ):
                if(werewolf.currentSprite.rect.x > self.currentSprite.rect.x):
                    self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_LEFT)
                    self.currentSprite.update()
                    self.currentSprite.rect.x -= self.xSpeed
                else:
                    self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_RIGHT)
                    self.currentSprite.update()
                    self.currentSprite.rect.x += self.xSpeed
            elif(TD == "N"):
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_UP)
                self.currentSprite.update()
                self.currentSprite.rect.y -= self.ySpeed
            elif(TD == "S"):
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_DOWN)
                self.currentSprite.update()
                self.currentSprite.rect.y += self.ySpeed
            elif(TD == "W"):
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_LEFT)
                self.currentSprite.update()
                self.currentSprite.rect.x -= self.xSpeed
            elif(TD == "E"):
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_RIGHT)
                self.currentSprite.update()
                self.currentSprite.rect.x += self.xSpeed
            elif(TD == "NE"):
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_UP)
                self.currentSprite.update()
                self.currentSprite.rect.y -= self.ySpeed
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_RIGHT)
                self.currentSprite.update()
                self.currentSprite.rect.x += self.xSpeed
            elif(TD == "NW"):
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_UP)
                self.currentSprite.update()
                self.currentSprite.rect.y -= self.ySpeed
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_LEFT)
                self.currentSprite.update()
                self.currentSprite.rect.x -= self.xSpeed
            elif(TD == "SE"):
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_DOWN)
                self.currentSprite.update()
                self.currentSprite.rect.y += self.ySpeed
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_RIGHT)
                self.currentSprite.update()
                self.currentSprite.rect.x += self.xSpeed
            elif(TD == "SW"):
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_DOWN)
                self.currentSprite.update()
                self.currentSprite.rect.y += self.ySpeed
                self.currentSprite.setAnimation(Globals.ANIMATION_MOVE_LEFT)
                self.currentSprite.update()
                self.currentSprite.rect.x -= self.xSpeed
    
    def danger(self, werewolf):
        distance = calculateDistance(self, werewolf)
        if (distance < 150000):
            self.danger = True
        
    def threat_direction(self, werewolf):
        if(werewolf.currentSprite.rect.x == self.currentSprite.rect.x and 
           werewolf.currentSprite.rect.y == self.currentSprite.rect.y):
            return "x"
        elif(werewolf.currentSprite.rect.x == self.currentSprite.rect.x):
            if(werewolf.currentSprite.rect.y - self.currentSprite.rect.y > 0):
                return "N"
            else:
                return "S"
        elif(werewolf.currentSprite.rect.y == self.currentSprite.rect.y):
            if(werewolf.currentSprite.rect.x - self.currentSprite.rect.x > 0):
                return "W"
            else:
                return "E"
        elif(werewolf.currentSprite.rect.x - self.currentSprite.rect.x > 0):
            if(werewolf.currentSprite.rect.y - self.currentSprite.rect.y > 0):
                return "NW"
            else:
                return "SW"
        else:
            if(werewolf.currentSprite.rect.y - self.currentSprite.rect.y > 0):
                return "NE"
            else:
                return "SE"
            
    def calculateDistance(self, humanPlayer):
        xDistance = self.currentSprite.rect.x - humanPlayer.currentSprite.rect.x
        yDistance = self.currentSprite.rect.y - humanPlayer.currentSprite.rect.y
        return math.sqrt((xDistance ** 2) + (yDistance ** 2))
    
    def draw(self, screen):
        self.currentSprite.draw(screen)
    