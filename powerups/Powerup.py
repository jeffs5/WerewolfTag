import pygame

class Powerup(object):

	def __init__(self, x, y, name):

		self.name = name
		self.rect = pygame.Rect(x, y, 16, 16)
		self.color = (255,255, 0)
		self.speed = 2
		self.active = True

		if name == 'speed':
			self.color = (255, 0, 0)
			self.speed = 4

		elif name == 'shovel':
			self.color = (255, 125, 0)

		elif name == 'wall':
			self.color = (125, 0, 125)

	def draw_powerup(self, screen):
		pygame.draw.rect(screen, self.color, self.rect)

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