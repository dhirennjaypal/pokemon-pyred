import pygame

TOUCHSCREEN = True

class Controller:

	def __init__(self, screenw, screenh, buttonw, buttonh):
		self.rect = {}
		self.rect["dpad"] = {}
		self.rect["cpad"] = {}
		self.rect["trigger"] = {}
		#self.rect["dpad"]["Up"] = pygame.Rect(buttonw, screenh-buttonh*3, buttonw, buttonh)
		self.rect["dpad"]["Up"] = (buttonw, screenh-buttonh*3, buttonw, buttonh)
		self.rect["dpad"]["Down"] = pygame.Rect(buttonw, screenh-buttonh, buttonw, buttonh)
		self.rect["dpad"]["Left"] = pygame.Rect(0, screenh-buttonh*2, buttonw, buttonh)
		self.rect["dpad"]["Right"] = pygame.Rect(buttonw*2, screenh-buttonh*2, buttonw, buttonh)
		self.rect["cpad"]["X"] = pygame.Rect(screenw-buttonw*2, screenh-buttonh*3, buttonw, buttonh)
		self.rect["cpad"]["Y"] = pygame.Rect(screenw-buttonw*3, screenh-buttonh*2, buttonw, buttonh)
		self.rect["cpad"]["A"] = pygame.Rect(screenw-buttonw, screenh-buttonh*2, buttonw, buttonh)
		self.rect["cpad"]["B"] = pygame.Rect(screenw-buttonw*2, screenh-buttonh, buttonw, buttonh)
		self.rect["trigger"]["L"] = pygame.Rect(0, screenh-buttonh*4, buttonw*2.5, buttonh*0.5)
		self.rect["trigger"]["R"] = pygame.Rect(screenw-buttonw*2.5, screenh-buttonh*4, buttonw*2.5, buttonh*0.5)

		#new logic
		self.pyrect = {}
		self.pyrect["dpad"] = {}
		self.pyrect["cpad"] = {}
		self.pyrect["trigger"] = {}

		for set in self.rect:
			for button in self.rect[set]:
				self.pyrect[set][button] = pygame.Rect(self.rect[set][button])
		
		#touchscreen logic
		self.touchdown = False
		self.touches = []
		
		
	def draw(self, surface, color, font):
		#pressed = "None"
		touched = []
		if not TOUCHSCREEN and pygame.mouse.get_pressed()[0]:
			touched.append(self.get_pressed())
		if TOUCHSCREEN:
			touched = self.get_touched(surface)
		for set in self.rect:
			for button in self.rect[set]:
				surf = pygame.Surface(( self.rect[set][button][2], self.rect[set][button][3] ))
				pygame.draw.rect(surf, color, pygame.Rect(0, 0, self.rect[set][button][2], self.rect[set][button][3] ), border_radius=5)
				if touched and button in touched:
					surf.set_alpha(150)
				else:
					surf.set_alpha(50)
				surface.blit(surf, (self.rect[set][button][0], self.rect[set][button][1]))
				label = font.render(button, 1, color)
				x = self.rect[set][button][0] + self.rect[set][button][2]/2 - font.size(button)[0]/2
				y = self.rect[set][button][1] + self.rect[set][button][3]/2 - font.get_height()/2
				surface.blit(label, (x, y))
	
	def get_pressed(self):
		if pygame.mouse.get_pressed()[0]:
			pos = pygame.mouse.get_pos()
			for set in self.pyrect:
				for button in self.pyrect[set]:
					if self.pyrect[set][button].collidepoint(pos):
						return button
		return None
	
	def get_touched(self, surface):
		for event in pygame.event.get():
			if event.type == pygame.FINGERDOWN:
				self.touchdown = True
				self.touches.append(event)
				
			elif event.type == pygame.FINGERMOTION:
				for i in range(0, len(self.touches)):
					if self.touches[i].finger_id == event.finger_id:
						self.touches.pop(i)
						break
				#self.touchdown = True
				self.touches.append(event)

			elif event.type == pygame.FINGERUP:
				for i in range(0, len(self.touches)):
					if self.touches[i].finger_id == event.finger_id:
						self.touches.pop(i)
						break

				if not len(self.touches):
					self.touchdown = False

		if self.touchdown:
			touched = []

			for touch in self.touches:
				x = touch.x * surface.get_width()
				y = touch.y * surface.get_height()
			
				for set in self.pyrect:
					for button in self.pyrect[set]:
						if self.pyrect[set][button].collidepoint((x, y)):
							touched.append(button)
			return touched

		else:
			return None