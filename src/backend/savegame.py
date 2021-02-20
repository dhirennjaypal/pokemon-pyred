import json

def save(game):
	data = {}
	data["mapname"] = game.map.mapname
	data["player"] = {
		"x" : game.hero.position[0], "y" : game.hero.position[1]+8,
		"dir" : game.hero.dir, "map" : game.map.mapname, "walking" : 0
	}
	with open("data/savegame.json", "w") as fp:
		json.dump(data, fp)

def load():
	try:
		with open("data/savegame.json", "r") as fp:
			data = json.load(fp)
	except IOError:
		data = None
	return data