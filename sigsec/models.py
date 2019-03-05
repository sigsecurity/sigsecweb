from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask import current_app

db = SQLAlchemy(current_app)
lm = LoginManager(current_app)

class User(UserMixin, db.Model):
  __tablename__ = "users"

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  given_name = db.Column(db.String(40))
  family_name = db.Column(db.String(40))
  name = db.Column(db.String(80))
  picture_url = db.Column(db.String(200))
  is_public = db.Column(db.Boolean, default=True)

  def serialize(self):
    if self.is_public:
      data = dict(
        id=self.id,
        email=self.email,
        given_name=self.given_name,
        family_name=self.family_name,
        name=self.name,
        picture_url=self.picture_url,
        is_public=self.is_public
      )
    else:
      data = dict(
        id=self.id,
        is_public=self.is_public
      )
  
    return data

  def __repr__(self):
    return '<User {}>'.format(self.email)

@lm.user_loader
def load_user(id):
  return User.query.get(int(id))
