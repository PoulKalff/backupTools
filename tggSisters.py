#!/usr/bin/python3

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import io
import os
import sys
import math
import time
import json
import pygame
import random
import requests
import argparse
import pygame.locals
from io import BytesIO
from PIL import Image


# --- Variables / Ressources ----------------------------------------------------------------------

pygame.init()
version = '0.20'		# player animation complete
sounds = {}
#backgroundMusic = pygame.mixer.Sound("snd/Mozart.-.Symphony.No.40.1st.Movement.mp3")
#backgroundMusic.set_volume(0.03)
background = pygame.image.load('gfx/background.png')
font30 = pygame.font.Font('freesansbold.ttf', 30)
font60 = pygame.font.Font('freesansbold.ttf', 60)


# --- Functions -----------------------------------------------------------------------------------


# --- Classes -------------------------------------------------------------------------------------


class colorList:
	black =			(0, 0, 0)
	white =			(255, 255, 255)
	red =			(255, 0, 0)
	cyan =			(0, 255, 255)
	green =			(0, 255, 0)
	grey =			(150, 150, 150)
	lightGrey =		(150, 150, 150)
	almostBlack =	(20, 20, 20)
	orange =		(220, 162, 57)
	green =			(70, 180, 50)
	blue =			(80, 120, 250)
	background =	(55, 55, 55)
	yellow = 		(255, 255, 0)



class FlipSwitch():
	""" Represents a switch with on and off-state """

	def __init__(self, Ind):
		self._value = bool(Ind)

	def flip(self):
		if self._value == True:
			self._value = False
		else:
			self._value = True

	def get(self):
		return self._value

	def getString(self):
		return str(self._value)



class RangeIterator():
	# (v3) Represents a range of INTs from 0 -> X

	def __init__(self, Ind, loop=True):
		self.current = 0
		self.max = Ind
		self.loop = loop

	def inc(self, count=1):
		self.current += count
		self._test()

	def dec(self, count=1):
		self.current -= count
		self._test()

	def incMax(self, incCurrent = True):
		""" Increase both value and max valuse """
		self.max += 1
		if incCurrent:
			self.current += 1
		self._test()

	def decMax(self, count=1):
		""" Increase both value and max valuse """
		self.max -= count
		self.current -= count
		self._test()

	def _test(self):
		""" Tests that all is well, should be called after any change in values"""
		self.max = 0 if self.max < 0 else self.max
		if self.loop:
			if self.current > self.max:
				self.current -= self.max + 1
			elif self.current < 0:
				self.current += self.max + 1
		elif not self.loop:
			if self.current >= self.max:
				self.current = self.max
			elif self.current < 0:
				self.current = 0

	def get(self):
		return self.current



class playerMovement():
	""" Representation of the current movement of the player """

	def __init__(self):
		self.left = False
		self.right = False
		self.up = False
		self.down = False

	def verticalMove(self, direction):
		if direction:
			self.left = True
			self.right = False
		else:
			self.left = False
			self.right = True

	def goUp(self):
		self.up = True
		self.down = False

	def goDown(self):
		self.up = False
		self.down = True

	def stop(self):
		self.left = False
		self.right = False
		self.up = False
		self.down = False

	def isMoving(self):
		if self.left or self.right or self.up or self.down:
			return True
		else:
			return False

	def show(self):
		print(int(self.left), int(self.right), int(self.up), int(self.down))



class player():
	""" Representation of the player """

	def __init__(self, parent):
		self.parent = parent
		self.vector = 1				# last direction, left or right
		self.movement = playerMovement()
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
		if self.vector and self.xPos < 850:
			self.xPos += 7
		elif not self.vector and self.xPos > 250:
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
			self.vector = speed > 0
			self.movement.verticalMove(speed > 0)
			self.changeFrame()
			if speed > 0 and self.xPos < 850:
				self.xPos += speed
			elif speed < 0 and self.xPos > 250:
				self.xPos += speed


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









class background():
	""" Representation of the background """

	def __init__(self, parent):
		self.parent = parent
		self.wallpaper = pygame.image.load('gfx/background.png')
		self.xPosBackground = 0
		self.wBackground = self.wallpaper.get_width()



	def update(self):
		pass


	def draw(self):
		self.parent.display.blit(self.wallpaper, (self.xPosBackground, 0))







class tggSisters():
	""" get data from API and display it """

	def __init__(self):
		self.ticks = 0 
		self.width = 1280
		self.height = 720
		pygame.init()
		self.gameTimer = pygame.time.Clock
		self.tickEvent = pygame.USEREVENT + 0
		self.jumpEvent = pygame.USEREVENT + 1
		pygame.time.set_timer(self.tickEvent, 1000)			# register a event to count ticks, to align game to
		pygame.display.set_caption('The Great Greendale Sisters')
		self.display = pygame.display.set_mode((self.width, self.height))


	def run(self):
		self.initGame()
		self.loop()


	def initGame(self):
		self.running = True
		self.player = player(self)
		self.background = background(self)
		pass


	def drawBackground(self):
		self.background.update()
		self.background.draw()


	def drawPlayer(self):
		self.player.update()
		self.player.draw()


	def checkInput(self):
		""" Checks and responds to input from keyboard and mouse """
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					self.running = False
				elif event.key == pygame.K_q:
					self.running = False
				elif event.key == pygame.K_SPACE:
					pass
			elif event.type == self.jumpEvent:					# special events
				self.player.calculateJump()
			elif event.type == self.tickEvent:
				self.ticks += 1
				if 	self.ticks > 60: self.ticks = 0
		keysPressed = pygame.key.get_pressed()
		if keysPressed[pygame.K_UP]:
			if not self.player.kneeling:
				self.player.movement.goUp()
				self.player.jumping = True
				self.player.kneeling = False
				pygame.time.set_timer(self.jumpEvent, 100)			# register a jump-event
		elif keysPressed[pygame.K_DOWN]:
			self.player.movement.goDown()
			if not self.player.jumping: self.player.kneel()
		elif keysPressed[pygame.K_LEFT]:
			self.player.move(-10)
#			if self.xPosBackground < 0:
#				self.xPosBackground += 2
		elif keysPressed[pygame.K_RIGHT]:
			self.player.move(10)
#			if self.wBackground + self.xPosBackground > self.width:
#				self.xPosBackground -= 2
		elif self.player.movement.isMoving() and not self.player.jumping:
			self.player.stop()
#		print(self.player.xPos)





	def loop(self):
		""" Ensure that view runs until terminated by user """
		while self.running:
			self.drawBackground()
			self.drawPlayer()
			self.checkInput()
			pygame.display.update()
		pygame.quit()
		print('  Game terminated gracefully\n')


# --- Main  ---------------------------------------------------------------------------------------


#check arguments
parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=120))
parser.add_argument("-v", "--version",	action="store_true",	help="Print version and exit")
args = parser.parse_args()


colors = colorList
obj =  tggSisters()
obj.run()


# --- TODO ---------------------------------------------------------------------------------------
# - 


# --- NOTES --------------------------------------------------------------------------------------






