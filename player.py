import time
import pygame
import random
from helperFunctions import *


class Player():
	""" Representation of the player """

	def __init__(self, parent):
		self.parent = parent
		self.vector = 1				# last direction, left or right
		self.movement = PlayerMovement()
		self.stationary = 0
		self.goingUp = False
		self.kneeling = False
		self.death = 0
		self.standFrame = pygame.image.load('gfx/animRun/standing.png')
		self.kneelFrame = pygame.image.load('gfx/animRun/kneeling.png')
		self.kneelHeadFrame = pygame.image.load('gfx/animHead/kneeling.png')
		self.jumpFrames = {0: pygame.image.load('gfx/animRun/jumpUp.png'), 1 : pygame.image.load('gfx/animRun/jumpDown.png')}
		self.runFrames = {nr : pygame.image.load('gfx/animRun/' + str(nr + 1) + '.png') for nr in range(20)}
		self.headFrames = {nr : pygame.image.load('gfx/animHead/' + str(nr + 1) + '.png') for nr in range(8)}
		self.headDeath  = {0 : pygame.image.load('gfx/animHead/death1.png'), 1 : pygame.image.load('gfx/animHead/death2.png'), 2 : pygame.image.load('gfx/animHead/death1.png')}
		self.deathScreen = pygame.image.load('gfx/deathScreen.png')
		self.frameNo = RangeIterator(19)
		self.currentBody = self.runFrames[self.frameNo.get()]
		self.currentHead = self.headFrames[0]
		y, x  = pygame.display.get_surface().get_size()
		self.size = self.runFrames[1].get_rect().size
		self.yAcc = 30
		self.xPos = 300
		self.yPosLevel = x - self.runFrames[1].get_height() - 40
		self.yPos = self.yPosLevel
		self.xPosMin = 350
		self.xPosMax = 650


	def onGround(self):
		return self.yPos == self.yPosLevel


	def showDeath(self, xPos, yPos):
		""" paint 10 heads flying in different directions, from starting point """
		yPos -= 20
		posMatrix = [
						[[0, 10], [2, -24], [-34, -39], [-59, -26], [8, 5], [10, 38], [12, 91], [16, 176], [20, 312], [25, 529], [30, 846]] ,
						[[0, -24], [10, -39], [20, -26], [30, 5], [45, 38], [60, 91], [85, 176], [110, 312], [150, 529], [200, 846], [250, 1000]] ,
						[[0, -39], [50, -26], [100, 5], [150, 38], [175, 91], [200, 176], [225, 312], [250, 529], [275, 846], [265, 1000], [270, 1000]] ,
						[[0, -26], [25, 5], [50, 38], [75, 91], [87, 176], [100, 312], [112, 529], [125, 846], [137, 1000], [132, 1000], [122, 1000]] ,
						[[0, 5], [25, 38], [50, 91], [75, 176], [87, 312], [100, 529], [112, 846], [125, 1000], [137, 1000], [132, 1000], [122, 1000]] ,
						[[0, 38], [32, 91], [65, 176], [97, 312], [113, 529], [130, 846], [145, 1000], [162, 1000], [178, 1000], [171, 1000], [158, 1000]] 
					]
		if self.parent.ticks % 6:
			time.sleep(0.05)
		if self.death == 11:
			""" Show screen while delaying """
			time.sleep(1)
			self.parent.display.blit(self.deathScreen , (0, 0))
			pygame.display.update()
			time.sleep(3)
			self.parent.initGame()
		for head in range(6):
		#	head = 0
			self.parent.display.blit(self.headDeath[random.randint(0,2)], (xPos + posMatrix[head][self.death - 1][0], yPos + posMatrix[head][self.death - 1][1]) )
			self.parent.display.blit(self.headDeath[random.randint(0,2)], (xPos - posMatrix[head][self.death - 1][0], yPos + posMatrix[head][self.death - 1][1]) )
		self.death += 1
		return 1



	def update(self):
		if self.stationary and self.parent.ticks > self.stationary + 4:
			frame = self.parent.ticks % 4 if self.movement.isMoving() else self.parent.ticks % 8
		else:
			frame = self.parent.ticks % 4
		self.calculateJump()
		self.changeBody()
		self.changeHead(frame)
		if not self.movement.isMoving():
			self.stop()



	def changeBody(self):
		if self.onGround():
			if self.movement.left or self.movement.right:
				self.currentBody = self.runFrames[self.frameNo.get()]
			else:
				self.currentBody = self.kneelFrame if self.kneeling else self.standFrame
		elif self.goingUp:
			self.currentBody = self.jumpFrames[0] 		# going up
		else:
			self.currentBody = self.jumpFrames[1]		# going down
		if not self.vector:
			self.currentBody = pygame.transform.flip(self.currentBody, True, False)



	def changeHead(self, frame):
		self.currentHead = self.kneelHeadFrame if self.kneeling else self.headFrames[frame]
		if not self.vector:
			self.currentHead = pygame.transform.flip(self.currentHead, True, False)


	def calculateJump(self):
		if self.goingUp and self.yPos > 200:
			self.yPos -= 15
			self.movement.goUp()
		else:
			self.goingUp = False
			if self.yPos < self.yPosLevel:		# if player is in the air 
				self.movement.goDown()
				self.yPos += 10			# gravity
				if self.yPos > self.yPosLevel:
					self.yPos = self.yPosLevel


	def move(self, speed):
		self.frameNo.inc()
		self.kneeling = False
		self.movement.verticalMove(speed > 0)
		if speed != 0:
			self.xPos += speed
			self.vector = True if speed > 0 else False


	def stop(self):
		self.frameNo.current = 0
		self.stationary = self.parent.ticks
		self.movement.stop()
		self.idle = self.parent.ticks


	def getHeadCoord(self):
		if self.kneeling:
			x = self.xPos + (105 if self.vector else -15)
			y = self.yPos + 110
		else:
			x = self.xPos + (60 if self.vector else 25)
			y = self.yPos - 30
		return (x,y)


	def draw(self):
		if self.death:
			self.showDeath(self.xPos, self.yPos)
		else:
			self.parent.display.blit(self.currentBody, (self.xPos, self.yPos) )
			self.parent.display.blit(self.currentHead, self.getHeadCoord() )
