def calculate_scores(choices):
	if not 1 in choices.values():
		return {x:-100 for x in choices}
	return {x:40 if not choices[x] else -20 for x in choices}

def set_choice(db, group_name, username, action):
	db.game4.update_one({'username': username, 'group_name': group_name}, {'$set': {'action': action}}, upsert=True)
	if not 'score' in db.game4.find_one({'username': username}):
		db.game4.update({'username': username}, {'$set': {'score': 0}})

def calculate_scores_db(db):
	scores = {}
	for i in db.game4.find():
		group_name = i['group_name']
		if not group_name in scores:
			group_scores = db.game4.find({'group_name': group_name})
			scores[group_name] = {}
			for j in group_scores:
				scores[group_name][j['username']] = j['action']

	print(scores)
	results = {}
	for g in scores:
		for x in scores[g]:
			results[g] = calculate_scores(scores[g])

	for i in results:
		for j in results[i]:
			db.game4.update({'username': str(j)}, {'$inc': {'score': results[i][j]}})