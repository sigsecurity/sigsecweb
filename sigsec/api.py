from flask import request, session, url_for, current_app, Blueprint
from sigsec.models import *
from flask_login import current_user, logout_user
from sigsec.utils import success

api = Blueprint('api', __name__, url_prefix='/v1')

resource_not_found = success(False, reason='Resource not found')
not_authenticated = success(False, reason='You are not allowed to access this resource')

@api.route('/users')
def users_list():
  users = [user.serialize() for user in User.query.all()]
  return success(True, data=dict(users=users))

@api.route('/users/<int:user_id>')
def get_user(user_id):
  user = User.query.get(user_id)
  if user is None:
    return resource_not_found
  else:
    return success(True, data=dict(user=user.serialize()))

@api.route('/users/current-user')
def get_current_user():
  if current_user.is_authenticated:
    return success(True, data=dict(user=current_user.serialize()))
  else:
    return success(True, data=dict(user=None))

@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
  if current_user.is_authenticated:
    if current_user.id == user_id or current_user.is_admin:
      user = User.query.get(user_id)
      if user is None:
        return resource_not_found
      db.session.delete(user)
      db.session.commit()
      logout_user()
      return success(True)
  return not_authenticated
  


