from requests_oauthlib import OAuth2Session
from flask import request, redirect, session, url_for, jsonify, current_app, Blueprint
from sigsec.database import db, User

auth = Blueprint('auth', __name__)

CLIENT_ID = current_app.config['GOOGLE_OAUTH_CLIENT_ID']
CLIENT_SECRET = current_app.config['GOOGLE_OAUTH_CLIENT_SECRET']
SCOPE = ['https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile']

@auth.route('/join')
@auth.route('/login')
def external_login():
  google = OAuth2Session(CLIENT_ID, redirect_uri=url_for('auth.callback', _external=True), scope=SCOPE)
  authorization_url, state = google.authorization_url('https://accounts.google.com/o/oauth2/v2/auth')
  
  session['oauth_state'] = state
  return redirect(authorization_url)

@auth.route('/callback')
def callback():
  google = OAuth2Session(CLIENT_ID, state=session['oauth_state'], redirect_uri=url_for('auth.callback', _external=True))
  token = google.fetch_token('https://www.googleapis.com/oauth2/v4/token', client_secret=CLIENT_SECRET, authorization_response=request.url)
  resp = google.get('https://www.googleapis.com/oauth2/v1/userinfo')

  if resp.status_code == 200:
    user_data = resp.json()
    hd = user_data.get('hd')

    if hd is None:
      return redirect('/login')
    
    if hd != "mst.edu":
      return redirect('/login')

    user = User.query.filter_by(email=user_data['email']).first()

    if user is None:
      user = User()
      user.email = user_data['email']
      user.name = user_data['name']
      user.given_name = user_data['given_name']
      user.family_name = user_data['family_name']
      user.picture_url = user_data['picture']
    
      db.session.add(user)
      db.session.commit()

    session['google_oauth_token'] = token
    session['email'] = user_data['email']
    return redirect('/')
  return '', 500


@auth.route('/logout')
def logout():
  session.clear()
  return redirect('/')
