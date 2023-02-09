

import os

#UI_FILES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Dialogs')
UI_FILES_DIR = os.path.dirname(os.path.realpath(__file__))

UI_Login = os.path.join(UI_FILES_DIR, 'LoginDialog.ui')
UI_UserManager = os.path.join(UI_FILES_DIR, 'UserManager.ui')
UI_Expenses = os.path.join(UI_FILES_DIR, 'Expenses.ui')
UI_Admin = os.path.join(UI_FILES_DIR, 'Admin.ui')

os.path.realpath(__file__)