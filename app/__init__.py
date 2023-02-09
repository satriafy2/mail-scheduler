from flask import Flask
from flask_migrate import Migrate
from app.apps import email
from app.db.database import db
from app.extension.scheduler import scheduler
from app.extension.mail import mail


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.BaseConfig')

    from app.db import model
    db.init_app(app)
    Migrate().init_app(app, db)

    mail.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    app.register_blueprint(email.bp)
    return app
