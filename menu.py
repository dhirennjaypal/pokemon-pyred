import pygame
#import savegame
from dialog import ChoiceDialog
from box import Box

class Menu:

	def __init__(self, screen, game):
		self.game = game
		self.screen = screen
		self.x = self.screen.screen_size[0] * 0.8
		self.y = 0
		self.w = self.screen.screen_size[0] * 0.2
		self.items = {
			0 : { "name" : "Save", "desc" : "Save the game", "tostate" : "save" }, 
			1 : { "name" : "Return", "desc" : "Close the menu", "tostate" : "map" },
			2 : { "name" : "nothing", "desc" : "Do nothing", "tostate" : "menu" }
		}
		itemsh = 0
		self.length = 0
		for i in self.items:
			itemsh += 20
			self.length += 1
		self.h = itemsh+20
		self.box = Box((self.w, self.h))#pygame.Rect(self.x, self.y, self.w, self.h)
		self.color = (255, 255, 255)
		self.font = 0
		self.current = 0
	
	def draw(self):
		#pygame.draw.rect(self.screen.surface, self.color, self.rect, border_radius=10)
		#pygame.draw.rect(self.screen.surface, (0, 50, 220), self.rect, width=5, border_radius=10)
		self.screen.surface.blit(self.box, (self.x, self.y))
		for i in self.items:
			if i == self.current:
				label = self.screen.font.render(">"+self.items[i]["name"], 1, (0, 0, 0))
			else:
				label = self.screen.font.render(self.items[i]["name"], 1, (0, 0, 0))
			self.screen.surface.blit(label, (self.x+15, self.y+10+20*i))

	def next(self):
		self.current += 1
		if self.current == self.length:
			self.current = 0
	
	def prev(self):
		self.current -= 1
		if self.current == -1 :
			self.current = self.length - 1
	
	def select(self):
		#self.screen.state = self.items[self.current]["tostate"]
		#if self.screen.state == "save":
		#savegame.save(self.game.map, self.game.hero)
		if self.items[self.current]["tostate"] == "save":
			#savegame.save(self.game)
			dialogbox = ChoiceDialog( "Do you want to save game ?", self.screen.surface, {"Yes" : "savegame", "No" : "nothing"}, True)
			self.screen.drawDialog(dialogbox)
		self.screen.state["menu"] = False