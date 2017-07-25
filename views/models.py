from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True)
	added_time = db.Column(db.DateTime, default=datetime.now())
	password_hash = db.Column(db.String(128))
	is_administrator = db.Column(db.Boolean, default=False)
	is_deleted = db.Column(db.Boolean, default=False)
	
	def __init__(self, username, password, is_administrator):
		self.username = username
		self.password_hash = generate_password_hash(password)
		self.is_administrator = is_administrator
	
	@property
	def password(self):
		raise AttributeError('Password is a readable attribute.')
	
	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)
	
	def __repr__(self):
		return '{}, {}, {}, {}'.format(self.id, self.username, self.added_time.strftime('%Y-%M-%d %H:%m:%s'),
									   self.is_administrator)


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


class Blog(db.Model):
	__tablename__ = 'blogs'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
	post = db.relationship('Comment', backref='post', lazy='dynamic')
	is_deleted = db.Column(db.Boolean, default=False)


class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
	post_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
