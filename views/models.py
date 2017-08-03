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
	title = db.Column(db.Text)
	body = db.Column(db.Text)
	mark = db.Column(db.Text)
	category = db.Column(db.Integer)  # 1 learn	2 blah
	timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
	changed_time = db.Column(db.DateTime)
	comments = db.relationship('Comment', backref='blog', lazy='dynamic')
	is_deleted = db.Column(db.Boolean, default=False)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	changed_user_id = db.Column(db.Integer)


class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
	blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
