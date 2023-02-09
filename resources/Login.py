import datetime
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

class Login(Resource):
    """description of class"""
    def post(self):
        r= request
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required = True, help='E-Mail address of user in JSON')
        parser.add_argument('password', type=str, required = True, help='Password Sha-256 in JSON')
        #parser.add_argument('email', location= 'json', help='E-Mail address of user in JSON')
        #parser.add_argument('password', help='Password Sha-256 in JSON')
        args = parser.parse_args(strict=True)        
        
        email = args['email']
        password = args['password']
        #if not username:
        #    response = jsonify(msg="Missing username parameter")
        #    response.status_code = 400
        #    return response
        #if not password:
        #    response = jsonify(msg="Missing password parameter")
        #    response.status_code = 400
        #    return response

        
        # Identity can be any data that is json serializable
        user = User()
        user.email = email
        user = _db.retreive_user(user)
        
        if user is None:
            return 'Wrong username or password',401
        if not verify_password(user.password(), password):
            return 'Wrong username or password',401

        expire_delta = datetime.timedelta(float(1.0))
        access_token = create_access_token(identity=username, expires_delta=expire_delta)

        return jsonify(access_token=access_token)

