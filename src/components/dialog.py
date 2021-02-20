import pygame
#import controller
from . import box
from . import foreground

LINESEP = "$$"
OBJECTBUFFER = 0
LINEBUFFER = 10
BORDER = 20
TRANS = (255, 0, 255)

name = "Dhiren"
items = { 0 : "Town Map", 1 : "TM Case" }

class Dialog(foreground.ForegroundObject):

	def __init__(self, text, screen, drawCursor = False):
		#setup
		iscommand = False
		command = ""
		for ch in text:
			if ch == "{":
				iscommand = True
			if iscommand:
				command = command+ch
			if ch == "}":
				if "name" in command:
					text = text.replace(command, "@"+name+"@")
				elif "item" in command:
					number = command.translate(command.maketrans("{item}", "      "))
					text = text.replace(command, "#"+items[int(number)]+"#")
				command = ""
				iscommand = False
		#end setup
		self.temp = text
		self.text = text.split(LINESEP)
		self.screen = screen
		self.drawCursor = drawCursor
		transparency = TRANS

		if not "speed" in self.__dir__():
			self.speed = 1
		self.font = pygame.font.Font("gfx/pkmnfl.ttf", 25)
		size = (self.screen.get_width()-(OBJECTBUFFER*2), (len(self.text)*(self.font.get_height()+LINEBUFFER))-LINEBUFFER+(BORDER*2)+5)
		self.box = box.Box(size).convert_alpha(self.screen)

		#load cursor
		self.cursor = pygame.image.load("gfx/cursor.png").convert_alpha(self.screen)
		self.cursor = pygame.transform.scale(self.cursor, (10, 10))
		self.cursor.set_colorkey(transparency)
		self.cursorLocation = (self.screen.get_width()-OBJECTBUFFER-BORDER-self.cursor.get_width(), self.screen.get_height()-OBJECTBUFFER-BORDER-self.cursor.get_height())
		
		self.sideCursor = pygame.transform.rotate(self.cursor, 90)
		self.sideCursor = pygame.transform.scale(self.sideCursor, (10, 10))
		self.sideCursor.set_colorkey(transparency)

		self.location = OBJECTBUFFER, self.screen.get_height()-size[1]-OBJECTBUFFER
		
		self.progress = 0
		self.writing = True
		self.busy = True

	def draw(self):
		c = 0
		started = False
		color = (0, 0, 0)
		for i in range(0, len(self.text)):
			line = self.text[i]
			location = BORDER, BORDER+(i*(self.font.get_height()+LINEBUFFER))
			charsOnLine = self.progress - c
			if charsOnLine < len(line):
				cutText = line[:charsOnLine]
			else:
				cutText = line
			#writetext start
			px, py = location
			for ch in cutText:
				if started and (ch == "#" or ch =="@"):
					started = False
					color = (0, 0, 0)
				elif ch == "#" and not started:
					color = (0, 0, 255)
					started = True
				elif ch == "@" and not started:
					color = (0, 255, 0)
					started = True
				else:
					label = self.font.render(ch, 1, color)
					self.box.blit(label, (px, py))
					px += self.font.size(ch)[0]
				#writetextend
			c += len(cutText)
		self.screen.blit(self.box, self.location)
		
		if not self.writing and self.drawCursor:
			self.screen.blit(self.cursor, self.cursorLocation)

	def tick(self):
		self.progress += self.speed
		if self.progress > sum(map(len, self.text)):
			self.writing = False

	def inputButton(self, button):
		if button in ("A", "B"):
			if not self.writing:
				self.busy = False

class ChoiceDialog(Dialog):

	def __init__(self, text, screen, choices, drawCursor = False):
		Dialog.__init__(self, text, screen, drawCursor = drawCursor)
		self.choicedict = choices
		self.choices = []
		for choice in self.choicedict:
			self.choices.append(choice)

		maxWidth = max(map(self.font.size, self.choices))[0]
		size = (maxWidth+(BORDER*2)+self.font.size(">")[0], ((self.font.get_height()+LINEBUFFER)*len(self.choices))-LINEBUFFER+(BORDER*2))
		self.choiceBox = box.Box(size).convert(self.screen)
		#self.choiceBox.fill((255, 255, 255))
		if not "current" in self.__dir__():
			self.current = 0
		
		self.choiceLocation = (self.screen.get_width()-self.choiceBox.get_width()-OBJECTBUFFER, self.location[1]-self.choiceBox.get_height()-OBJECTBUFFER)

	def draw(self):
		Dialog.draw(self)

		if not self.writing:
			self.screen.blit(self.choiceBox, self.choiceLocation)
			cursorLocation = (self.choiceLocation[0]+BORDER-5,self.choiceLocation[1]+BORDER+(self.current*(self.font.get_height()+LINEBUFFER))+5)
			self.screen.blit(self.sideCursor, cursorLocation)

		for i in range(0, len(self.choices)):
			choice = self.choices[i]
			location = BORDER+self.sideCursor.get_width(), BORDER+(i*(self.font.get_height()+LINEBUFFER))
			#writetext start
			px, py = location
			for ch in choice:
				label = self.font.render(ch, 1, (0, 0, 0))
				self.choiceBox.blit(label, (px, py))
				px += self.font.size(ch)[0]
			#writetextend
		self.choiceLocation = (self.screen.get_width()-self.choiceBox.get_width()-OBJECTBUFFER, self.location[1]-self.choiceBox.get_height()-OBJECTBUFFER)

	def inputButton(self, button):
		Dialog.inputButton(self, button)
		
		if button == "Down":
			if self.current < len(self.choices)-1:
				self.current += 1
		elif button == "Up":
			if self.current > 0:
				self.current -= 1
		
		if self.busy == False:
			selected = self.choicedict[self.choices[self.current]]
			return selected
