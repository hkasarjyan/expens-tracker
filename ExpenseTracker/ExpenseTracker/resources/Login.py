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
from ExpenseTracker.encoder import box_identity
from ExpenseTracker.encoder import unbox_identity

from ExpenseTracker.models.User import User
from ExpenseTracker.models.Permissions import Permissions
from ExpenseTracker.models.Expense import Expense
from ExpenseTracker.encoder import CustomJSONEncoder

class Login(Resource):
    """description of class"""
    def post(self):
        r= request
        parser = reqparse.RequestParser()
        parser.add_argument('email', location='json', type=str, required = True, help='E-Mail address of user in JSON')
        parser.add_argument('password', location='json', type=str, required = True, help='Password Sha-256 in JSON')
        args = parser.parse_args(strict=True)        
        
        email = args['email']
        password = args['password']

        user = User()
        user.email = email
        user = _db.retrieve_user(user)
        
        if user is None:
            result = jsonify(msg='Wrong username or password')
            result.status_code = 401
            return result
        if not verify_password(user.password, password):            
            result = jsonify(msg='Wrong username or password')
            result.status_code = 401
            return result

        expire_delta = datetime.timedelta(float(1.0))
        identity = box_identity(user,_db.retrieve_user_permissions(user))
        access_token = create_access_token(identity=identity, expires_delta=expire_delta)
        return jsonify(access_token=access_token, id=user.id)

