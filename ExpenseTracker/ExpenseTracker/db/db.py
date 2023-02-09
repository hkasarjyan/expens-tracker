
from ExpenseTracker.models.User import User
from ExpenseTracker.models.Expense import Expense
from ExpenseTracker.models.Permissions import Permissions
from ExpenseTracker import app
import mysql.connector
from ExpenseTracker.util import generate_insert_query, generate_update_query, generate_select_expenses_query

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
        #retrieve before insert
        query, values_map = generate_insert_query(user, 'users')
        cursor.execute(query, values_map)        
        if cursor.rowcount > 0 :
            user.id = cursor.lastrowid
        
        connection.commit()
        connection.close()
        return user

    def retrieve_user(self, user: User):
        connection = self.create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""SELECT id, firstName, lastName, email, password, role 
                          FROM users
                          WHERE email=%(email)s""", {'email':user.email})
        rows = cursor.fetchall()
        if len(rows) == 1:
            user = User.from_dict(rows[0])
            return user
        return None
    def retrieve_user_with_id(self, user: User):
        connection = self.create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""SELECT id, firstName, lastName, email, password, role 
                          FROM users
                          WHERE id=%(id)s""", {'id':user.id})
        rows = cursor.fetchall()
        if len(rows) == 1:
            user = User.from_dict(rows[0])
            return user
        return None
    def retrieve_users(self):        
        connection = self.create_connection()
        cursor = connection.cursor(dictionary=True)
        #Add pagination
        cursor.execute("""SELECT * FROM users""")
        users=[]
        for row in cursor:
            users.append(User.from_dict(row))            
        connection.close()
        return users


    def update_user(self, user: User):
        connection = self.create_connection()
        cursor = connection.cursor()
        #retrieve before insert
        query, values_map = generate_update_query(user, 'users')
        cursor.execute(query, values_map)
        res = None
        if cursor.rowcount > 0 :
            res  = True
        connection.commit()
        connection.close()
        return res


    def delete_user(self, user: User):        
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM users WHERE id=%(id)s""", {'id': user.id})
        result = None
        if cursor.rowcount > 0 :
            result = True
        connection.commit()
        connection.close()
        return result

    def create_expense(self, expense: Expense):
        connection = self.create_connection()
        cursor = connection.cursor()
        #retrieve before insert
        query, values_map = generate_insert_query(expense, 'expenses')
        cursor.execute(query, values_map)        
        if cursor.rowcount > 0 :
            expense.id = cursor.lastrowid
        connection.commit()
        connection.close()
        return expense
    

    def retrieve_expense(self, expense: Expense):
        connection = self.create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""SELECT * 
                          FROM expenses
                          WHERE id=%(id)s""", {'id':expense.id})
        rows = cursor.fetchall()
        if len(rows) == 1:
            expense = Expense.from_dict(rows[0])
            return expense
        return None
    def retrieve_expenses(self, filters):        
        connection = self.create_connection()
        cursor = connection.cursor(dictionary=True)
        query, values = generate_select_expenses_query(filters)
        #Add pagination
        cursor.execute("""SELECT * FROM expenses""")
        expenses=[]
        for row in cursor:
            expenses.append(Expense.from_dict(row))            
        connection.close()
        return expenses

    def update_expense(self, expense: Expense):
        connection = self.create_connection()
        cursor = connection.cursor()
        #retrieve before insert
        query, values_map = generate_update_query(expense, 'expenses')
        cursor.execute(query, values_map)
        res = None
        if cursor.rowcount > 0 :
            res  = True
        connection.commit()
        connection.close()
        return res

    def delete_expense(self, expense: Expense):        
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute("""DELETE FROM expenses WHERE id=%(id)s""", {'id': expense.id})
        result = None
        if cursor.rowcount > 0 :
            result = True
        connection.commit()
        connection.close()
        return result
    #Custom methods should be checked
    def retrieve_user_expenses(self, user: User, filters):
        connection = self.create_connection()
        cursor = connection.cursor(dictionary=True)
        query, values = generate_select_expenses_query(filters)

        #Add pagination
        cursor.execute(query, values)
        expenses=[]
        for row in cursor:
            expenses.append(Expense.from_dict(row))            
        connection.close()
        return expenses

    def retrieve_user_permissions(self, user: User):
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute("""SELECT permissions.name 
                          FROM roles JOIN role_permissions ON roles.id = role_permissions.role_id JOIN permissions ON role_permissions.permission_id = permissions.id
                          WHERE roles.id=%(role_id)s""", {'role_id': user.role})
        permission_list=[]
        for row in cursor:
            permission_list.append(row[0])

        permissions = Permissions(permission_list)
        return permissions



    