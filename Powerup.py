import pygame
from Player import Player

class Powerup(object):



	def __init__(self, x, y, value, type):

		self.name = type
		self.powerupNumber = int(value)
        self.rect = pygame.Rect(x, y, 16, 16)
        self.speed = 2

		if self.name is "speed":
       		self.color = (255, 0, 0)
       		self.speed = 4

		elif self.name is "shovel":
       		self.color = (255, 125, 0)

		elif self.name is "wall":
			self.color = (125, 0, 125)


	def apply_power(player):

		if self.name is "speed":
			player.speed = self.speed
			player.speedTimer = 5

		elif self.name is "shovel":
       		player.shovel = True

		elif self.name is "wall":
			player.wall = True