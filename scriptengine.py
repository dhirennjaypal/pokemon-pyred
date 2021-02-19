import json
from dialog import Dialog, ChoiceDialog
from npc import NPC
#temp
import savegame

class ScriptEngine:
	
	def __init__(self, game):
		self.game = game
		self.running = False
		self.busy = False
		self.npcs = {}
		self.scripts = {}
		self.movements = {}
		self.current_move = {}
		self.flags = {}
		self.current_npc = None #temp
		self.current_script = 0 #temp
		self.timer = 0
		self.delay = {}
		self.ready = {}
	
	def load_npc(self, object):
		with open("data/npc/"+object.name+".json", "r") as file:
			data = json.load(file)
		self.npcs[data["name"]] = NPC(data["image"], data["name"])
		self.npcs[data["name"]].dir = data["dir"]
		self.npcs[data["name"]].position = [object.x, object.y-8]
		self.npcs[data["name"]].rect.topleft = self.npcs[data["name"]].position
		self.scripts[data["name"]] = data["scripts"]
		
		if "flags" in data:
			self.flags[data["name"]] = {}
			for i in data["flags"]:
				self.flags[data["name"]][i] = False
			#print(self.flags[data["name"]])	
		
		if "movements" in data:
			#self.moving = True
			self.delay[data["name"]] = data["delay"]
			self.movements[data["name"]] = data["movements"]
			self.current_move[data["name"]] = 0
			#self.waking[data["name"]] = False
		return self.npcs[data["name"]] #to map, so it can be added to group
	
	def tick(self):
		for npc in self.npcs:
			self.npcs[npc].tick()
		if self.running and not self.busy:
			self.busy = True
			if self.scripts[self.current_npc][self.current_script]["type"] == "dialog":
				if "conditions" in self.scripts[self.current_npc][self.current_script]:
					for condition in self.scripts[self.current_npc][self.current_script]["conditions"]:
						#print(condition)
						if not self.flags[self.current_npc][condition]:
							self.busy = False
							self.next()
							return
				#print(self.scripts[self.current_npc][self.current_script])
				cursor = False
				if self.scripts[self.current_npc][self.current_script]["cursor"] == 1:
					cursor = True
				dialogbox = Dialog("@"+self.current_npc+"@: #"+self.scripts[self.current_npc][self.current_script]["text"]+"#", self.game.screen.surface, cursor)
				self.game.screen.drawDialog(dialogbox)
			elif self.scripts[self.current_npc][self.current_script]["type"] == "choicedialog":
				cursor = False
				if self.scripts[self.current_npc][self.current_script]["cursor"] == 1:
					cursor = True
				choices = self.scripts[self.current_npc][self.current_script]["choices"]
				#print(self.scripts[self.current_npc][self.current_script]["choices"].keys())
				#for choice in self.scripts[self.current_npc][self.current_script]["choices"].keys():
					#choices.append(choice)
				#print(choices)
				dialogbox = ChoiceDialog("@"+self.current_npc+"@: #"+self.scripts[self.current_npc][self.current_script]["text"]+"#", self.game.screen.surface, choices, cursor)
				self.game.screen.drawDialog(dialogbox)
			elif self.scripts[self.current_npc][self.current_script]["type"] == "changedir":
				if self.scripts[self.current_npc][self.current_script]["dir"] == "player":
					if self.game.hero.dir == "Up":
						npcdir = "Down"
					elif self.game.hero.dir == "Down":
						npcdir = "Up"
					elif self.game.hero.dir == "Left":
						npcdir = "Right"
					elif self.game.hero.dir == "Right":
						npcdir = "Left"
					self.npcs[self.current_npc].change_dir(npcdir)
				else:
					self.npcs[self.current_npc].change_dir(self.scripts[self.current_npc][self.current_script]["dir"])
#				self.idle = True
				self.busy = False
		
		#movements
		for npc in self.movements:
			if (not self.npcs[npc].walking) and (not self.busy):
				move = self.movements[npc][self.current_move[npc]]
				if self.timer % self.delay[npc] == 0:
					self.npcs[npc].change_dir(move)
					if move == "Up":
						self.npcs[npc].move(0, -1)
					elif move == "Down":
						self.npcs[npc].move(0, 1)
					elif move == "Left":
						self.npcs[npc].move(-1, 0)
					elif move == "Right":
						self.npcs[npc].move(1, 0)
					self.ready[npc] = self.npcs[npc].walking
					
		self.next()

	def input(self, button):
		if button == "A":
			self.busy = False
	
	def next(self):
		self.timer += 1
		if self.running and not self.busy:
			if self.current_script == len(self.scripts[self.current_npc])-1:
#			self.current_script = 0
#			self.scripts = {}
#			self.npc = None
				if len(self.flags) != 0:
					if self.current_npc in self.flags:
						for flag in self.flags[self.current_npc]:
							self.flags[self.current_npc][flag] = False
				self.running = False
				return
#		elif len(self.scripts) == 0:
#			return
#		elif self.idle:
			self.current_script += 1
#			#self.idle = True
		for npc in self.movements:
			if self.npcs[npc].walking and self.ready[npc]:
				self.ready[npc] = False
				self.current_move[npc] += 1
				if self.current_move[npc] == len(self.movements[npc]):
					self.current_move[npc] = 0
		
	def run(self, npc):
		if (not len(self.scripts) == 0) and (not self.busy):
			self.current_npc = npc.name
			self.current_script = 0
			#self.busy = True
			self.running = True
			#self.running = True
	
	def clear(self):
		self.npcs = {}
		self.scripts = {}
		self.movements = {}
		self.current_move = {}
		self.delay = {}
		self.ready = {}
		self.flags = {}
		self.running = False
		self.busy = False
		self.timer = 0
	
	def update(self, value):
		#temp start
		if value == "savegame":
			savegame.save(self.game)
			dialogbox = Dialog( "Game saved.", self.game.screen.surface)
			self.game.screen.drawDialog(dialogbox)
		#temp end
		#pass
		#print(value)
		if len(self.flags) != 0:
			print(self.flags)
			if self.current_npc in self.flags:
				for flag in self.flags[self.current_npc]:
					if value == flag:
						self.flags[self.current_npc][flag] = True
						#print(self.flags)
						#print("value "+value)
						#print("flag "+flag)
						