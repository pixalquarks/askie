import pymongo

class ServerDB():

	def __init__(self):
		self.url = "mongodb://pixal_sama:WG9NQX2vtDd3PrEs@cluster0-shard-00-00.hy7pp.mongodb.net:27017,cluster0-shard-00-01.hy7pp.mongodb.net:27017,cluster0-shard-00-02.hy7pp.mongodb.net:27017/server_player_db?ssl=true&replicaSet=atlas-758ine-shard-0&authSource=admin&retryWrites=true&w=majority"
		self.client = pymongo.MongoClient(self.url)
		self.db = self.client.server_player_db
		print("SERVER DB CONNECTED")
	def insert_server(self,data:dict):
		self.db.test_server_list.insert_one(data)
	def isServer(self,id:int):
		data = self.db.test_server_list.find_one({"_id":id})
		return bool(data)
	def insert_player(self,data:dict):
		self.db.test_player_list.insert_one(data)
	def isPlayer(self,id:int):
		data = self.db.test_player_list.find_one({"_id":id})
		return bool(data)
	def insert_waifu(self,player_id:int,waifustats:dict):
		name = waifustats["name"]
		data = self.db.test_player_list.find_one({"_id":player_id})
		if name not in data["waifu_list"].keys():
			nn = "waifu_list." + name
			self.db.test_player_list.update_one({"_id":player_id},{"$set" : {nn: waifustats},"$inc":{"waifu_count."+waifustats["data"]["status"]:1}})
			return "added {} to your harem".format(name)
		else:
			nn = "waifu_list." + name + ".data.level"
			self.db.test_player_list.update_one({"_id":player_id},{"$inc":{nn:1}})
			return "Your waifu {} has leveled up to level {}".format(name,data["waifu_list"][name]["data"]["level"])
	def get_waifus(self,player_id:int):
		data = self.db.test_player_list.find_one({"_id":player_id})
		return data["waifu_list"]
	def dec_Count(self,player_id:int,status:str):
		data = self.db.test_player_list.find_one({"_id":player_id},{"waifu_draws":1})
		if data['waifu_draws'][status] > 0:
			self.db.test_player_list.update_one({"_id":player_id},{"$inc":{"waifu_draws."+status: -1}})
			return None
		else:
			return "You are out of draws. Draws refresh everyday"
	def getPlayerData(self,player_id:int):
		data = self.db.test_player_list.find_one({"_id":player_id})
		return data

if __name__ == "__main__":
	db = ServerDB()
	#waifustats = {"name": "Asuna Yuuki","data": {"id":5,"level":1,"status":"legendary"}}
	#db.insert_waifu(436046584678187008,waifustats)
	#m = db.dec_Count(436046584678187008,"legendary")
	db.getPlayerData(436046584678187008)