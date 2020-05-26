import os
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000

BASEDIR = Path(Path(__file__).parent)
DB_DIRECTORY = Path(BASEDIR, "db-data")
DB_DIRECTORY.mkdir(parents=True, exist_ok=True)

ENV_PATH = Path(BASEDIR, '.env')
load_dotenv(dotenv_path=ENV_PATH, verbose=False)


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious_secret_key")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{Path(DB_DIRECTORY, 'torrents.db')}"


class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = "development"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    FLASK_ENV = "development"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{Path(DB_DIRECTORY, 'torrents_test.db')}"
    )
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = "production"


config_by_name = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "prod": ProductionConfig,
}

key = Config.SECRET_KEY
