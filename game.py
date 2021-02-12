import pygame
from map import Map
from player import Player
from screen import Screen
from input import Input_Handler
from data import Data_Helper
from scriptengine import ScriptEngine
import savegame

white = (255, 255, 255)

class Game:

	def __init__(self):
		#load everything to game
		pygame.init()
		self.screen = Screen(self)

		#reverse __init__
		self.gamepad = self.screen.gamepad
		self.hero = Player()
		self.datahelper = Data_Helper()
		self.scriptengine = ScriptEngine(self)
		self.map = Map(self)
		self.input = Input_Handler(self)

	def load(self, data):
			self.map.load(data)
			self.screen.state["mainmenu"] = False
			self.screen.state["map"] = True

	def main(self):
		self.screen.draw()
		self.scriptengine.tick()
		self.input.main()