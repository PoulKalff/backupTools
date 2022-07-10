import pygame
from helperFunctions import *

class Object():
	""" Representation of any object, other than the player """

	def __init__(self, x, y, speed, updateVal, frames):
		self.xPos = x			# location in the level
		self.yPos = y			# location in the level
		self.animFrames = {}
		self.speed = speed
		self.updateVal = updateVal	# how often frames of object are updated
		for no, frame in enumerate(frames):
			self.animFrames[no] = pygame.image.load(frame)
		self.count = RangeIterator(len(self.animFrames) - 1)







