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

from helperFunctions import *
from player import Player
from level import Level

# --- Variables / Ressources ----------------------------------------------------------------------

pygame.init()
version = '0.20'		# player animation complete
sounds = {}
#backgroundMusic = pygame.mixer.Sound("snd/Mozart.-.Symphony.No.40.1st.Movement.mp3")
#backgroundMusic.set_volume(0.03)
font30 = pygame.font.Font('freesansbold.ttf', 30)
font60 = pygame.font.Font('freesansbold.ttf', 60)


# --- Classes -------------------------------------------------------------------------------------

class Main():
	""" get data from API and display it """

	def __init__(self):
		self.ticks = 0 
		self.width = 1280
		self.height = 720
		self.time_down = 0.0
		self.time_elapsed = 0.0
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
		self.player = Player(self)
		self.level = Level(self, 1)
		self.level.xPosition = self.player.xPos


	def showProgressBar(self):
		percentage = (self.level.xPos + self.player.xPos) / (self.width + self.level.xPosMax)
		barWidth = self.width - 200
		pygame.draw.rect(self.display, (70, 180, 50), (100, 30, barWidth, 20))	# bar
		pygame.draw.rect(self.display, (0, 0, 0),     (100 + (barWidth * percentage), 30, 2, 20))	# player location



	def checkInput(self):
		""" Checks and responds to input from keyboard and mouse """
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			# --- Key Down Events ---------------------------------------------
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					if self.player.yPos == self.player.yPosLevel:
						self.player.goingUp = True
				elif event.key == pygame.K_DOWN:
					self.player.kneeling = True
			# --- Key Up Events -----------------------------------------------
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_ESCAPE:
					self.running = False
				elif event.key == pygame.K_UP:
					self.player.goingUp = False
				elif event.key == pygame.K_DOWN:
					self.player.kneeling = False
				elif event.key == pygame.K_q:
					self.running = False
				elif event.key == pygame.K_SPACE:
					pass
			elif event.type == self.tickEvent:
				self.ticks += 1
				if self.ticks > 60: self.ticks = 0
		keysPressed = pygame.key.get_pressed()
		# --- FOR DEV ------------------------------------------------------
		if keysPressed[pygame.K_d]:
			self.player.death = 1
		# --- FOR DEV ------------------------------------------------------
		elif keysPressed[pygame.K_LEFT]:
			# move player
			if self.player.xPos > self.player.xPosMin:
				self.player.move(-10)
			elif self.level.xPos == 0 and self.player.xPos > 0:
				self.player.move(-10)
			elif self.level.xPos == 0 and self.player.xPos == 0:
				self.player.stop()
			else:
				self.player.move(0)
			# move level
			if self.level.xPos > 0 and self.player.xPos == self.player.xPosMin:
				self.level.move(-10)
		elif keysPressed[pygame.K_RIGHT]:
			# move player
			if self.player.xPos < self.player.xPosMax:
				self.player.move(10)
			elif self.level.xPos == self.level.xPosMax and self.player.xPos < self.width:
				self.player.move(10)
			elif self.level.xPos == self.level.xPosMax and self.player.xPos == self.player.xPosMax:
				self.player.stop()
			else:
				self.player.move(0)
			# move level
			if self.level.xPos < self.level.xPosMax and self.player.xPos == self.player.xPosMax:
				self.level.move(10)
			# check complete
			if self.player.xPos >= self.width:
				self.level.triggerEnd()
		elif self.player.movement.isMoving() and not self.player.goingUp and self.player.yPos == self.player.yPosLevel:
			self.player.stop()



	def checkCollision(self):
		""" check if player's gfx overlaps any enemy's gfx """
		bX, bY = self.player.currentBody.get_rect().size
		hX, hY = self.player.currentHead.get_rect().size
		xPosHead, yPosHead = self.player.getHeadCoord()
		bodyRect = pygame.Rect(self.player.xPos, self.player.yPos, bX, bY) 
		headRect = pygame.Rect(xPosHead, yPosHead, hX, hY) 
		# --- FOR DEV ----------------------------------------------------------
		pygame.draw.rect(self.display, (0,255,0), bodyRect, 1)			# draw GREEN body collision rect
		pygame.draw.rect(self.display, (255,0,0), headRect, 1)		# draw RED head collision rect
		# --- FOR DEV ----------------------------------------------------------
		for obj in self.level.visibleObjects:
			objSize = obj.animFrames[obj.count.get()].get_rect().size
			objRect = pygame.Rect(self.width - (self.level.xPos + self.width - obj.xPos), obj.yPos, *objSize)
			# --- FOR DEV ----------------------------------------------------------
			pygame.draw.rect(self.display, (0,0,255), objRect, 1)			# draw BLUE body collision rect
			# print(bodyRect, objRect, pygame.Rect.colliderect(bodyRect, objRect))
			# --- FOR DEV ----------------------------------------------------------
			if pygame.Rect.colliderect(bodyRect, objRect) or pygame.Rect.colliderect(headRect, objRect):
				self.player.death = 1
		return 1




	def loop(self):
		""" Ensure that view runs until terminated by user """
		while self.running:
			self.checkInput()
			self.level.update()
			self.player.update()
			self.player.draw()
			self.showProgressBar()
			if not self.player.death:
				self.checkCollision()
			pygame.display.update()
	#		self.player.movement.show()
		pygame.quit()
		print('  Game terminated gracefully\n')


# --- Main  ---------------------------------------------------------------------------------------


#check arguments
parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog,max_help_position=120))
parser.add_argument("-v", "--version",	action="store_true",	help="Print version and exit")
args = parser.parse_args()


colors = colorList
obj =  Main()
obj.run()


# --- TODO ---------------------------------------------------------------------------------------
# - enemies move more advanced, eg jump, move back/forth, change speed
# - vaaben/skud?
# - use build-in ticks i stedet for self.ticks
# - noget mindre hidsig collision detection... mindre rect inden i playe rect?



# --- NOTES --------------------------------------------------------------------------------------






