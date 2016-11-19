GROUP_SIZE = 5


def form_groups(n):
	a = list(range(1, n + 1))
	groups = [a[x:x+GROUP_SIZE] for x in range(0, len(a), GROUP_SIZE)]
	if len(groups) % 2 == 0:
		return groups
	g = groups[:-2]
	g.append(groups[-1] + groups[-2])
	return g

def prepare_groups(db):
	n = db.users.find().count() - 1
	groups = form_groups(n)
	for i in range(1, n + 1):
		db.users.update_one({'username': str(i)}, {'$set': {'group': get_group(groups, i)}}, upsert=False)

def get_group(groups, i):
	try:
		result = groups[(i - 1) // GROUP_SIZE]
		return result
	except IndexError:
		return groups[(i - 1) // GROUP_SIZE - 1]

def get_group_for_user(db, i):
	return get_group(form_groups(db.users.find({'role': 'player'}).count()), i)