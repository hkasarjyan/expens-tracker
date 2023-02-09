import sys
from PySide2.QtWidgets import QApplication, QPushButton, QTableWidget
from PySide2.QtCore import QObject
from Dialogs.ui_loader import UILoader
from Dialogs import util
from APIClient import _client

class Expenses(QObject):

    def __init__(self):
        self.widget = UILoader(util.UI_Admin).loadUiWidget()    

        remove_btn = self.widget.findChild(QPushButton, "remove_button")
        remove_btn.clicked.connect(self.remove_clicked)

        view_expenses_btn = self.widget.findChild(QPushButton, "view_expenses_button")
        view_expenses_btn.clicked.connect(self.view_expenses_clicked)

        users_tbl =  self.widget.findChild(QTableWidget, "users_table")

    def get_widget(self):
        return self.widget
    
    def remove_clicked(self):
        print("Add clicked")

    def view_expenses_clicked(self):
        print("Show expenses for current user")
