from werkzeug import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(120), unique = True)
	pwdhash = db.Column(db.String(54))
	posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

	def __init__(self, firstname, lastname, email, password):
		self.firstname=firstname.title()
		self.lastname=lastname.title()
		self.email=email.lower()
		self.set_password(password)

	def is_authenticated(self):
		return True

	def photo(self, size):
		return 'https://www.graph.facebook.com/me/picture'

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)

	def __repr__(self):
		return '<User%r>' % (self.firstname)

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key = True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	users_id = db.Column(db.Integer, db.ForeignKey('users.id'))

	def __repr__(self):
		return '<Post%r>' % (self.body)


# accessing information on facebook.

""" data = facebook.get('/me').data
if 'id' in data and 'name' in data:
    user_id = data['id']
    user_name = data['name'] """