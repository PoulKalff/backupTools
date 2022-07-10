import json
import time
import pygame

from objects import Object
from helperFunctions import *
from background import Background

class Level():
	""" Representation of the background """

	def __init__(self, parent, levelNo, startPos = 0):
		self.parent = parent
		# read data
		with open('levelData.json') as json_file:
			self.levelData = json.load(json_file)['levels'][str(levelNo)]
		self.xPosMax = self.levelData['length']		# The width of the level, in pixel
		self.xPos = int(startPos * self.xPosMax) if startPos else 0					# Where in the level is player
#		self.xPos = 17000
		self.background = Background(self.parent, self.levelData, self.xPos)
		self.objects = [Object(*obj) for obj in self.levelData['objects']]		# List of objects bound to the level (portal, toadstool, etc..)
		self.visibleObjects = []
		self.counter = RangeIterator(11)	# for counting when to update frames
		self.endScreen = pygame.image.load(self.levelData['endScreen'])


#		print(self.objects)
#		import sys
#		sys.exit('Kileld for DEV')




	def move(self, speed):
		if speed > 0 and self.xPos < self.xPosMax:
			self.xPos += speed
			self.background.move(True)
		elif speed < 0 and self.xPos > 0:
			self.xPos += speed
			self.background.move(False)



	def update(self):
		self.background.draw()
		self.visibleObjects = []
		for obj in self.objects:
			if self.xPos < obj.xPos < self.xPos + self.parent.width + 100:
				self.visibleObjects.append(obj)
		for obj in self.visibleObjects:
			# animate
			self.counter.inc()
			if (self.counter.get() + 1) % obj.updateVal == 0:
				obj.count.inc()
			# move
			obj.xPos -= obj.speed
			# show
			self.parent.display.blit(obj.animFrames[obj.count.get()], (self.parent.width - (self.xPos + self.parent.width - obj.xPos), obj.yPos))



	def triggerEnd(self):
		""" Triggered when player reaches end of level (level.xPos == self.length) """
		self.parent.display.blit(self.endScreen , (0, 0))
		pygame.display.update()
		time.sleep(7)
		
		self.parent.running = False

















