import pymongo
import random



class Database():

	def __init__(self):
		self.url = "mongodb://pixal_sama:WG9NQX2vtDd3PrEs@cluster0-shard-00-00.hy7pp.mongodb.net:27017,cluster0-shard-00-01.hy7pp.mongodb.net:27017,cluster0-shard-00-02.hy7pp.mongodb.net:27017/waifu_db?ssl=true&replicaSet=atlas-758ine-shard-0&authSource=admin&retryWrites=true&w=majority"
		self.client = pymongo.MongoClient(self.url)
		self.rank_tup = ("legendary","superrare","special","common")
		print("DATABASE CONNECTED")
	def find_waifu(self,name:str):
		data = self.client.waifu_db.waifuList.find({"waifu.name":{"$regex":name}},{"waifu.name" : 1, "_id": 1})
		return data
	def waifu_status(self,status:str):
		rank = None
		print("Inside the data base")
		while True:
			try:
				if status == self.rank_tup[0]:
					rank = random.randint(1,32)
					print(rank)
				elif status == self.rank_tup[1]:
					rank = random.randint(32,120)
				elif status == self.rank_tup[2]:
					rank = random.randint(120,500)
				elif status == self.rank_tup[3]:
					rank = random.randint(500,4000)
				data = self.client.waifu_db.waifuList.find_one({"waifu.popularity_rank":rank})
				return data
			except:
				pass
	def find_waifu_by_id(self,id:int):
		data = self.client.waifu_db.waifuList.find_one({"_id" : id})
		return data
	def get_waifu_by_rank(self,rank:int):
		data = self.client.waifu_db.waifuList.find_one({"waifu.popularity_rank":rank})
		return data
	def get_imouto(self):
		data = self.client.waifu_db.waifuList.find({"$and" : [{"waifu.age":{"$lte":14}},{"waifu.age":{"$gte":8}}]})
		ln = list(data)
		return random.choice(ln)
	def get_busty(self,nsfw=False):
		data = self.client.waifu_db.waifuList.find({"$and": [{"waifu.bust":{"$gte":85}},{"waifu.hip":{"$gte":90}},{"waifu.nsfw":nsfw}]})
		ln = list(data)
		return random.choice(ln)
	def get_milf(self,nsfw=False):
		data = self.client.waifu_db.waifuList.find({"$and": [{"waifu.bust":{"$gte":85}},{"waifu.hip":{"$gte":90}},{"waifu.age":{"$gte":23}},{"waifu.nsfw":nsfw}]})
		return random.choice(list(data))
	def nsfw(self):
		data = self.client.waifu_db.waifuList.find({"waifu.nsfw":True})
		return random.choice(list(data))


if __name__ == "__main__":
	db = Database()
	data = db.find_waifu("Kurumi")
	data = list(data)
	print(data)