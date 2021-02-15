
from werkzeug.security import safe_str_cmp
from models.user import UserModel

# he authenticate function is called with that username and password. Flask-JWT set this up when we created the JWT object.


def authenticate(username, password):
    user = UserModel.find_by_username(username)

    # it´s not good idea compare strings directly, becouse Python old version
    # if user and user.password == password:
    # A way to sove this problem  to any SO and a

    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
