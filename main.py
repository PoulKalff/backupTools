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
background = pygame.image.load('gfx/background.png')
font30 = pygame.font.Font('freesansbold.ttf', 30)
font60 = pygame.font.Font('freesansbold.ttf', 60)

# --- Classes -------------------------------------------------------------------------------------

class Main():
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
		self.player = Player(self)
		self.level = Level(self, 1)
		self.level.xPosition = self.player.xPos


	def drawBackground(self):
		self.level.background.draw()


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
			if self.level.xPosition > 0:
				self.player.move(-10)
				self.level.xPosition -= 10


				if self.player.xPos <= self.player.xPosMin:
					self.level.background.move(self.player.vector)




		elif keysPressed[pygame.K_RIGHT]:
			if self.level.xPosition < self.level.length:
				self.player.move(10)
				self.level.xPosition += 10
				if self.player.xPos >= self.player.xPosMax:
					self.level.background.move(self.player.vector)
			else:
				self.player.stop()
		elif self.player.movement.isMoving() and not self.player.jumping:
			self.player.stop()





	def loop(self):
		""" Ensure that view runs until terminated by user """
		while self.running:
			self.drawBackground()
			self.drawPlayer()
			self.checkInput()
			pygame.display.update()


			print(self.level.xPosition, self.level.length)


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
# - 


# --- NOTES --------------------------------------------------------------------------------------






