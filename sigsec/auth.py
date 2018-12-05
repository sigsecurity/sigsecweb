from flask import Blueprint, current_app, request, render_template, jsonify, session, flash
from flask_bcrypt import Bcrypt
from sigsec.database import User, db

def success(status, reason=None):
  status = bool(status)
  message = {"success" : status}

  if reason:
    message["reason"] = reason
  
  return jsonify(message)

bcrypt = Bcrypt(current_app)

auth = Blueprint('auth', __name__)

@auth.route("/register", methods=['GET', 'POST'])
def register():
  if request.method == "GET":
    return render_template("register.html")
  else:
    data = request.get_json()

    if not data:
      return success(False)

    if {"email", "password"} <= set(data):
      if User.query.filter_by(email = data['email']).first():
        return success(False, "Email already in use")
      
      bcrypt_password = bcrypt.generate_password_hash(data['password']).decode()

      new_user = User(email = data["email"], password=bcrypt_password)
      db.session.add(new_user)
      db.session.commit()
      flash("You have been successfully registered! You can now log in!", "info")
      return success(True)
    else:
      return success(False)

@auth.route("/login", methods=['GET', 'POST'])
def login():
  if request.method == "GET":
    return render_template("login.html")
  else:
    data = request.get_json()

    if not data:
      return success(False)

    if {"email", "password"} <= set(data):
      user = User.query.filter_by(email = data["email"]).first()

      if user == None:
        return success(False, "Username or password incorrect")
      
      if not bcrypt.check_password_hash(user.password, data['password']):
        return success(False, "Username or password incorrect")

      session["user_id"] = user.id
      flash("You have been logged in", "info")
      return success(True)

    else:
      return success(False)
