import pygame
from base import Globals

class Placeable(object):

    def __init__(self, x, y, pType):

        self.type = pType
        self.active = True

        if self.type == 'hole':
            #self.color = (125, 125, 125)
            self.surface = pygame.image.load(Globals.SPRITE_FILEPATH_HOLE)
        
        elif self.type == 'wall':
            #self.color = (125, 0, 125)
            self.surface = pygame.image.load(Globals.SPRITE_FILEPATH_BARN)
           

        self.rect = self.surface.get_rect() 
        self.rect.topleft = [x,y]

    def draw_placeable(self, screen):
        screen.blit(self.surface, self.rect)
        # pygame.draw.rect(screen, self.color, self.rect)

        #not used
    def trigger_hole(self):
        self.active = False
