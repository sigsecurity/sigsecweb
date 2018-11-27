from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import current_app

db = SQLAlchemy(current_app)
migrate = Migrate(current_app, db)

