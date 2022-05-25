import pygame
from helperFunctions import *

class Background():
	""" Representation of the background. Should ONLY be moved by level-class! """

	def __init__(self, parent, levelData, xPos):
		self.parent = parent
		self.tile = pygame.image.load(levelData['TilePath'])
		self.layer = pygame.image.load(levelData['layerPath'])
		self.background = pygame.image.load(levelData['bgPath'])
		self.layerDim = self.layer.get_size()
		self.pavementOffset = RangeIterator(8)
		self.xPosBackground = xPos / -5



	def move(self, direction):
		""" Move the bacground left or right """
		if direction:
			self.pavementOffset.dec()
			if self.xPosBackground > -(self.layerDim[0] - self.parent.width):
				self.xPosBackground -= 2
		else:
			self.pavementOffset.inc()
			if self.xPosBackground < 0:
				self.xPosBackground += 2


	def draw(self):
		self.parent.display.blit(self.background, (0, 0))
		self.parent.display.blit(self.layer, (self.xPosBackground, 0))
		for t in range(-80, 1360, 80):
			self.parent.display.blit(self.tile, (t + 10 * self.pavementOffset.get() , self.parent.height - 80))

