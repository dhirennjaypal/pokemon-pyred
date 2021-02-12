import pygame
from pytmx.util_pygame import load_pygame
import pyscroll
from pyscroll.group import PyscrollGroup
from dialog import Dialog
from foreground import FadeOutAndIn, FadeOut, FadeIn
#from npc import NPC

class Map:

	def __init__(self, game):
		self.game = game
		self.screen = game.screen
		self.datahelper = game.datahelper
		self.hero = game.hero
		self.scriptengine = game.scriptengine
		self.hero.map = self

	def load(self, data):
		#loading map to creating group
		tmx_data = load_pygame(self.datahelper.maps[data["mapname"]]["file"])
		map_data = pyscroll.data.TiledMapData(tmx_data)
		self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.surface.get_size(), clamp_camera=False) #tall_sprites=1)
		self.map_layer.zoom = 2
		self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=5)#data["layer"])
		#setting up player
		self.mapname = data["mapname"]
		self.hero.position = [data["player"]["x"], data["player"]["y"]-8]
		if data["player"]["walking"] == 1:
			self.hero.walking = True
			self.hero.movingx, self.hero.movingy = data["player"]["walkingx"], data["player"]["walkingy"]
			self.hero.steps = 16
		self.group.add(self.hero)
		self.hero.rect.topleft = self.hero.position

		#colliditon
		self.collidable = {}
		self.interactable = {}
		self.warps = {}
		self.npcs = {}
		i = j = k = l = 0
		for id in tmx_data.objects_by_id:
			#print(tmx_data.objects_by_id[id].name)
			if tmx_data.objects_by_id[id].name in self.datahelper.interactable:
				self.interactable[j] = tmx_data.objects_by_id[id]
				j += 1
			if tmx_data.objects_by_id[id].name in self.datahelper.collidable:
				self.collidable[i] = (tmx_data.objects_by_id[id].x, tmx_data.objects_by_id[id].y)
				i += 1
			if "Warp" in tmx_data.objects_by_id[id].name:
				self.warps[k] = tmx_data.objects_by_id[id]
				k += 1
			if "npc" in tmx_data.objects_by_id[id].name:
				self.npcs[l] = self.scriptengine.load_npc(tmx_data.objects_by_id[id])
				#self.npcs[l] = NPC(tmx_data.objects_by_id[id].name)
				#self.npcs[l].position = [tmx_data.objects_by_id[id].x, tmx_data.objects_by_id[id].y-8] 
				self.group.add(self.npcs[l])
				self.npcs[l].map = self
				#self.npcs[l].rect.topleft = self.npcs[l].position
				#if "dir" in tmx_data.objects_by_id[id].properties.keys():
					#self.npcs[l].dir = tmx_data.objects_by_id[id].properties["dir"]
					#self.scriptengine.load(self.npcs[l])
					#self.npcs[l].map = self
				l += 1
		#animations
		#print(self.warps)
		self.timer = 0
		self.warping = False
		self.nextmap = {}
		#self.autorun = False
		#tempfade
		#self.fade = FadeOut(self.screen.surface, 10)
		#self.fade = FadeIn(self.screen.surface, 30)
		#self.fade = FadeOut(self.screen.surface, 30)
		#self.loaded = False

	def draw(self, screen):
		self.group.update()
		self.hero.tick()
		self.group.center(self.hero.rect.topleft)
		#self.group.draw(screen)
		#if self.loaded:
		self.group.draw(screen)

	def change_map(self, data):
		#self.screen.drawFade()
		#temp = self.autorun
		#temp fade
		#self.fade = FadeOut(self.screen.surface, 30)
		self.warps = 0
		self.scriptengine.clear()
		#self.group.remove(self.hero)
		#if self.fade.halftime<self.fade.count:
		self.load(data)
		#if self.screen != None:
		#self.autorun = temp

	def update(self):
		for key, warp in self.warps.items():
			if self.hero.rect.collidepoint(warp.x, warp.y):
				if not self.screen.state["fade"]:
					self.screen.drawFade()
				if self.screen.fadein:
					self.change_map(self.datahelper.warps[warp.name])

	def collide(self, rect, npc=False):
		for i in self.collidable:
			if rect.collidepoint(self.collidable[i]):
				return True
		for i in self.npcs:
			if self.npcs[i].walking:
				if rect.colliderect(self.npcs[i].facing):
					return True
			else:
				if rect.collidepoint(self.npcs[i].position[0], self.npcs[i].position[1]+8):
					return True
		if npc and rect.collidepoint(self.hero.position[0], self.hero.position[1]+8):
			return True
		return False

	def interact(self):
		#print(self.interactable)
		for i in self.interactable:
			if self.hero.facing.collidepoint(self.interactable[i].x, self.interactable[i].y):
				dialogbox = Dialog(self.datahelper.interactable[self.interactable[i].name], self.screen.surface)
				self.screen.drawDialog(dialogbox)
		for i in self.npcs:
			if not self.npcs[i].walking:
				if self.hero.facing.collidepoint(self.npcs[i].rect.x, self.npcs[i].rect.y+8):
					self.scriptengine.run(self.npcs[i])