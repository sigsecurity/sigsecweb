from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import current_app

db = SQLAlchemy(current_app)
migrate = Migrate(current_app, db)

class User(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  given_name = db.Column(db.String(40))
  family_name = db.Column(db.String(40))
  name = db.Column(db.String(80))
  picture_url = db.Column(db.String(150))


  
