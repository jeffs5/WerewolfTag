import pygame

class Placeable(object):

    def __init__(self, x, y, pType):
        self.rect = pygame.Rect(x, y, 25, 25)
        self.type = pType
        self.active = True
        self.color = (0, 0, 0)
        if self.type == 'hole':
            self.color = (125, 125, 125)
        
        if self.type == 'wall':
            self.color = (125, 0, 125)

    def draw_placeable(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def trigger_hole(self):
        self.active = False
