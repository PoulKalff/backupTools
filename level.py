#import pygame
#from helperFunctions import *

from background import Background

class Level():
	""" Representation of the background """

	def __init__(self, parent, levelNo):
		self.parent = parent
		self.number = levelNo		# should get level No and read data from file
		self.length = 8320			# The width of the level, in pixel (8320 = 1280 * 6.5)
		self.xPosition = 0			# Where in the level is player	
		self.background = Background(self.parent)



		def triggerEnd(self):
			""" Triggered when player reaches end of level (xPos == self.length) """
			sys.exit('Level ' + str(self.number) + ' Completed!')













