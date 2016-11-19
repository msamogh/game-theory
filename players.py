from datetime import datetime

def get_all_players(db):
	return db.users.find({'role': 'player'}).sort([("added", -1)])

class Player(object):
	def __init__(self, db, name):
		self.db = db
		count = db.users.count()
		self.username = count
		db.users.insert_one({'added': datetime.utcnow(), 'username': str(count), 'password': str(count * 9 - 8), 'name': name, 'role': 'player', 'score': 0})
	
