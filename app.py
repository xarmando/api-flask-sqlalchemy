from flask import Flask
from flask_restful import Api
# this make osme function for us, as encrypt the id at the moment to logiin
#from flask_jwt import JWT

from flask_jwt_extended import JWTManager
from security import authenticate, identity
from db import db
from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
# this can be mysql, postgres, etcb
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# this allows Flask return message execption from the backend
app.config['PROPAGATE_EXECPTIONS'] = True

# alternative of this: app.config['JWT_SECRET_KEY']
app.secret_key = 'xarmando'
api = Api(app)


#app.config['JWT_AUTH_URL_RULE'] = '/login'
# call both methods on security.py
# call /auth to get the toke once the user were autheticated
# /auth is defined by default from flask_jwt
#jwt = JWT(app, authenticate, identity)

# jwtmanager work more explicit, that mean we handle more information about login
# look authenticate and identity funciton inside security file
jwt = JWTManager(app)

# config JWT to expire within half an hour
#app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# config JWT auth key name to be 'email' instead of default 'username'
#app.config['JWT_AUTH_USERNAME_KEY'] = 'email'


# Claims: pieces of data that we can attach to the JWT payload
# Claims are used to add some extra data that allows us to do something when the JWT comes back to us.
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    # Instead of hard-coding, you should read from config file or a database
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}


# http://127.0.01:5000/student/rolf
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:usr_id>')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    # definiton here, becouse prevent circular import witj sqlalchemy object
    db.init_app(app)
    app.run(port=5000, debug=True)  # this port is by default. not necesary
