import pygame
from controller import Controller
from menu import Menu
from mainmenu import MainMenu
from foreground import FadeIn, FadeOut

white = (255, 255, 255)

class Screen:

	def __init__(self, game):
		self.screen_size = (640, 360)
		self.font = pygame.font.SysFont("Arial", 20)
		self.surface = pygame.display.set_mode(self.screen_size,pygame.SCALED | pygame.FULLSCREEN)
		self.gamepad = Controller(self.screen_size[0], self.screen_size[1], 60, 60)
		self.dialogbox = None
		self.game = game
		self.mainmenu = MainMenu(self.surface)
		self.menu = Menu(self, self.game)
		self.fade = None
		self.fadein = False
		self.state = { "mainmenu" : True, "map" : False, "dialog" : False, "menu" : False, "fade" : False}

	def drawDialog(self, dialogbox):
		self.dialogbox = dialogbox
		self.state["dialog"] = True
	
	def drawFade(self, fadein = False):
		self.counter = 0
		self.fadein = fadein
		if fadein:
			self.fade = FadeIn(self.surface, 30)
		else:
			self.fade = FadeOut(self.surface, 30)
		self.state["fade"] = True

	def draw(self):
		pygame.display.flip()

		if self.state["mainmenu"]:
			self.mainmenu.draw()

		if self.state["map"]:
			self.game.map.draw()

		if self.state["dialog"]:
			self.dialogbox.draw()
			self.dialogbox.tick()

		if self.state["menu"]:
			self.menu.draw()

		if self.state["fade"]:
			if not self.fade.busy and not self.fadein:
				self.state["map"] = True
				self.drawFade(True)
			self.fade.draw()
			self.fade.tick()
			if self.state["map"] and not self.fadein:
				self.state["map"] = False
			if not self.fade.busy and self.fadein:
				self.fadein = False
				self.state["fade"] = False

		self.gamepad.draw(self.surface, white, self.font)
		pygame.display.flip()
		#test