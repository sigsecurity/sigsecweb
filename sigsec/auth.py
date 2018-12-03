from flask import Blueprint, current_app, request, render_template
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(current_app)

auth = Blueprint('auth', __name__)

@auth.route("/register", methods=['GET', 'POST'])
def register():
  if request.method == "GET":
    return render_template("register.html")
  else:
    return ""


@auth.route("/login", methods=['GET', 'POST'])
def login():
  if request.method == "GET":
    return render_template("login.html")
  else:
    return ""
