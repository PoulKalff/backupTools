import json
from objects import Object

from background import Background

class Level():
	""" Representation of the background """

	def __init__(self, parent, levelNo, startPos = 0):
		self.parent = parent
		# read data
		with open('levelData.json') as json_file:
			self.levelData = json.load(json_file)['levels'][str(levelNo)]
		self.xPosMax = self.levelData['length']		# The width of the level, in pixel
		self.xPos = int(startPos * self.xPosMax) if startPos else 0




										# Where in the level is player	
		self.background = Background(self.parent, self.levelData, self.xPos)
		self.objects = [Object()]	# List of objects bound to the level (portal, toadstool, etc..)



	def move(self, speed):
		if speed > 0 and self.xPos < self.xPosMax:
			self.xPos += speed
			self.background.move(True)
		elif speed < 0 and self.xPos > 0:
			self.xPos += speed
			self.background.move(False)



	def update(self):
		self.background.draw()
		for obj in self.objects:
			if self.xPos < obj.xPos < self.xPos + self.parent.width + 100: #obj.animFrames[0].width:
				self.parent.display.blit(obj.animFrames[0], (self.parent.width - (self.xPos + self.parent.width - obj.xPos), obj.yPos))




	def triggerEnd(self):
		""" Triggered when player reaches end of level (level.xPos == self.length) """
		import sys
		sys.exit('Level ' + str(self.levelData['levelNo']) + ' Completed!')


















