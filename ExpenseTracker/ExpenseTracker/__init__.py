"""
The flask application package.
"""

from flask import Flask
from flask import jsonify
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import *
from flask_restful import Api, Resource
from flask_jwt_extended.config import config
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key-hovhannes-kasarjyan'
app.config['DB_HOST'] = 'localhost'
app.config['DB_USERNAME']='hovhannes'
app.config['DB_PASSWORD']='kasarjyan'
app.config['DB_PORT']=3306
app.config['DB_NAME']='expensesdb'

jwt = JWTManager(app)
class CustomApi(Api):
    def handle_error(self, e):
        for val in current_app.error_handler_spec.values():
            for handler in val.values():
                registered_error_handlers = list(filter(lambda x: isinstance(e, x), handler.keys()))
                if len(registered_error_handlers) > 0:
                    raise e
        return super().handle_error(e)


api = CustomApi(app)

version = 'v1.0'
prefix = '/api/{}'.format(version)


import flask_jwt_extended.default_callbacks



from  ExpenseTracker.resources.Login import Login
from  ExpenseTracker.resources.Users import UserResource, UsersResource
from  ExpenseTracker.resources.Expenses import ExpenseResource, ExpensesResource

api.add_resource(Login, '/login')
api.add_resource(UserResource,'/users/<int:userid>')
api.add_resource(UsersResource, '/users')
api.add_resource(ExpenseResource,'/expenses/<int:expenseid>')
api.add_resource(ExpensesResource, '/expenses')









