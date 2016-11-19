import math

def set_value(db, username, value):
	db.game2.update({'username': username}, {'$set': {'value': value}}, upsert=True)

def get_average(db):
	nums = []
	for i in db.game2.find():
		nums.append(i['value'])
	return 2/3 * sum(nums) / len(nums)

def calculate_scores(db):
	avg = get_average(db)
	for i in db.game2.find():
		value = i['value']
		score = math.fabs((value - avg) * 2)
		db.game2.update({'username': i['username']}, {'$inc': {'score': -score}})