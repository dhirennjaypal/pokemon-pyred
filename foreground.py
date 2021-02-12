import pygame

class ForegroundObject():

	def __init__(self):
		self.busy = False

	def inputButton(self, button):
		pass

	def draw(self):
		pass

	def tick(self):
		pass

class FadeOutAndIn(ForegroundObject):

	def __init__(self, screen, time):
		self.screen = screen
		self.halftime = time/2
		self.surface = pygame.Surface((self.screen.get_width(),self.screen.get_height()))
		self.surface.fill((0,0,0))
		self.surface.set_alpha(0)
		self.count = 0
		self.busy = True

	def draw(self):
		self.screen.blit(self.surface, (0,0))
	
	def tick(self):
		self.count += 1
		if self.count <= self.halftime:
			self.surface.set_alpha(int((self.count*255)/self.halftime))
		elif self.count <= self.halftime*2:
			self.surface.set_alpha(int(255-(((self.count-self.halftime)*255)/self.halftime)))
		if self.count >= self.halftime*2:
			self.busy = False

class FadeOut(ForegroundObject):

	def __init__(self, screen, time):
		self.screen = screen
		self.time = time
		self.surface = pygame.Surface((self.screen.get_width(),self.screen.get_height()))
		self.surface.fill((0,0,0))
		self.surface.set_alpha(0)
		self.count = 0
		self.busy = True

	def draw(self):
		self.screen.blit(self.surface, (0,0))
	
	def tick(self):
		self.count += 1
		self.surface.set_alpha(int((self.count*255)/self.time))
		if self.count >= self.time:
			self.busy = False

class FadeIn(ForegroundObject):

	def __init__(self, screen, time):
		self.screen = screen
		self.time = time
		self.surface = pygame.Surface((self.screen.get_width(),self.screen.get_height()))
		self.surface.fill((0,0,0))
		self.surface.set_alpha(0)
		self.count = 0
		self.busy = True

	def draw(self):
		self.screen.blit(self.surface, (0,0))
	
	def tick(self):
		self.count += 1
		self.surface.set_alpha(int(255-(self.count*255)/self.time))
		if self.count >= self.time:
			self.busy = False