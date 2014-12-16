#
# python imports
#
import pygame
from base import Globals
from base.Sprite import Sprite

#
# Werewolf Sprite Class Module
#
class Werewolf(Sprite):
    # sprite animation frames
    animationFrames = {Globals.ANIMATION_MOVE_DOWN: (4, [(370, 0, 34, 47), (432, 1, 34, 47), (488, 1, 33, 50), (545, 3, 34, 48)]),
              Globals.ANIMATION_MOVE_LEFT: (4, [(196, 120, 35, 46), (134, 121, 40, 46), (67, 120, 39, 46), (8, 120, 40, 46)]),
              Globals.ANIMATION_MOVE_UP:(4, [(81, 61, 34, 49), (126, 59, 34, 50), (175, 61, 33, 49), (215, 60, 34, 49)]),
              Globals.ANIMATION_MOVE_RIGHT:(4, [(128, 1, 36, 45), (186, 2, 37, 45), (252, 2, 37, 45), (308, 2, 40, 44)]),
              Globals.ANIMATION_TRANSFORM: (4, [(370, 123, 34, 43), (424, 123, 34, 46), (490, 123, 34, 47), (545, 127, 34, 46)])}
    
    #
    # default constructor
    #
    def __init__(self):
        Sprite.__init__(self)
        self.currentFrame = 0
        self.currentAnimation = Globals.ANIMATION_MOVE_DOWN
        self.updateFrame(self.animationFrames[self.currentAnimation][1][self.currentFrame])
        self.surface = pygame.image.load(Globals.SPRITE_FILEPATH_WEREWOLF)
        
    #
    # set animation
    #
    def setAnimation(self, animation):
        # reset current animation
        if self.currentAnimation != animation:
            self.currentFrame = 0
        
        # update current animation
        self.currentAnimation = animation
     
    #
    # update sprite
    #
    def update(self):
        # get up animation frames
        animation = self.animationFrames.get(self.currentAnimation)
        
        # validate animation
        if animation != None:
           
            # update sprite frame
            self.updateFrame(animation[1][self.currentFrame])
            
            # update current frame
            self.currentFrame = self.currentFrame + 1 if self.currentFrame + 1 < animation[0] else 0
