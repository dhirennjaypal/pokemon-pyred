import json

class Data_Helper:
	
	def __init__(self):
		with open("data/collidable.json", "r") as file:
			self.collidable = json.load(file)["Collidable"]
		with open("data/interactable.json", "r") as file:
			self.interactable = json.load(file)
		with open("data/warps.json") as file:
			self.warps = json.load(file)
		with open("data/maps.json") as file:
			self.maps = json.load(file)

#end