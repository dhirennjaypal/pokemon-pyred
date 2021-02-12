import pygame

class Box(pygame.Surface):
	def __init__(self, size, fn=None):
		pygame.Surface.__init__(self, size)
		if fn == None:
			fn = "gfx/box.png"

		#tiles
		tile = pygame.image.load(fn).convert_alpha()
		tilesize = round(tile.get_width()/3), round(tile.get_height()/3)

		tileNW = pygame.Surface(tilesize)
		tileNW.blit(tile, (0, 0), pygame.Rect((0, 0), tilesize))
		tileNC = pygame.Surface(tilesize)
		tileNC.blit(tile, (0, 0), pygame.Rect((tilesize[0], 0), tilesize))
		tileNE = pygame.Surface(tilesize)
		tileNE.blit(tile, (0, 0), pygame.Rect((tilesize[0]*2, 0), tilesize))
		tileW = pygame.Surface(tilesize)
		tileW.blit(tile, (0, 0), pygame.Rect((0, tilesize[1]), tilesize))
		tileC = pygame.Surface(tilesize)
		tileC.blit(tile, (0, 0), pygame.Rect(tilesize, tilesize))
		tileE = pygame.Surface(tilesize)
		tileE.blit(tile, (0, 0), pygame.Rect((tilesize[0]*2, tilesize[1]), tilesize))
		tileSW = pygame.Surface(tilesize)
		tileSW.blit(tile, (0, 0), pygame.Rect((0, tilesize[1]*2), tilesize))
		tileSC = pygame.Surface(tilesize)
		tileSC.blit(tile, (0, 0), pygame.Rect((tilesize[0], tilesize[1]*2), tilesize))
		tileSE = pygame.Surface(tilesize)
		tileSE.blit(tile, (0, 0), pygame.Rect((tilesize[0]*2, tilesize[1]*2), tilesize))
		
		#dimentions
		middleSize = size[0]-(2*tilesize[0]), size[1]-(2*tilesize[1])
		dimensions = (middleSize[0]/tilesize[0])+1, (middleSize[1]/tilesize[1])+1
		origin = (size[0]-(dimensions[0]*tilesize[0]))/2, (size[1]-(dimensions[1]*tilesize[1]))/2
		
		#fill transparent
		self.fill((0,0,0))
		self.set_colorkey((0,0,0))
		
		#blit
		for x in range(0, round(dimensions[0])):
			for y in range(0, round(dimensions[1])):
				self.blit(tileC, (origin[0]+(x*tilesize[0]), origin[1]+(y*tilesize[1])))
				if x == 0:
					self.blit(tileW, (0, origin[1]+(y*tilesize[1])))
					self.blit(tileE, (size[0]-tilesize[0], origin[1]+(y*tilesize[1])))
			self.blit(tileNC, (origin[0]+(x*tilesize[0]), 0))
			self.blit(tileSC, (origin[0]+(x*tilesize[0]), size[1]-tilesize[1]))
		#cornerblit
		self.blit(tileNW, (0, 0))
		self.blit(tileNE, (size[0]-tilesize[0], 0))
		self.blit(tileSW, (0, size[1]-tilesize[1]))
		self.blit(tileSE, (size[0]-tilesize[0], size[1]-tilesize[1]))
