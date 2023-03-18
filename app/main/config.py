import os

basedir = os.path.abspath(os.path.dirname("database")) + '/app/database'

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING=True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'projectDB.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '9OLWxND4o83j4K4iuopO'


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'testDB.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY