import json
import math

from datetime import date, datetime, time
from ExpenseTracker import app
from flask_restful import reqparse, Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask import jsonify, Request
from flask import request
from ExpenseTracker.db import _db
from ExpenseTracker.util import verify_password, hash_password
from ExpenseTracker.encoder import unbox_identity
from ExpenseTracker.models.User import User
from ExpenseTracker.models.Permissions import Permission
from ExpenseTracker.models.Permissions import Permissions
from ExpenseTracker.models.Expense import  Expense
from ExpenseTracker.encoder import CustomJSONEncoder


class ExpenseResource(Resource):

    @jwt_required
    def get(self, expenseid):
        """Get user with id userid"""
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
        expense = Expense()
        expense.id = expenseid
        expense = _db.retrieve_expense(expense)
        if expense is None:
            result = jsonify(msg='Resource not found')
            result.status_code = 404
            return result
        if expense.userid != user.id:
            if Permission.READ_EXPENSES.value not in permissions.user_permissions:
                result = jsonify(msg='Permission denied')
                result.status_code = 403
                return result

        expense_json = json.loads(json.dumps(expense, cls=CustomJSONEncoder))
        result = jsonify(expense_json)
        return result


    @jwt_required
    def put(self, expenseid):
        """Update user with id userid"""
        parser = reqparse.RequestParser()
        parser.add_argument('amount', type=float, location = 'json', help = 'Last Name of user in JSON')        
        parser.add_argument('datetime', type=str, help='ISO 8601 datetime "%Y-%m-%dT%H:%M:%S%z"')
        parser.add_argument('description', type=str, help='Password Sha-256 in JSON')
        parser.add_argument('comment', type=str, help='Role of user in JSON')
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

        expense = Expense()
        expense.id = expenseid
        expense = _db.retrieve_expense(expense)
        if expense is None:
            result = jsonify(msg='Resource not found')
            result.status_code = 404
            return result
        if expense.userid != user.id:
            if Permission.WRITE_EXPENSES.value not in permissions.user_permissions:
                result = jsonify(msg='Permission denied')
                result.status_code = 403
                return result
                
        modified_expense = Expense.from_dict(args)
        modified_expense.id = expenseid

        result = _db.update_expense(modified_expense)
        if result is None:
             result = jsonify(msg='Failed to update the expense8')
             result.status_code = 403
             return result
        return  jsonify()

    @jwt_required
    def delete(self, expenseid):
        """Delete user with id userid"""
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
        expense = Expense()
        expense.id = expenseid
        expense = _db.retrieve_expense(expense)
        if expense is None:
            result = jsonify(msg='Resource not found')
            result.status_code = 404
            return result
        if expense.userid != user.id:
            if Permission.WRITE_EXPENSES.value not in permissions.user_permissions:
                result = jsonify(msg='Permission denied')
                result.status_code = 403
                return result
        result = _db.delete_expense(expense)
        if result is None:
             result = jsonify(msg='Failed to update the expense')
             #todo: chack error code
             result.status_code = 400
             return result

        result = jsonify(msg='Expense deleted')
        result.status_code = 204
        return result


class ExpensesResource(Resource):

    """description of class"""
    """Create a user """
    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('userid', type=int, help='First Name of user in JSON')
        parser.add_argument('amount', type=float, required = True, help='Last Name of user in JSON')
        parser.add_argument('datetime', type=str, required = True, help='ISO 8601 datetime "%Y-%m-%dT%H:%M:%S"')
        parser.add_argument('description', type=str, required = True, help='Password Sha-256 in JSON')
        parser.add_argument('comment', type=str, required = True, help='Role of user in JSON')
        
        args = parser.parse_args(strict=True)        
        args['id'] = -1
        if args['userid'] is None:
            del args['userid']

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

        expense = Expense.from_dict(args)
        if expense.userid is not None and expense.userid != user.id :
            #expense different user id is provided, check for permission
            if Permission.WRITE_EXPENSES.value not in permissions.user_permissions:
                result = jsonify(msg='Permission denied')
                result.status_code = 403
                return result
            else:
                #Check for user to exist
                u = User()
                u.id = expense.userid
                u = _db.retrieve_user_with_id(u)
                if u is None:
                    result = jsonify(msg='User not found')
                    result.status_codes = 400
                    return result
        if expense.userid is None:
            expense.userid = user.id

        expense = _db.create_expense(expense)
        
        if expense is None:
             result = jsonify(msg='Failed to create the expense')
             #todo: chack error code
             result.status_code = 401
             return result
        #"Remove token generation keep only for login"
        return jsonify(id=expense.id, user_id=expense.userid)

    @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("userid", type=int, help="asdasd")
        parser.add_argument('startdatetime', type=str,  help='ISO 8601 datetime "%Y-%m-%dT%H:%M:%S"')
        parser.add_argument('enddatetime', type=str,  help='ISO 8601 datetime "%Y-%m-%dT%H:%M:%S"')
        parser.add_argument('description', type=str, help='descrition tip in json')
        parser.add_argument('comment', type=str,  help='comment tip in json')
        parser.add_argument('minamount', type=str, help='minimum amount of expense in json')
        parser.add_argument('maxamount', type=str, help='maximum amount of expense in json')
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
        expenses = None

        filters = dict([(a,b) for a, b in args.items() if b != None])
        try:
            startTimeIsThere = False
            endTimeIsThere = False
            if 'startdatetime' in filters:
                start_time = datetime.fromisoformat(filters['startdatetime'])
                startTimeIsThere = True
                if 'enddatetime' in filters:
                    end_time = datetime.fromisoformat(args['enddatetime'])
                    endTimeIsThere = True
            elif 'enddatetime' in filters:
                end_time = datetime.fromisoformat(args['enddatetime'])
                endTimeIsThere = True
            if startTimeIsThere:
                filters['startdatetime'] = start_time
            if endTimeIsThere:
                filters['enddatetime'] = end_time
            filters['timeType'] = "datetime"
        except :
            try:
                startTimeIsThere = False
                endTimeIsThere = False
                if 'startdatetime' in filters:
                    start_time = time.fromisoformat(filters['startdatetime'])
                    startTimeIsThere = True
                    if 'enddatetime' in filters:
                        end_time = time.fromisoformat(args['enddatetime'])
                        endTimeIsThere = True
                elif 'enddatetime' in filters:
                    end_time = time.fromisoformat(args['enddatetime'])
                    endTimeIsThere = True
                if startTimeIsThere:
                    filters['startdatetime'] = start_time
                if endTimeIsThere:
                    filters['enddatetime'] = end_time
                filters['timeType'] = "time"
            except:
                result = jsonify(msg='Wrong filter used')
                result.status_code = 400
                return result

        if 'userid' in filters:
            if filters['userid'] != user.id:
                if Permission.READ_EXPENSES.value in permissions.user_permissions:
                    #Check for user to exist
                    u = User()
                    u.id = filters["userid"]
                    u = _db.retrieve_user_with_id(u)
                    if u is None:
                        result = jsonify(msg='User not found')
                        result.status_codes = 400
                        return result
                    expenses = _db.retrieve_user_expenses(u, filters)
                else:
                    result = jsonify(msg='Permission denied')
                    result.status_code = 403
                    return result
            else:
                expenses = _db.retrieve_user_expenses(user, filters)
        else:
            if Permission.READ_EXPENSES.value not in permissions.user_permissions:
                filters["userid"] = user.id
                expenses = _db.retrieve_user_expenses(user, filters)
            else:
                expenses = _db.retrieve_expenses(filters)

        expenses_json = json.loads(json.dumps(expenses, cls=CustomJSONEncoder))

        result = jsonify(expenses=expenses_json)
        return result