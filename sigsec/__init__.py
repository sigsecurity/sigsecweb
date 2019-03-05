from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from sqlalchemy_utils import database_exists
from sqlalchemy.engine.url import make_url
import os


def create_app(config='sigsec.config.Config'):
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(config)

    with app.app_context():
        from sigsec.models import db
        db.create_all()
        
        from sigsec.g_auth import g_auth
        app.register_blueprint(g_auth)

        from sigsec.api import api
        app.register_blueprint(api)

    return app
