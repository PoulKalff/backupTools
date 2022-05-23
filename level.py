#import pygame
#from helperFunctions import *

from background import Background

class Level():
	""" Representation of the background """

	def __init__(self, parent, levelNo):
		self.parent = parent
		self.number = levelNo		# should get level No and read data from file
		self.xPosMax = 8320			# The width of the level, in pixel (8320 = 1280 * 6.5)
		self.xPos = 0				# Where in the level is player	
		self.background = Background(self.parent)


	def move(self, speed):
		if speed > 0 and self.xPos < self.xPosMax:
			self.xPos += speed
			self.background.move(True)
		elif speed < 0 and self.xPos > 0:
			self.xPos += speed
			self.background.move(False)




	def triggerEnd(self):
		""" Triggered when player reaches end of level (xPos == self.length) """
		import sys
		sys.exit('Level ' + str(self.number) + ' Completed!')


















