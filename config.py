import os

import sys


class Config():
	SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'danxinghaoshimowenqiancheng')
	SSL_DISABLE = False
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_RECORD_QUERIES = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	FLASKY_SLOW_DB_QUERY_TIME = 0.5
	
	@staticmethod
	def init__app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/flask_dev?charset=utf8'


class ProductionConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/flask_pro?charset=utf8'


config = {
	'default': ProductionConfig,
	'development': DevelopmentConfig,
	'production': ProductionConfig
}
