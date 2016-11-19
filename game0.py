def init_scores(db):
	count = db.users.find({'role': 'player'}).count()
	for i in range(1, count + 1):
		db.scores.insert_one({'username': str(i), 'score': 0})