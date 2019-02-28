from flask import Blueprint, render_template, session

views = Blueprint('views', __name__)

@views.route("/")
def hello_world():
  if 'google_oauth_token' in session:
    authenticated = True
  else:
    authenticated = False
  return render_template("main/index.html", authenticated=authenticated)

@views.route("/officers")
def officers_page():
  return render_template("main/officers.html")
