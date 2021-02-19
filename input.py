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
		self.holdtime = 0
		self.delay = 5

	def main(self):
		#touchscreen
		touched = self.gamepad.get_touched(self.screen.surface)
		#new_way
		if pygame.mouse.get_pressed()[0]:
			pressed = self.gamepad.get_pressed()

			#for menu
			if self.screen.state["fade"]:
				pass
			elif self.screen.state["menu"]:
				if pressed == "B":
					if not self.keydown:
						self.screen.state["menu"] = False
						self.keydown = True
				elif pressed == "A":
					if not self.keydown:
						self.screen.menu.select()
						self.keydown = True
				elif pressed == "Up":
					if not self.keydown:
						self.screen.menu.prev()
						self.keydown = True	
				elif pressed == "Down":
					if not self.keydown:
						self.screen.menu.next()
						self.keydown = True
			#end menu

			#state dialog
			elif self.screen.state["dialog"]:
				if pressed in ("A", "B", "Up", "Down"):
					if not self.keydown:
						selected = self.screen.dialogbox.inputButton(pressed)
						self.keydown = True
						if (not self.screen.dialogbox.busy) and pressed == "A":
							self.screen.state["dialog"] = False
							self.keydown = True
							self.game.scriptengine.input(pressed)
							self.game.scriptengine.update(selected)
							self.game.scriptengine.next()
			#end menu
			
			#start mainmenu
			elif self.screen.state["mainmenu"]:
				if pressed in ("Up", "Down"):
					if not self.keydown:
						self.screen.mainmenu.giveInput(pressed)
						self.keydown = True
				elif pressed == "A":
					data = self.screen.mainmenu.giveInput(pressed)
					self.game.load(data)
			#end mainmenu

			#for map state
			
			#touchscreen
			elif self.screen.state["map"] and TOUCHSCREEN and touched:
				if touched and not self.hero.walking:
					self.holdtime += 1
				if "B" in touched:
					if not self.hero.walking:
						self.hero.running = True
				else:
					self.hero.running = False
				if self.hero.dir in touched and not self.hero_walking:# and not self.keydown:
					self.hero_walking = True
				for key in touched:
					if key in ("Up", "Down", "Left", "Right"):
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

				if "X" in touched:
					self.screen.state["menu"] = True			
			#
			#touchscreen end
			#
			#
				
				
			elif self.screen.state["map"] and not TOUCHSCREEN:
				if pressed != "None" and not self.hero.walking:
					self.holdtime += 1
				if (self.hero.dir == pressed and not self.hero_walking) and not self.keydown:
					self.hero_walking = True
				if pressed in ("Up", "Down", "Left", "Right"):
					self.hero.change_dir(pressed)
					self.keydown = True
				if (self.holdtime % self.delay == 0 and not self.hero.walking) or self.hero_walking:# if (self.hero.dir == pressed and not self.hero_walking):
					if pressed == "Up":
						self.hero.move(0, -1)
						self.hero_walking = True
					elif pressed == "Down":
						self.hero.move(0, 1)
						self.hero_walking = True
					elif pressed == "Left":
						self.hero.move(-1, 0)
						self.hero_walking = True
					elif pressed == "Right":
						self.hero.move(1, 0)
						self.hero_walking = True
				if pressed == "A":
					if not self.keydown:
						self.map.interact()
						self.keydown = True
				elif pressed == "X":
					self.screen.state["menu"] = True
				elif pressed == "L":
					if self.delay == 20:
						dialogbox = Dialog( "Autorun Enabled", self.screen.surface)
						self.screen.drawDialog(dialogbox)
						#self.screen.state["dialog"] = True
						self.delay = 5
						self.hero.running = True
					else:
						dialogbox = Dialog( "Autorun Disabled", self.screen.surface)
						self.screen.drawDialog(dialogbox)
						#self.screen.state["dialog"] = True
						self.delay = 20
						self.hero.running = False
					#self.textbox.draw()
			#end map state

		if TOUCHSCREEN and not touched:
				self.holdtime = 0
				self.keydown = False
				self.hero_walking = False

		elif not TOUCHSCREEN:
			self.holdtime = 0
			self.keydown = False
			self.hero_walking = False