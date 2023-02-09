import sys
from PySide2.QtWidgets import QApplication, QPushButton, QTableWidget
from PySide2.QtCore import QObject
from Dialogs.ui_loader import UILoader
from Dialogs import util
from APIClient import _client

class Expenses(QObject):

    def __init__(self):
        self.widget = UILoader(util.UI_userManager).loadUiWidget()    

        remove_btn = self.widget.findChild(QPushButton, "remove_button")
        remove_btn.clicked.connect(self.remove_clicked)

        users_tbl =  self.widget.findChild(QTableWidget, "users_table")

    def get_widget(self):
        return self.widget

    def remove_clicked(self):
        print("Remove clicked")