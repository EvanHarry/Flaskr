import os


class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SECRET_KEY = 'secret key'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres@127.0.0.1:5432/flaskr'


class TestingConfig(Config):
    SECRET_KEY = 'secret key'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres@127.0.0.1:5432/flaskr_test'


class ProductionConfig(Config):
    SECRET_KEY = os.getenv('FLASKR_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgres://evan:imfaa#18@127.0.0.1:5432/flaskr'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
