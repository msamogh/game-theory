from flask import Flask, request, render_template, session, redirect, url_for
from flask.ext.login import current_user, LoginManager, login_user, logout_user
from pymongo import MongoClient

import game1
import game2
import game3
import game4

import players
import groups

from datetime import datetime

class User:
	def __init__(self, username, name=None):
		self.username = username
		self.name = name

	def is_authenticated(self):
		return not self.username is None

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.username

app = Flask(__name__)
app.secret_key = 'A0Zr9qaj/3yXR~XHH!jmN]LWX/,?RT'

login_manager = LoginManager()
login_manager.init_app(app)


client = MongoClient('localhost', 27017)

db = client.game_theory

"""General stuff"""

@app.before_first_request
def initialize():
	if db.users.find({'username': 'msamogh'}).count() == 0:
		db.users.insert_one({'added': datetime.utcnow(), 'username': 'msamogh', 'password': 'amoghms', 'role': 'admin'})


@login_manager.user_loader
def load_user(username):
	if not db.users.find_one({'username': username}) is None:
		return User(username)
	return None

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated and current_user.get_id() == 'msamogh':
		if request.method == 'GET':
			return render_template('register.html', users=players.get_all_players(db))
		player = players.Player(db, request.form['name'])
		
		return render_template('register.html', username=player.username,users=players.get_all_players(db))
	return 'Not authorized'



@app.route('/', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		if current_user.get_id == 'msamogh':
			return render_template('register.html')
		return render_template('game0.html')

	if request.method == 'POST':
		user_id = request.form['inputId']
		password = request.form['inputPassword']

		u = db.users.find_one({'username': user_id, 'password': password})
		if u is None:
			return render_template('index.html', error='Wrong username/password combination')
		login_user(User(user_id))
		return render_template('register.html') if user_id == 'msamogh' else render_template('game0.html')
	return render_template('index.html')

@app.route("/logout")
def logout():
   	logout_user()
   	return redirect("/")
""" End of general stuff """


""" Admin URLs """
# @app.route('/prepare/game1')
# def prepare_game1():
# 	game1.prepare_groups(db)
# 	return 'Groups formed'
@app.route('/finalize')
def finalize():
	if current_user.is_authenticated and current_user.get_id() == 'msamogh':
		groups.form_group_db(db)
		groups.form_opponents(db)
		return 'Groups formed'
	return 'Not authorized'

@app.route('/groups')
def display_groups():
	mod_groups= groups.form_group2(db, db.users.find({'role': 'player'}).count())
	return render_template('groups.html', mod_groups=mod_groups)

@app.route('/who')
def who():
	return current_user.get_id()

@app.route('/end/game1')
def flush_results_1():
	if current_user.is_authenticated and current_user.get_id() == 'msamogh':
		game1.calculate_scores(db)
		return 'Calculated. Do not reload unnecessarily!!!!!!!!!!!!!!!!!'
	return 'Not authorized'

@app.route('/end/game2')
def flush_results_2():
	if current_user.is_authenticated and current_user.get_id() == 'msamogh':
		game2.calculate_scores(db)
		return 'Calculated. Do not reload unnecessarily!!!!!!!!!!!!!!!!!'
	return 'Not authorized'
@app.route('/end/game3')
def flush_results_3():
	if current_user.is_authenticated and current_user.get_id() == 'msamogh':
		game3.calculate_scores(db)
		return 'Calculated. Do not reload unnecessarily!!!!!!!!!!!!!!!!!'
	return 'Not authorized'
@app.route('/end/game4')
def flush_results_4():
	if current_user.is_authenticated and current_user.get_id() == 'msamogh':
		game4.calculate_scores_db(db)
		return 'Calculated. Do not reload unnecessarily!!!!!!!!!!!!!!!!!'
	return 'Not authorized'


@app.route('/flush/game1')
def end_game_1():
	if current_user.is_authenticated and current_user.get_id() == 'msamogh':
		for i in db.game1.find():
			group_name = i['group_name']
			score = i['score']
			g = db.groups.find_one({'group_name': int(group_name)})
			for m in g['members']:
				db.users.update_one({'username': str(m)}, {'$inc': {'score': score}})
		return 'Flushed game 1 score to master DB'

	return 'Not authorized'

@app.route('/flush/game2')
def end_game_2():
	if current_user.is_authenticated and current_user.get_id() == 'msamogh':
		for i in db.game2.find():
			db.users.update_one({'username': i['username']}, {'$inc': {'score': i['score']}})
		return 'Flushed game 2 score to master DB'

	return 'Not authorized'

@app.route('/flush/game3')
def end_game_3():
	if current_user.is_authenticated and current_user.get_id() == 'msamogh':
		for i in db.game3.find():
			group_name = i['group_name']
			score = i['score']
			g = db.groups.find_one({'group_name': int(group_name)})
			for m in g['members']:
				db.users.update_one({'username': str(m)}, {'$inc': {'score': score}})
		return 'Flushed game 3 score to master DB'

	return 'Not authorized'

@app.route('/flush/game4')
def end_game_4():
	if current_user.is_authenticated and current_user.get_id() == 'msamogh':
		for i in db.game4.find():
			db.users.update_one({'username': i['username']}, {'$inc': {'score': i['score']}})
		return 'Flushed game 4 score to master DB'

	return 'Not authorized'

""" End of Admin URLs """

"""Result URLs"""
@app.route('/results/game1')
def result_game1():
	if current_user.is_authenticated and current_user.get_id() == 'msamogh':
		return render_template('results1.html', table=db.game1.find())	
	return 'Not authorized'

@app.route('/results/game2')
def result_game2():
	if current_user.is_authenticated and current_user.get_id() == 'msamogh':
		return render_template('results2.html', avg=game2.get_average(db), table=db.game2.find().sort('score', -1))
	return 'Not authorized'

@app.route('/results/game3')
def result_game3():
	if current_user.is_authenticated and current_user.get_id() == 'msamogh':
		return render_template('results3.html', table=db.game3.find())
	return 'Not authorized'

@app.route('/results/game4')
def result_game4():
	if current_user.is_authenticated and current_user.get_id() == 'msamogh':
		return render_template('results4.html', table=db.game4.find().sort('group_name'))
	return 'Not authorized'

@app.route('/leaderboard')
def leaderboard():
	if current_user.is_authenticated and current_user.get_id() == 'msamogh':
		return render_template('leaderboard.html', scores=enumerate(db.users.find({'role': 'player'}).sort([("score", -1)])))
	return 'Not authorized'

"""End of results URLs"""


""" Games """
@app.route('/gameone')
def gameone():
	members = groups.get_group_for_user(db, int(current_user.get_id()))
	group = groups.Group(db, members)
	error = 0
	if request.args.get('error'):
		error = 1
	return render_template('game1.html', error=error, opponent=group.opponent, group_name=group.group_name, group=[db.users.find_one({'username': str(x)})['name'] for x in members])

@app.route('/game2')
def gametwo():
	return render_template('game2.html')

@app.route('/thirdgame')
def gamethree():
	members = groups.get_group_for_user(db, int(current_user.get_id()))
	group = groups.Group(db, members)
	return render_template('game3.html', group_name=group.group_name)

@app.route('/4')
def gamefour():
	members = groups.get_group_for_user(db, int(current_user.get_id()))
	group = groups.Group(db, members)
	return render_template('game4.html', group_name=group.group_name, group=[db.users.find_one({'username': str(x)})['name'] for x in members])

@app.route('/game/<int:game>', methods=['POST'])
def handle_game_submit(game):
	COOP = 1
	DEF = 0
	if game == 1:
		group_name = request.form['group_name']
		value = request.form['bid']
		if int(value) == 50:
			return redirect('/gameone?error=50')
		game1.set_bid(db, group_name, value)
		return redirect('/gameone')
	elif game == 2:
		try:
			value = float(request.form['bid'])
		except ValueError:
			return 'Invalid value'
		game2.set_value(db, current_user.get_id(), value)
		return redirect('/game2')
	elif game == 3:
		action = int(request.form['action'])
		group_name = request.form['group_name']
		game3.set_action(db, group_name, current_user.get_id(), action)
		return redirect('/thirdgame')
	elif game == 4:
		action = int(request.form['action'])
		group_name = request.form['group_name']
		action = int(request.form['action'])
		game4.set_choice(db, group_name, current_user.get_id(), action)
		return redirect('/4')
	return 'idk'

""" End of Games"""

if __name__ == '__main__':
	#app.run(host='172.1.6.99', port=8888, debug=True)
	app.run(host='0.0.0.0', port=8080, debug=True)