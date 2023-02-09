from ExpenseTracker.models.User import User
from ExpenseTracker.models.Expense import Expense
from ExpenseTracker import app
import mysql.connector
from ExpenseTracker.util import generate_insert_query

class db:
    DB_HOST = app.config['DB_HOST']
    DB_USERNAME = app.config['DB_USERNAME']
    DB_PASSWORD = app.config['DB_PASSWORD']
    DB_PORT = app.config['DB_PORT']
    DB_NAME = app.config['DB_NAME']

    def create_connection(self):
        connection = mysql.connector.connect(host=self.DB_HOST,
            user=self.DB_USERNAME,
            password=self.DB_PASSWORD,
            port=self.DB_PORT,
            database=self.DB_NAME)
        return connection



    def create_user(self, user: User):
        connection = self.create_connection()
        cursor = connection.cursor()
        #Retreive before insert
        query, values_map = generate_insert_query(user, 'users')
        cursor.execute(query, values_map)        
        if cursor.rowcount > 0 :
            user.id = cursor.lastrowid
        
        connection.commit()
        connection.close()
        return user

    def retreive_user(self, user: User):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT id, firstName, lastName, email, password, role 
                          FROM users
                          WHERE email=%(email)s""", {'email':user.email})
        rows = cursor.fetchall()
        if len(rows) == 1:
            user = User.from_dict(rows[0])
            return user
        return None
    def update_user(self, user: User):
        return None
    def delete_user(self, user: User):
        return None

    def create_expense(self, expense: Expense):
        connection = self.create_connection()
        cursor = connection.cursor()
        #Retreive before insert
        query, values_map = generate_insert_query(expense, 'expenses')
        cursor.execute(query, values_map)        
        if cursor.rowcount > 0 :
            expense.id = cursor.lastrowid        
        connection.commit()
        connection.close()
        return user
        return None
    def retrieve_expense(self, expense: Expense):
        return None
    def update_expense(self, expense: Expense):
        return None
    def delete_expense(self, expense: Expense):
        return None
    #Custom methods should be checked
    def retrieve_user_expenses(self, user: User):
        return None

    def retrieve_user_permissions(self, user: User):
        return None
    