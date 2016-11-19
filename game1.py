JACKPOT = 100

def set_bid(db, group_name, bid):
	db.game1.update({'group_name': group_name}, {'$set': {'bid': bid}}, upsert=True)

def calculate_scores(db):
	bids = {}
	pairings = {}
	scores = {}
	for group in db.game1.find():
		bids[int(group['group_name'])] = int(group['bid'])
	for group in db.groups.find():
		if not group in pairings.values():
			pairings[group['group_name']] = group['opponent']
	for i in pairings:
		if not i in bids:
			continue
		a, b = bids[i], bids[pairings[i]]
		if a + b > JACKPOT:
			scores[i] = scores[pairings[i]] = 0
		else:
			scores[i], scores[pairings[i]] = a, b
	for i in scores:
		db.game1.update({'group_name': str(i)}, {'$inc': {'score': scores[i]}})


def generate_pairs(db):
	groups = form_groups(db.users.find({'role': 'player'}))
	return [(groups[i], groups[i + 1]) for i in range(0, len(groups), 2)]
