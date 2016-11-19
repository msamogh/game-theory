COOP = 1
DEF = 0

def set_action(db, group_name, username, action):
	db.game3.update({'group_name': group_name}, {'$set': {'action': action}}, upsert=True)

def calculate_payoffs(a, b):
	if a == COOP:
		return (30, 30) if b == COOP else (0, 50)
	else:
		return (50, 0) if b == COOP else (-10, -10)


def calculate_scores(db):
	actions = {}
	scores = {}
	pairings = {}
	for group in db.game3.find():
		actions[int(group['group_name'])] = int(group['action'])
	for group in db.groups.find():
		if not group in pairings.values():
			pairings[group['group_name']] = group['opponent']
	for i in pairings:
		if not i in actions:
			continue
		a, b = actions[i], actions[pairings[i]]
		scores[i], scores[pairings[i]] = calculate_payoffs(a, b)
	for i in scores:
		db.game3.update({'group_name': str(i)}, {'$inc': {'score': scores[i]}})
