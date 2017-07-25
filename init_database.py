from myblog import application
from views import db
from views.models import User, Blog, Comment

with application.app_context():
	db.create_all()
	
	# must change it
	user = User(username='admin', password='admin', is_administrator=True)
	db.session.add(user)
