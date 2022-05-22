import pygame
from helperFunctions import *

class Background():
	""" Representation of the background """

	def __init__(self, parent):
		self.parent = parent
		self.pavement = pygame.image.load('gfx/pavement.png')
		self.wallpaper = pygame.image.load('gfx/background.png')
		self.wallpaperDim = self.wallpaper.get_size()
		self.pavementOffset = RangeIterator(8)
		self.xPosBackground = 0



	def move(self, direction):
		""" Move the bacground left or right """
		if direction:
			self.pavementOffset.dec()
			if self.xPosBackground > -(self.wallpaperDim[0] - self.parent.width):
				self.xPosBackground -= 2
		else:
			self.pavementOffset.inc()
			if self.xPosBackground < 0:
				self.xPosBackground += 2
#		print(-(self.wallpaperDim[0] - self.parent.width))



	def draw(self):
		self.parent.display.blit(self.wallpaper, (self.xPosBackground, 0))
		for tile in range(-80, 1360, 80):
			self.parent.display.blit(self.pavement, (tile + 10 * self.pavementOffset.get() , self.parent.height - 80))

