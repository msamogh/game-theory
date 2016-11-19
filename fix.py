from pymongo import MongoClient
scores = [110, 110, -40, -40, -30, 30, 20, 20]

client = MongoClient('localhost', 27017)

db = client.game_theory

groups = db.groups.find()

for i in groups:
	group_name = i['group_name']
	for m in i['members']:
		db.users.update_one({'username': str(m)}, {'$inc': {'score': scores[group_name - 1]}})

"""Group1 - 110
group2 - 110
group3 - -40
group4 - -40
group5 - -30
group6 - 30
group7 - 20
group8 - 20"""