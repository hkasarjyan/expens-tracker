import sys
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QLabel
from PySide2.QtCore import QObject
from Dialogs.ui_loader import UILoader
from Dialogs import util
from APIClient import _client
from PySide2.QtCore import QObject, QMetaObject
from PySide2.QtWidgets import QMessageBox
from ExpenseTracker.models.User import User
from APIClient.client import ResponseData
import json

class LoginDialog(QObject):

    def __init__(self):
        self.widget = UILoader(util.UI_Login).loadUiWidget()    
        signin_btn = self.widget.findChild(QPushButton, "signin_button")
        signin_btn.clicked.connect(self.login_clicked)

        self.signin_logIn    = self.widget.findChild(QLineEdit, "signin_logIn")
        self.signin_password = self.widget.findChild(QLineEdit, "signin_password")

        signup_btn = self.widget.findChild(QPushButton, "signup_button")
        signup_btn.clicked.connect(self.signup_clicked)

        self.signup_email    = self.widget.findChild(QLineEdit, "signup_email")
        self.signup_first_name    = self.widget.findChild(QLineEdit, "signup_first_name")
        self.signup_last_name     = self.widget.findChild(QLineEdit, "signup_last_name")
        self.signup_password = self.widget.findChild(QLineEdit, "signup_password")
        
        # Info for successfull signup
        signup_info = self.widget.findChild(QLabel, "signup_info")

    def get_widget(self):
        return self.widget
    
    def login_clicked(self):
        user  = User()
        user.email = self.signin_logIn.text()
        user.password = self.signin_password.text()
        responseData = _client.login(user)
        if not responseData.status:
            QMessageBox.critical(self.widget, "adasdasd",responseData.json["msg"], QMessageBox.Ok)

    def signup_clicked(self):
        user  = User()
        user.email = self.signup_email.text()
        user.password = self.signup_password.text()
        user.first_name = self.signup_first_name.text()
        user.last_name = self.signup_last_name.text()
        user.role = 1
        responseData = _client.signup(user)
        if not responseData.status:
            QMessageBox.critical("adasdasd",responseData.json["msg"])

