import pygame

class Textbox:

	def __init__(self, screen):
		self.screen = screen
		self.x = self.screen.screen_size[0] * 0.25
		self.y = self.screen.screen_size[1] * 0.7
		self.w = self.screen.screen_size[0] * 0.5
		self.h = self.screen.screen_size[1] * 0.3
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
		#image start
		image = pygame.image.load("gfx/box.png").convert_alpha()
		self.image = pygame.transform.scale(image, (round(self.w), round(self.h)))
		#image end
		self.color = (255, 255, 255)
		self.font = 0
		self.text = ""
		self.letters = {}
		self.current = 0
		self.length = 0
		self.concat = ""
		self.prevtext = self.text
	
	def draw(self):
		if self.text != self.prevtext:
			i = 0
			for letter in self.text:
				self.letters[i] = letter
				i+=1
			self.length = i
			self.prevtext = self.text
		self.screen.surface.blit(self.image, self.rect)
		if self.current < self.length:
			self.concat += self.letters[self.current]
			self.current += 1
			label = self.screen.font.render(self.concat, 1, (0, 0, 0))
			self.screen.surface.blit(label, (self.x+10, self.y+10))
		else:
			label = self.screen.font.render(self.text, 1, (0, 0, 0))
			self.screen.surface.blit(label, (self.x+10, self.y+10))
			#label = self.screen.font.render(self.text2, 1, (0, 0, 0))
			#self.screen.surface.blit(label, (self.x+10, self.y+30))
		
	def show(self, text):
		self.text = text
		self.screen.state = "textbox"