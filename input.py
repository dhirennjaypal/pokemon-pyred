import pygame
from dialog import Dialog

TOUCHSCREEN = True

class Input_Handler:

	def __init__(self, game):
		self.game = game
		self.screen = game.screen
		self.map = game.map
		self.hero = game.hero
		self.gamepad = game.gamepad
		self.keydown = False
		self.hero_walking = False
		self.hero_autorun = False
		self.holdtime = 0
		self.delay = 5

	def main(self):
		touched = []
		#touchscreen
		if TOUCHSCREEN:
			touched = self.gamepad.get_touched(self.screen.surface)
		#new_way
		if not TOUCHSCREEN and pygame.mouse.get_pressed()[0]:
			touched.append(self.gamepad.get_pressed())

		if touched:

			if self.screen.state["fade"]:
				pass

			elif self.screen.state["menu"]:
				if "B" in touched:
					if not self.keydown:
						self.screen.state["menu"] = False
						self.keydown = True
				elif "A" in touched:
					if not self.keydown:
						self.screen.menu.select()
						self.keydown = True
				elif "Up" in touched:
					if not self.keydown:
						self.screen.menu.prev()
						self.keydown = True	
				elif "Down" in touched:
					if not self.keydown:
						self.screen.menu.next()
						self.keydown = True
			#end menu

			#state dialog
			elif self.screen.state["dialog"]:
				for key in ("A", "B", "Up", "Down"):
					if key in touched:
						if not self.keydown:
							selected = self.screen.dialogbox.inputButton(key)
							self.keydown = True
							if (not self.screen.dialogbox.busy) and "A" in touched:
								self.screen.state["dialog"] = False
								self.keydown = True
								self.game.scriptengine.input(key)
								self.game.scriptengine.update(selected)
								self.game.scriptengine.next()
			#end menu
			
			#start mainmenu
			elif self.screen.state["mainmenu"]:
				for key in ("Up", "Down"):
					if key in touched:
						if not self.keydown:
							self.screen.mainmenu.giveInput(key)
							self.keydown = True
				if "A" in touched:
					data = self.screen.mainmenu.giveInput("A")
					self.game.load(data)
			#end mainmenu

			#for map state
			
			#touchscreen
			elif self.screen.state["map"]:
				if touched and not self.hero.walking:
					self.holdtime += 1
				if not self.hero.walking:
					if "B" in touched:
						self.hero.running = not self.hero_autorun
					else:
						self.hero.running = self.hero_autorun
				if self.hero.dir in touched and not self.hero_walking:# and not self.keydown:
					self.hero_walking = True
				for key in touched:
					if key in ("Up", "Down", "Left", "Right") and not self.hero.walking:
						self.hero.change_dir(key)
						self.keydown = True
				if (self.holdtime % self.delay == 0 and not self.hero.walking) or self.hero_walking:
					if "Up" in touched:
						self.hero.move(0, -1)
						self.hero_walking = True
					elif "Down" in touched:
						self.hero.move(0, 1)
						self.hero_walking = True
					elif "Left" in touched:
						self.hero.move(-1, 0)
						self.hero_walking = True
					elif "Right" in touched:
						self.hero.move(1, 0)
						self.hero_walking = True
					else:
						self.hero_walking = False
				if "L" in touched:
					if not self.hero_autorun:
						dialogbox = Dialog( "Autorun Enabled", self.screen.surface)
						self.screen.drawDialog(dialogbox)
						#self.screen.state["dialog"] = True
						self.hero_autorun = True
					else:
						dialogbox = Dialog( "Autorun Disabled", self.screen.surface)
						self.screen.drawDialog(dialogbox)
						#self.screen.state["dialog"] = True
						self.hero_autorun = False
					self.hero.running = self.hero_autorun
				if "X" in touched:
					self.screen.state["menu"] = True
				if "A" in touched and not self.keydown:
						self.map.interact()
						self.keydown = True
				#self.hero_walking = self.hero.walking			
			#
			#touchscreen end
			#
			#end map state

		else:
		#if not touched:
			self.holdtime = 0
			self.keydown = False
			self.hero_walking = False
"""
		elif not TOUCHSCREEN:
			self.holdtime = 0
			self.keydown = False
			self.hero_walking = False
"""