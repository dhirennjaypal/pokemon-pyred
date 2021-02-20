import pygame
from .map import Map
from .player import Player
from .screen import Screen
from src.backend.input import Input_Handler
from src.backend.data import Data_Helper
from src.backend.scriptengine import ScriptEngine
from src.backend import savegame

white = (255, 255, 255)

class Game:

	def __init__(self):
		#load everything to game
		pygame.init()
		self.screen = Screen(self)
		self.dir = None

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