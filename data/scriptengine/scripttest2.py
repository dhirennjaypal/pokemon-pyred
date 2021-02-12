import json

with open("script.json", "r") as file:
	data = json.load(file)

#print(data)
#print()

#temp_flags = {}
#for flag in data["npc1"]["temp_flags"]:
#	temp_flags[flag] = False

#print(temp_flags)
#print()
#temp_flags["text1"] = True

#do = True
#for script in data["npc1"]["scripts"]:
#	for condition in script["conditions"]:
#		if not temp_flags[condition]:
#			do = False
#			break
#	if do:
#		pass#print(script["text"])

#i = 0
#def script(npc):
#	global i
#	#print(npc["scripts"][i])
#	i += 1
	
#script(data["npc1"])
#script(data["npc1"])

#no temp flags in script
class ScriptEngine:

	def __init__(self, npc):
		flags = npc["temp_flags"]
		self.scripts = npc["scripts"]
		self.current = 0
		self.flags = {}
		self.running = True
		for flag in flags:
			self.flags[flag] = False
	
	def run(self):
		script = self.scripts[self.current]
		for c in script["conditions"]:
			if not self.flags[c]:
				return self.next()
		if script["type"] == "text":
			print("Dialog : "+script["text"])
		return self.next(["text1"])

	def next(self, flags=None):
		if flags != None:
			for flag in flags:
				self.flags[flag] = True
		self.current += 1
		if self.current > len(self.scripts)-1:
			self.running = False
			return self.running
		return self.running

engine = ScriptEngine(data["npc1"])
#print(engine.run())
#engine.next(["text1"])
#print(engine.run())
#print(engine.run())
#print(engine.run())

#engine.run()

#i think this was success

#now i need to make text based choice boxes to check