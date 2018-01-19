import os
class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'laomaizi secretkey'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	#此句禁用了SQLALCHEMY_TRACK_MODIFICATIONS报错
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	FLASKY_MAIL_SENDER = 'Laomaizi <20778688@qq.com>'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'navyjt@163.com'


	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	# MAIL_SERVER = 'smtp.googlemail.com'
	# MAIL_PORT = 587
	# MAIL_USE_SSL = True
	# MAIL_USE_TLS = True
	MAIL_SERVER = 'smtp.qq.com'
	MAIL_PORT = 465

	MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '20778688@qq.com'
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'gohfbwnzsdpmbiid'
	SQLALCHEMY_DATABASE_URI ='mysql://root:navyjt@localhost/pytest'#配置数据库

class TestingConfig(Config):
	TESTING = True
	

class ProductionConfig(Config):
	DEBUG = False


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}