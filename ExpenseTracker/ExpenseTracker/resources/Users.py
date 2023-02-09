import datetime
import json
import re

from ExpenseTracker import app
from flask_restful import reqparse, Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask import jsonify, Request
from flask import request
from ExpenseTracker.db import _db
from ExpenseTracker.util import verify_password, hash_password
from ExpenseTracker.encoder import box_identity
from ExpenseTracker.encoder import unbox_identity

from ExpenseTracker.models.User import User
from ExpenseTracker.models.Permissions import Permissions, Permission
from ExpenseTracker.models.Expense import Expense
from ExpenseTracker.encoder import CustomJSONEncoder



class UserResource(Resource):
    """Get user with id userid"""
    @jwt_required
    def get(self, userid):
        identity = get_jwt_identity()
        if identity is None:
            result = jsonify(msg='Authentication failed')
            result.status_code = 401
            return result
        user, permissions = unbox_identity(identity)
        if user is None or permissions is None:
            result = jsonify(msg='Token is damaged')
            result.status_code = 401
            return result
        if user.id != userid:
            # user should be either admin or superuser
            # check permissions to contain READ_USERS
            result = jsonify(msg='Permission denied')
            result.status_code = 403
            return result
        user = _db.retrieve_user_with_id(user)
        if user is None:
            result = jsonify(msg='Resource not found')
            result.status_code = 404
            return result
        user_json = json.loads(json.dumps(user, cls=CustomJSONEncoder))
        del user_json['password']
        result = jsonify(user_json)
        return result

    """Update user with id userid"""
    @jwt_required
    def put(self, userid):

        parser = reqparse.RequestParser()
        parser.add_argument('firstName', type=str, help='First Name of user in JSON')
        parser.add_argument('lastName', type=str,  help='Last Name of user in JSON')        
        parser.add_argument('password', type=str,  help='Password Sha-256 in JSON')
        args = parser.parse_args(strict=True)

        identity = get_jwt_identity()
        if identity is None:
            result = jsonify(msg='Authentication failed')
            result.status_code = 401
            return result
        user, permissions = unbox_identity(identity)
        if user is None or permissions is None:
            result = jsonify(msg='Token is damaged')
            result.status_code = 401
            return result
        if user.id != userid:
            # user should be either admin or superuser
            # check permissions to contain READ_USERS
            result = jsonify(msg='Permission denied')
            result.status_code = 403
            return result
        modified_user = User.from_dict(args)
        modified_user.id = userid

        modified_user = _db.update_user(modified_user)
        if modified_user is None:
            result = jsonify(msg='Failed to update the user')
            result.status_code = 403
            return result
        return  jsonify()



    """Delete user with id userid"""
    @jwt_required
    def delete(self, userid):
        identity = get_jwt_identity()
        if identity is None:
            result = jsonify(msg='Authentication failed')
            result.status_code = 40
            return result
        user, permissions = unbox_identity(identity)
        if user is None or permissions is None:
            result = jsonify(msg='Token is damaged')
            result.status_code = 401
            return result
        if user.id != userid:
            # user should be either admin or superuser
            # check permissions to contain READ_USERS
            result = jsonify(msg='Permission denied')
            result.status_code = 403
            return result
        user_to_delete = User()
        user_to_delete.id = userid
        user_to_delete = _db.retrieve_user_with_id(user_to_delete)
        if user_to_delete is None:
            result = jsonify(msg='Resource not found')
            result.status_code = 404
            return result
        result = _db.delete_user(user_to_delete)
        if result is None:
            result = jsonify(msg='Failed to delete the user')
            result.status_code = 400
            return result

        #TODO:chack is there a need to jsonify this as well
        return "User deleted", 200



class UsersResource(Resource):
    """description of class"""
    def post(self):
        """Create a user """
        parser = reqparse.RequestParser()

        parser.add_argument('firstName', type=str, required = True, help='First Name of user in JSON')
        parser.add_argument('lastName', type=str, required = True, help='Last Name of user in JSON')
        parser.add_argument('email', type=str, required = True, help='E-Mail of user in JSON')
        parser.add_argument('password', type=str, required = True, help='Password Sha-256 in JSON')
        parser.add_argument('role', type=int, required = True, help='Role of user in JSON')

        args = parser.parse_args(strict=True)        
        args['id'] = -1
        user = User.from_dict(args)
        prog = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        #check whether the email is valid
        if prog.match(user.email) is None:
            result = jsonify(msg='Bad recipient address syntax')
            result.status_code = 513
            return result
        retrieved_user = _db.retrieve_user(user)
        if retrieved_user is not None:
            result = jsonify(msg='User alredy exists')
            result.status_code = 409
            return result

        user.password = hash_password(user.password)
        user = _db.create_user(user)
        
        if user is None:
            result = jsonify(msg='Failure')
            result.status_code = 401
            return result        
        #"Remove token generation keep only for login"
        
        expire_delta = datetime.timedelta(float(1.0))
        identity = box_identity(user,_db.retrieve_user_permissions(user))
        access_token = create_access_token(identity=identity, expires_delta=expire_delta)
        return jsonify(access_token=access_token, id=user.id)

    @jwt_required
    def get(self):
        identity = get_jwt_identity()
        if identity is None:
            result = jsonify(msg='Authentication failed')
            result.status_code = 401
            return result
        user, permissions = unbox_identity(identity)
        if user is None or permissions is None:
            result = jsonify(msg='Token is damaged')
            result.status_code = 401
            return result
        if Permission.READ_USERS.value not in permissions.user_permissions:
            # user should be either admin or superuser
            # check permissions to contain READ_USERS
            result = jsonify(msg='Permission denied')
            result.status_code = 403
            return result
        
        users = _db.retrieve_users()
        users_json = json.loads(json.dumps(users, cls=CustomJSONEncoder))        
        for u in users_json:
            del u["password"]

        result = jsonify(users=users_json)
        return result