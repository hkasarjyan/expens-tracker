import datetime
import json
from ExpenseTracker import app
from flask_restful import reqparse, Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask import jsonify, Request
from flask import request
from ExpenseTracker.db import _db
from ExpenseTracker.util import verify_password, hash_password

from ExpenseTracker.models.User import User
from ExpenseTracker.models.Permissions import Permissions
from ExpenseTracker.models.Expense import Expense
from ExpenseTracker.encoder import CustomJSONEncoder



class Users(Resource):
    """description of class"""
    """Create a user """
    def post(self):
        r= request
        parser = reqparse.RequestParser()

        parser.add_argument('firstName', type=str, required = True, help='First Name of user in JSON')
        parser.add_argument('lastName', type=str, required = True, help='Last Name of user in JSON')
        parser.add_argument('email', type=str, required = True, help='E-Mail of user in JSON')
        parser.add_argument('password', type=str, required = True, help='Password Sha-256 in JSON')
        parser.add_argument('role', type=int, required = True, help='Role of user in JSON')

        args = parser.parse_args(strict=True)        
        args['id'] = -1

        user = User.from_dict(args)
        user.password = hash_password(user.password)
        user = _db.create_user(user)
        
        if user is None:
            return 'Failure', 401
        
        expire_delta = datetime.timedelta(float(1.0))
        access_token = create_access_token(identity=json.dumps(user, cls=CustomJSONEncoder), expires_delta=expire_delta)

        return jsonify(access_token=access_token)

    """Get user with id userid"""
    @jwt_required
    def get(self, userid):
        pass

    """Get all users"""
    @jwt_required
    def get(self):
        pass

    """Update user with id userid"""
    @jwt_required
    def put(self, userid):
        pass

    """Delete user with id userid"""
    @jwt_required
    def delete(self, userid):
        pass