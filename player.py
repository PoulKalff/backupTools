import pygame
from helperFunctions import *


class Player():
	""" Representation of the player """

	def __init__(self, parent):
		self.parent = parent
		self.vector = 1				# last direction, left or right
		self.movement = PlayerMovement()
		self.stationary = 0
		self.jumping = False
		self.kneeling = False
		self.standFrame = pygame.image.load('gfx/animRun/standing.png')
		self.kneelFrame = pygame.image.load('gfx/animRun/kneeling.png')
		self.kneelHeadFrame = pygame.image.load('gfx/animHead/kneeling.png')
		self.jumpFrames = {0: pygame.image.load('gfx/animRun/jumpUp.png'), 1 : pygame.image.load('gfx/animRun/jumpDown.png')}
		self.runFrames = {nr : pygame.image.load('gfx/animRun/' + str(nr + 1) + '.png') for nr in range(20)}
		self.headFrames = {nr : pygame.image.load('gfx/animHead/' + str(nr + 1) + '.png') for nr in range(8)}
		self.frameNo = RangeIterator(19)
		self.currentBody = self.runFrames[self.frameNo.get()]
		self.currentHead = self.headFrames[0]
		y, x  = pygame.display.get_surface().get_size()
		self.size = self.runFrames[1].get_rect().size
		self.yAcc = 30
		self.xPos = 300
		self.yPos = x - self.runFrames[1].get_height() - 30
		self.xPosMin = 250
		self.xPosMax = 850


	def update(self):
		if self.stationary and self.parent.ticks > self.stationary + 4:
			frame = self.parent.ticks % 4 if self.movement.isMoving() else self.parent.ticks % 8
		else:
			frame = self.parent.ticks % 4
		self.changeHead(frame)



	def changeFrame(self):
		self.frameNo.inc()
		self.currentBody = self.runFrames[self.frameNo.get()]
		if not self.vector:
			self.currentBody = pygame.transform.flip(self.currentBody, True, False)



	def changeHead(self, frame):
		self.currentHead = self.kneelHeadFrame if self.kneeling else self.headFrames[frame]
		if not self.vector:
			self.currentHead = pygame.transform.flip(self.currentHead, True, False)


	def kneel(self):
		self.kneeling = True
		self.currentBody = self.kneelFrame
		if not self.vector:
			self.currentBody = pygame.transform.flip(self.currentBody, True, False)



	def calculateJump(self):
		if self.vector and self.xPos < self.xPosMax:
			self.xPos += 7
		elif not self.vector and self.xPos > self.xPosMin:
			self.xPos -= 10
		self.yPos -= self.yAcc
		self.yAcc -= 2
		if self.yAcc > 0:
			self.currentBody = self.jumpFrames[0] if self.vector else pygame.transform.flip(self.jumpFrames[0] , True, False)
		else:
			self.currentBody = self.jumpFrames[1]  if self.vector else pygame.transform.flip(self.jumpFrames[1], True, False)
		if self.yPos >= 448:
			self.yPos = 448
			self.yAcc = 30
			self.jumping = False
			pygame.time.set_timer(self.parent.jumpEvent, 0)			# un-register the jump-event
			self.currentBody = self.standFrame if self.vector else pygame.transform.flip(self.standFrame, True, False)



	def move(self, speed):
		if not self.jumping:
			self.kneeling = False
			self.movement.verticalMove(speed > 0)
			self.changeFrame()
			if speed != 0:
				self.xPos += speed
				self.vector = True if speed > 0 else False




	def stop(self):
		self.frameNo.current = 0
		self.stationary = self.parent.ticks
		self.kneeling = False
		self.movement.stop()
		self.idle = self.parent.ticks
		self.currentBody = self.standFrame if self.vector else pygame.transform.flip(self.standFrame, True, False)


	def getHeadCoord(self):
		if self.kneeling:
			x = self.xPos + (105 if self.vector else -15)
			y = self.yPos + 110
		else:
			x = self.xPos + (60 if self.vector else 25)
			y = self.yPos - 30
		return (x,y)


	def draw(self):
		self.parent.display.blit(self.currentBody, (self.xPos, self.yPos) )
		self.parent.display.blit(self.currentHead, self.getHeadCoord() )

