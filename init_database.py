from myblog import application
from views import db
from views.models import User, Blog, Comment

with application.app_context():
	db.create_all()
	# must change the password
	user = User(username='admin', password='admin', is_administrator=True)
	
	blog = Blog(title='about', category=0, body='about', author_id=1)
	db.session.add(user)
	db.session.add(blog)
