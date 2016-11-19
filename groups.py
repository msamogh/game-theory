GROUP_SIZE = 5

def form_groups(n):
	a = list(range(1, n + 1))
	groups = [a[x:x+GROUP_SIZE] for x in range(0, len(a), GROUP_SIZE)]
	if len(groups) % 2 == 0:
		return groups
	g = groups[:-2]
	g.append(groups[-1] + groups[-2])
	return g

def form_group2(db, n):
	a = list(range(1, n + 1))
	groups = {}
	for i in a:
		if not i % 8 + 1 in groups:
			groups[i % 8 + 1] = []	
		name = db.users.find_one({'username': str(i)})
		groups[i % 8 + 1].append(name['name'])
	return groups

def form_group_db(db):
	groups = form_groups(db.users.find({'role': 'player'}).count())
	for i in groups:
		db.groups.insert_one({'group_name': groups.index(i) + 1, 'members': i, 'group_sum': sum(list(map(int, i))), 'score': 0})


def get_group(groups, i):
	try:
		result = groups[(i - 1) // GROUP_SIZE]
		return result
	except IndexError:
		return groups[(i - 1) // GROUP_SIZE - 1]

def get_group_for_user(db, i):
	return list(map(str, get_group(form_groups(db.users.find({'role': 'player'}).count()), i)))


# def prepare_groups(db):
# 	n = db.users.find().count() - 1
# 	groups = form_groups(n)
# 	for i in range(1, n + 1):
# 		db.users.update_one({'username': str(i)}, {'$set': {'group': get_group(groups, i)}}, upsert=False)

def form_opponents(db):
	groups = db.groups.find()
	for g in groups:
		group_name = g['group_name']
		if group_name % 2 == 0:
			opponent = group_name - 1
		else:
			opponent = group_name + 1
		db.groups.update({'group_name': group_name}, {'$set': {'opponent': opponent}})

class Group:
	def __init__(self, db, members):
		self.db = db
		this = db.groups.find_one({'group_sum': sum(list(map(int, members)))})
		self.group_name = this['group_name']
		self.members = members
		self.opponent = this['opponent']

	def set_opponent(opponent):
		self.db.update_one({'group_name': self.group_name}, {'$set': {'opponent': opponent}})
		self.db.update_one({'group_name': opponent}, {'$set': {'opponent': self.group_name}})

	def update_score(update_value):
		self.db.groups.update_one({'group_name': self.group_name}, {'$inc': {'score': update_value}})
		for m in self.members:
			self.db.users.update_one({'username': m}, {'$inc': {'score': update_value}})

	def reset_score():
		self.db.groups.update_one({'group_name': self.group_name}, {'score': 0})