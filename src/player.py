import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		
		#animations
		self.images = {}

		self.images["walking"] = {}
		self.images["walking"]["Down"] = {}
		self.images["walking"]["Left"] = {}
		self.images["walking"]["Right"] = {}
		self.images["walking"]["Up"] = {}
		
		self.images["running"] = {}
		self.images["running"]["Down"] = {}
		self.images["running"]["Left"] = {}
		self.images["running"]["Right"] = {}
		self.images["running"]["Up"] = {}

		#loading surfaces
		tileset = pygame.image.load("sprites/boy.png").convert_alpha()
		tilew, tileh = tileset.get_width()/4, tileset.get_height()/4
		j = 0
		for dir in self.images["walking"]:
			for i in range (1, 5):
				temprect = pygame.Rect((tilew*(i-1), tileh*j), (tilew, tileh))
				tempsurf = pygame.Surface((tilew, tileh)).convert_alpha()
				tempsurf.set_colorkey((255, 0, 255))
				tempsurf.fill((255, 0, 255))
				tempsurf.blit(tileset, (0, 0), temprect)
				self.images["walking"][dir][i] = pygame.transform.scale(tempsurf, (16, 24))
				self.images["walking"][dir][i].set_colorkey((255, 0, 255))
			j += 1
		
		tileset = pygame.image.load("sprites/boy_run.png").convert_alpha()	
		j = 0
		for dir in self.images["running"]:
			for i in range (1, 5):
				temprect = pygame.Rect((tilew*(i-1), tileh*j), (tilew, tileh))
				tempsurf = pygame.Surface((tilew, tileh)).convert_alpha()
				tempsurf.set_colorkey((255, 0, 255))
				tempsurf.fill((255, 0, 255))
				tempsurf.blit(tileset, (0, 0), temprect)
				self.images["running"][dir][i] = pygame.transform.scale(tempsurf, (16, 24))
				self.images["running"][dir][i].set_colorkey((255, 0, 255))
			j += 1

		self.dir = "Down"
		self.frame = 1
		self.image = self.images["walking"][self.dir][self.frame]
		#normal
		self._position = [0, 0]
		self.rect = self.image.get_rect()
		self.position = [self.position[0], self.position[1]]
		self.walking = False
		self.running = False
		self.collide = False
		self.steps = 0
		self.walkingx, self.walkingy = 0, 0
		#interaction
		self.facing = self.rect.copy()
		self.map = None

	@property
	def position(self):
		return list(self._position)
		
	@position.setter
	def position(self, value):
		self._position = list(value)

	def change_dir(self, dir):
		if dir != self.dir and not self.walking:
			self.dir = dir
#			if self.running and self.walking:
#				self.image = self.images["running"][self.dir][self.frame]
#			else:
#				self.image = self.images["walking"][self.dir][1]
			self.update()

	def move(self, x, y):
		#self.position = [self.position[0] + x, self.position[1] + y]
		self.collide = self.map.collide(self.facing)
		if (not self.walking) and (not self.collide):
			self.movingx, self.movingy = x, y
			self.walking = True
			self.steps = 16
		#self.rect.topleft = self.position

	def update(self):
		#interection
		self.facing = self.rect.copy()
		if self.dir == "Up":
			self.facing.y -= 16
		elif self.dir == "Down":
			self.facing.y += 16
		elif self.dir == "Left":
			self.facing.x -= 16
		elif self.dir == "Right":
			self.facing.x += 16
		if self.running and self.walking:
			self.image = self.images["running"][self.dir][self.frame]
		else:
			self.image = self.images["walking"][self.dir][self.frame]
		#self.map.update()
		
	def tick(self):
		#self.update()
		if self.steps == 0:
			self.walking = False
			self.map.update()
		if self.walking:
			if self.running:
				self.position = [self.position[0] + self.movingx*2, self.position[1] + self.movingy*2]
				self.steps -= 2
			else:
				self.position = [self.position[0] + self.movingx, self.position[1] + self.movingy]
				self.steps -= 1
			self.rect.topleft = self.position
			if self.steps % 8 == 0:
				if self.frame == 4:
					self.frame = 1
				else:
					self.frame += 1		