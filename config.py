import os


class Config():
	SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'f&k*n@kfa_H*tf^$)')
	SSL_DISABLE = False
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_RECORD_QUERIES = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	FLASKY_SLOW_DB_QUERY_TIME = 0.5
	FLASKY_PER_PAGE = 10
	
	@staticmethod
	def init__app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/flask_dev?charset=utf8mb4'


class ProductionConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/flask_pro?charset=utf8mb4'


config = {
	'default': ProductionConfig,
	'development': DevelopmentConfig,
	'production': ProductionConfig
}
