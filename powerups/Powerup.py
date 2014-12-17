import pygame
from base import Globals

class Powerup(object):

	def __init__(self, x, y, name):

		self.name = name
		self.rect = pygame.Rect(x, y, 16, 16)
		self.speed = 2
		self.active = True

		if name == 'speed':
			self.surface = pygame.image.load(Globals.SPRITE_FILEPATH_SPEED)
			self.speed = 4

		elif name == 'shovel':
			self.surface = pygame.image.load(Globals.SPRITE_FILEPATH_SHOVEL)

		elif name == 'wall':
			self.surface = pygame.image.load(Globals.SPRITE_FILEPATH_HAMMER)

		self.rect = self.surface.get_rect() 
		self.rect.topleft = [x,y]

	def draw_powerup(self, screen):
		screen.blit(self.surface, self.rect)
		#pygame.draw.rect(screen, self.color, self.rect)

	def remove_powerup(self):
		self.color = (0,0,0)

	def apply_powerup(self, player):
		if self.active:
			pygame.mixer.Sound("Music/Powerup.wav").play()
			if self.name == 'speed':
				player.start_speed(self.speed)

			elif self.name == 'shovel':
				player.shovel = True

			elif self.name == 'wall':
				player.wall = True

			self.active = False