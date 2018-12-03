from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import current_app

db = SQLAlchemy(current_app)
migrate = Migrate(current_app, db)

class User(db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)


  
