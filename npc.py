import pygame

class NPC(pygame.sprite.Sprite):
	def __init__(self, image="npc_mom", name="mom"):
		pygame.sprite.Sprite.__init__(self)
		
		self.name = name
		#animations
		self.images = {}

		self.images["Down"] = {}
		self.images["Left"] = {}
		self.images["Right"] = {}
		self.images["Up"] = {}

		#loading surfaces
		tileset = pygame.image.load("sprites/"+image+".png").convert_alpha()
		tilew, tileh = tileset.get_width()/4, tileset.get_height()/4
		j = 0
		for dir in self.images:
			for i in range (1, 5):
				temprect = pygame.Rect((tilew*(i-1), tileh*j), (tilew, tileh))
				tempsurf = pygame.Surface((tilew, tileh)).convert_alpha()
				tempsurf.set_colorkey((255, 0, 255))
				tempsurf.fill((255, 0, 255))
				tempsurf.blit(tileset, (0, 0), temprect)
				self.images[dir][i] = pygame.transform.scale(tempsurf, (16, 24))
				self.images[dir][i].set_colorkey((255, 0, 255))
			j += 1

		self.dir = "Down"
		self.frame = 1
		self.image = self.images[self.dir][self.frame]
		#normal
		self._position = [0, 0]
		self.rect = self.image.get_rect()
		self.position = [self.position[0], self.position[1]]
		self.walking = False
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
		if dir != self.dir:#and not self.walking:
			self.dir = dir
			self.image = self.images[self.dir][1]
		self.update()

	def move(self, x, y):
		#self.position = [self.position[0] + x, self.position[1] + y]
		self.collide = self.map.collide(self.facing, True)
		if (not self.walking) and (not self.collide):
			self.movingx, self.movingy = x, y
			self.walking = True
			self.steps = 16
			#self.facing.x += x*16
			#self.facing.y += y*16
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
		self.image = self.images[self.dir][self.frame]
		#self.map.update()
		
	def tick(self):
		#self.update()
		if self.steps == 0:
			self.walking = False
			#self.map.update()
		if self.walking:
			self.position = [self.position[0] + self.movingx, self.position[1] + self.movingy]
			self.steps -= 1
			self.rect.topleft = self.position
			if self.steps % 8 == 0:
				if self.frame == 4:
					self.frame = 1
				else:
					self.frame += 1