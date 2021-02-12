import json

with open("npc.json") as fp:
	data = json.load(fp)

for i in range(0, len(data["npc_mom"])):
	print(data["npc_mom"][i])
	
LASTRESULT = 0
#print(data)

#what to do: