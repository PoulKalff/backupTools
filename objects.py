import pygame
from helperFunctions import *

class Object():
	""" Representation of any object, other than the player """

	def __init__(self):
		self.animFrames = { 0: pygame.image.load('gfx/portal.png') }
		self.xPos = 18500 + 1200	# location in the level
		self.yPos = 365				# location in the level






