from security import identity
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token

# _ underscore at the begining of a variable name, means it's a private variable and it wont be import
_user_parser = reqparse.RequestParser()

_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )

_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )


class UserRegister(Resource):

    def post(self):

        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exist"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class User(Resource):

    @classmethod
    def get(cls, usr_id):
        user = UserModel.find_by_id(usr_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    def delete(cls, usr_id):
        user = UserModel.find_by_id(usr_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        # find user in database
        user = UserModel.find_by_username(data['username'])

        # this what the 'authentication' function used to do
        if user and safe_str_cmp(user.password, data['password']):
            # this identity = its what 'identity()' used to do
            access_toke = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
        # create access token
        # create refresh tocken
        # return them
            return {
                'access_token': access_toke,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials'}, 401
