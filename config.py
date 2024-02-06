import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

basedir = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI"
    ) or "sqlite:///" + os.path.join(basedir, "instance", "seedy.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUNDLE_ERRORS = True
    DEBUG = True


class ProductionConfig:
    SECRET_KEY = os.environ.get("PROD_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI"
    ) or "sqlite:///" + os.path.join(basedir, "instance", "seedy.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUNDLE_ERRORS = True
    DEBUG = True


class TestingConfig:
    SECRET_KEY = os.environ.get("TEST_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DB_URI"
    ) or "sqlite:///" + os.path.join(basedir, "instance", "test.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BUNDLE_ERRORS = True
    DEBUG = True


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    default=DevelopmentConfig,
)
