from base import Globals
from player.Human import Human
from player.Werewolf import Werewolf

class SinglePlayer(object):
    
    def __init__(self):
        self.humanSprite = Human()
        self.werewolfSprite = Werewolf()
        self.currentSprite = self.humanSprite
    
    def update(self,dx,dy,direction):
        self.currentSprite.rect.x +=dx
        self.currentSprite.rect.y +=dy
        self.currentSprite.setAnimation(direction)
        self.currentSprite.update()
        
    def draw(self, screen):
        self.currentSprite.draw(screen)
