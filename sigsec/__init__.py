from flask import Flask
from sqlalchemy_utils import database_exists
from sqlalchemy.engine.url import make_url
import os


def create_app(config='sigsec.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        from sigsec.database import db

        from sigsec.views import views
        app.register_blueprint(views)

        from sigsec.auth import auth
        app.register_blueprint(auth)

    return app
