#
# python imports
#
import pygame
from base import Globals
from base.Sprite import Sprite

#
# Human Sprite Class Module
#
class Human(Sprite):
    # sprite animation frames
    animationFrames = {Globals.ANIMATION_MOVE_DOWN: (4, [(10, 11, 36, 39), (10, 66, 36, 39), (10, 122, 36, 38), (10, 177, 36, 40)]),
              Globals.ANIMATION_MOVE_LEFT: (4, [(63, 11, 35, 40), (64, 67, 35, 40), (64, 123, 35, 39), (64, 178, 34, 39)]),
              Globals.ANIMATION_MOVE_UP:(4, [(122, 12, 35, 38), (122, 67, 35, 38), (122, 123, 35, 38), (122, 178, 35, 38)]),
              Globals.ANIMATION_MOVE_RIGHT:(4, [(178, 12, 35, 39), (178, 67, 35, 39), (178, 123, 35, 39), (178, 178, 35, 39)])}
    
    #
    # default constructor
    #
    def __init__(self):
        Sprite.__init__(self)
        self.currentFrame = 0
        self.currentAnimation = Globals.ANIMATION_MOVE_DOWN
        self.updateFrame(self.animationFrames[self.currentAnimation][1][self.currentFrame])
        self.surface = pygame.image.load(Globals.SPRITE_FILEPATH_HUMAN)
        
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
