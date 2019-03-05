from flask import request, session, url_for, current_app, Blueprint
from requests_oauthlib import OAuth2Session
from sigsec.utils import success
from sigsec.models import User, db
from flask_login import current_user, login_user, logout_user

g_auth = Blueprint('g_auth', __name__, url_prefix='/google')

CLIENT_ID = current_app.config['GOOGLE_OAUTH_CLIENT_ID']
CLIENT_SECRET = current_app.config['GOOGLE_OAUTH_CLIENT_SECRET']
SCOPE = ['https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile']

@g_auth.route('/auth', methods=['GET'])
def get_google_login_url():
  if current_user.is_authenticated:
    return success(False, reason="Already authenticated")
  else:
    google = OAuth2Session(CLIENT_ID, redirect_uri=url_for('g_auth.google_login_callback', _external=True), scope=SCOPE)
    authorization_url, state = google.authorization_url('https://accounts.google.com/o/oauth2/v2/auth', hd='mst.edu')
    session['oauth_state'] = state
    return success(True, data=dict(auth_url=authorization_url))


@g_auth.route('/callback', methods=['GET'])
def google_login_callback():
  google = OAuth2Session(CLIENT_ID, state=session['oauth_state'], redirect_uri=url_for('g_auth.google_login_callback', _external=True))
  token = google.fetch_token('https://www.googleapis.com/oauth2/v4/token', client_secret=CLIENT_SECRET, authorization_response=request.url)
  resp = google.get('https://www.googleapis.com/oauth2/v1/userinfo')

  if resp.status_code == 200:
    user_data = resp.json()
    hd = user_data.get('hd')

    if hd is None:
      return success(False)
    
    if hd != "mst.edu":
      return success(False)

    user = User.query.filter_by(email=user_data['email']).first()

    if user is None:
      user = User()
      db.session.add(user)
      
    user.email = user_data['email']
    user.name = user_data['name']
    user.given_name = user_data['given_name']
    user.family_name = user_data['family_name']
    user.picture_url = user_data['picture']
    
    db.session.commit()

    login_user(user)

    return success(True)
  
  return success(False)

@g_auth.route('/logout', methods=['GET'])
def logout():
  logout_user()
  return success(True)
