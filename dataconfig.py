import ServerDB

db = ServerDB.ServerDB()



def checkServer(ctx):
	if db.isServer(ctx.guild.id):
		return "This guild is already added"
	data_dict = {"name" : ctx.guild.name,
				"_id"    : ctx.guild.id,
				"owner_name" : ctx.guild.owner.name,
				"owner_id"   : ctx.guild.owner_id,
				"channels"   : [{"channel_name": i.name,"channel_id": i.id} for i in ctx.guild.channels],
				"members"    : [{"member_name": i.name,"member_id":i.id} for i in ctx.guild.members],
				"waifu_channel": None,
				"doujin_channel": None
	}
	mods = []
	for member in ctx.guild.members:
		for role in member.roles:
			if role.name == "Mods":
				mods.append({"mod_name":member.name,"mod_id":member.id})
				continue
	data_dict["Mods"] = mods
	db.insert_server(data_dict)
	return "Added Server"

# def configChannel(ctx,):

# def setChannel(ctx,channel_name:str):


def addPlayer(ctx,nick:str):
	if db.isPlayer(ctx.author.id):
		return "player already added"
	data_dict = {"name": ctx.author.name,
				"_id"  : ctx.author.id,
				"nickname": nick,
				"waifu_list": {},
				"waifu_count":	{"legendary": 0,
								"superrare": 0,
								"special": 0,
								"common" : 0},
				"max_level_count": {"legendary": 0,
								"superrare": 0,
								"special": 1,
								"common" : 3},
				"waifu_draws": {"legendary" : 3,
								"superrare" : 8,
								"special" : 20,
								"common" : 50},
				"level" : 1,
				"level_name" : "Peasent Level 1",
				"exp" : 0,
				"charisma" : 0,
				"reputation" : 0,
				"balance" : 0
				}
	db.insert_player(data_dict)
	return "Player Assigned"

def addWaifu(ctx,waifu_stats:dict):
	if not db.isPlayer(ctx.author.id):
		return "Seems like you are not yet added to the game. Try adding yourself to the game using $addme <nickname>"
	message = db.insert_waifu(ctx.author.id,waifu_stats)
	return message

def listWaifus(id:int):
	if not db.isPlayer(id):
		return "Seems like you are not yet added to the game. Try adding yourself to the game using $addme <nickname>"
	data = db.get_waifus(id)
	str_list = []
	id_list = []
	for key in data.keys():
		message = "Name:{} level: {} status {}".format(data[key]["name"],data[key]["data"]["level"],data[key]["data"]["status"])
		id_list.append(data[key]["data"]["id"])
		str_list.append(message)
	final_message = "\n".join(str_list)
	return final_message + "\n To show full details select waifu number", id_list

def showPlayer(id:int):
	if not db.isPlayer(id):
		return "Seems like you are not yet added to the game. Try adding yourself to the game using $addme <nickname>"
	data = db.getPlayerData(id)
	message = "Name : {}\nNickname : {}\nLevel : {}\nExp : {}\nCharisma : {}\nReputation : {}\nBalance : {}\nWaifu Count : legendary : {}\n\tSuper Rare : {}\n\tSpecial : {}\n\tCommon : {}".format(data["name"],data["nickname"],data["level_name"],data["exp"],data["charisma"],data["reputation"],data["balance"],data["waifu_count"]["legendary"],data["waifu_count"]["superrare"],data["waifu_count"]["special"],data["waifu_count"]["common"])
	return message

if __name__ == "__main__":
	msg = showPlayer(436046584678187008)
	print(msg)
	