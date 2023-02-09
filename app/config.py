from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from dotenv import load_dotenv
from os import environ, path

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class BaseConfig:
    DEBUG = environ.get('DEBUG', True)
    FLASK_ENV = environ.get('FLASK_ENV', 'development')
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI')

    SCHEDULER_TIMEZONE = environ.get('SCHEDULER_TZ', 'Asia/Singapore')
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URI)
    }

    MAIL_SERVER = environ.get('MAIL_SERVER', '')
    MAIL_PORT = environ.get('MAIL_PORT', '')
    MAIL_USERNAME = environ.get('MAIL_USERNAME', '')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD', '')
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS', True)
    MAIL_USE_SSL = environ.get('MAIL_USE_SSL', False)
    MAIL_DEBUG = environ.get('MAIL_DEBUG', True)
