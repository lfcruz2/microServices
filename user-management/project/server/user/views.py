# user-management/project/server/user/views.py
 
from flask_restful import Resource, Api
from project.models import User, UserSchema
from flask import request, Blueprint
from project.models import db
from flask_jwt_extended import create_access_token
from datetime import datetime
import hashlib, jwt
from project.config.config import Config


user_schema = UserSchema()

# blueprint
user_api = Blueprint("user_api", __name__, url_prefix="/users/")
api = Api(user_api)

# /users
class UsersResource(Resource):

    def get(self):
        return user_schema.dump(User.query.all(), many=True)

    def post(self):
        # verify that all fields are present
        if 'username' not in request.json or 'password' not in request.json or 'email' not in request.json:
            return {
                    "message": "All fields are required", 
                    "status": "fail"
                    }, 400

        username=request.json['username']
        password=request.json['password']
        email=request.json['email']

        if not all([username, password, email]):
            return {
                    "message": "All fields are required", 
                    "status": "fail"
                    }, 400

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return {
                    "message": "Username or email already exists",
                     "status": "fail"
                     }, 412

        # salt generated
        salt = hashlib.sha256(str(datetime.now()).encode('utf-8')).hexdigest()

        # salted password -> concatenating password and salt
        salted_password = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

        new_user = User(username=username, 
                        password=salted_password, 
                        email=email,
                        salt=salt)
        
        db.session.add(new_user)
        db.session.commit()

        user = user_schema.dump(new_user)

        return {
                "id": user['id'],
                "createdAt": user['createdAt']
                }, 201

# /users/auth
class AuthUserResource(Resource):

    def post(self):
        if not 'username' in request.json or not 'password' in request.json:
            return {
                "message": "Username and password are required", 
                "status": "fail"
                }, 400

        username = request.json['username']
        password = request.json['password']

        if not username or not password:
            return {
                "message": "Username and password are required", 
                "status": "fail"
                }, 400

        user = db.session.query(User).filter(User.username == username).first()

        if not user:
            return {
                    "message": "User not found", 
                    "status": "fail"
                    }, 404

        # salted password with stored salt
        salted_pasword = hashlib.sha256((password + user.salt).encode('utf-8')).hexdigest()

        if salted_pasword != user.password:
            return {
                    "message": "Invalid password", 
                    "status": "fail"
                    }, 401

        token = create_access_token(identity = user.id)
        token_expire = Config.JWT_ACCESS_TOKEN_EXPIRES
        expireAt = datetime.utcnow() + token_expire

        return {"id": user.id,
                "token": token,
                "expireAt": expireAt.isoformat()
                }, 200

# /users/me
class CurrentUserResource(Resource):

    def get(self):
        token_header = request.headers.get('Authorization', None)
        if not token_header:
            return {
                    "message": "Bearer token is missing in request",
                    "status": "fail"
                    }, 400

        token = token_header.split(" ")[1]

        try:
            user_id = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=[Config.JWT_ALGORITHM])['sub']
        except (jwt.exceptions.InvalidTokenError, KeyError):
            return {
                    "message": "Token not valid", 
                    "status": "fail"
                    }, 401

        user = db.session.query(User).filter(User.id == user_id).first()

        if not user:
            return {
                    "message": "Token not valid", 
                    "status": "fail"
                    }, 401

        if user.createdAt + Config.JWT_ACCESS_TOKEN_EXPIRES < datetime.utcnow():
            return {
                    "message": "Token expired", 
                    "status": "fail"
                    }, 401
        
        return {"id": user.id,
                "username": user.username,
                "email": user.email
                }, 200

# /users/ping
class PingUserResource(Resource):

    def get(self):
        return {"message": "pong", "status": "success"}


# user endpoints
api.add_resource(UsersResource, '/')
api.add_resource(AuthUserResource, '/auth/')
api.add_resource(CurrentUserResource, '/me/')
api.add_resource(PingUserResource, '/ping/')