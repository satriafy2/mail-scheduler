from flask import Flask
from app.apps import email
from app.db.database import db
from app.common.mail import mail
from app.common.tasks import scheduler
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.BaseConfig')

    from app.db import model

    db.init_app(app)
    Migrate().init_app(app, db)
    
    mail.init_app(app)
    scheduler.start()

    app.register_blueprint(email.bp)
    return app
