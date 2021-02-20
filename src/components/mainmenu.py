import pygame
from . import box
#import controller
from src.backend import savegame
from src.backend import data

OBJECTBUFFER = 5
BORDER = 10
LINEBUFFER = 10

white = (255, 255, 255)
screen_size = (640, 360)

class Infobox:
	
	def __init__(self, screen, font, title=None, info={}, order=[]):
		numLines = len(info)

		if title is not None:
			numLines += 1

		self.height = ((font.get_height()+LINEBUFFER)*numLines)+(BORDER*2)
		self.width = screen.get_width()/2
		self.box = box.Box((self.width, self.height)).convert(screen)

		i = 0
		if title is not None:
			location = BORDER*3, BORDER
			#fFont.writeText(title, self.box, location)
			#writetext start
			px, py = location
			for ch in title:
				label = font.render(ch, 1, (0, 0, 0))
				self.box.blit(label, (px, py))
				px += font.size(ch)[0]
			#writetextend
			i += 1
			
			for param in order:
				location = BORDER+10, (i*(font.get_height()+LINEBUFFER))+BORDER
				#fFont.writeText(param, self.box, location)
				#writetext start
				px, py = location
				for ch in param:
					label = font.render(ch, 1, (0, 0, 0))
					self.box.blit(label, (px, py))
					px += font.size(ch)[0]
				#writetextend
				location = self.width/2, (i*(font.get_height()+LINEBUFFER))+BORDER
				#fFont.writeText(info[param], self.box, location)
				#writetext start
				px, py = location
				for ch in info[param]:
					label = font.render(ch, 1, (0, 0, 0))
					self.box.blit(label, (px, py))
					px += font.size(ch)[0]
				#writetextend
				i += 1

class MainMenu:

	def __init__(self, screen):
		self.screen = screen
		self.font = pygame.font.Font("gfx/pkmnfl.ttf", 20)
		self.boxes = []
		
		#load save file data here later
		data = savegame.load()
		if data:
			info = {"Player": "Soon", "Time": "Soon", "Pokedex": "Soon", "Badges": "Soon", "Location" : data["mapname"],
		"Coords" : "( "+str(data["player"]["x"])+", "+str(data["player"]["y"])+" )" }
			order = ["Location", "Coords", "Player", "Time", "Pokedex", "Badges"]
		
			continueBox = Infobox(self.screen, self.font, "CONTINUE", info, order)
			self.boxes.append(continueBox)
		newgameBox = Infobox(self.screen, self.font, "NEW GAME")
		self.boxes.append(newgameBox)
		
		self.shadow = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
		self.shadow.fill((10,10,10))
		self.shadow.set_alpha(100)
		self.current = 0
		self.keysJustPressed = "None"

	def giveInput(self, key):
		if key == "A":
			return self.select()
		elif key == "Up":
			if self.current > 0:
				self.current -= 1
			else:
				self.current = len(self.boxes)-1
		elif key == "Down":
			if self.current < len(self.boxes)-1:
				self.current += 1
			else:
				self.current = 0
		return False

	def draw(self):
		self.screen.fill((0,0,50))

		pointerY = OBJECTBUFFER
		for i in range(0, len(self.boxes)):
			if i != self.current:
				location = (self.screen.get_width()-self.boxes[i].width)/2, pointerY
				self.screen.blit(self.boxes[i].box, location)
			else:
				locationY = pointerY
			pointerY += self.boxes[i].height + OBJECTBUFFER

		self.screen.blit(self.shadow, (0,0))
		location = (self.screen.get_width()-self.boxes[i].width)/2, locationY
		self.screen.blit(self.boxes[self.current].box, location)
	
	def select(self):
		if len(self.boxes) > 1:
			if self.current == 0:
				return savegame.load()
		dh = data.Data_Helper()
		return dh.warps["Starting Map"]