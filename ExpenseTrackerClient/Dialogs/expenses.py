import sys
from PySide2.QtWidgets import QApplication, QPushButton, QTableWidget
from PySide2.QtCore import QObject
from Dialogs.ui_loader import UILoader
from Dialogs import util
from APIClient import _client

class Expenses(QObject):

    def __init__(self):
        self.widget = UILoader(util.UI_Expenses).loadUiWidget()    
        
        add_btn = self.widget.findChild(QPushButton, "add_button")
        add_btn.clicked.connect(self.add_clicked)

        remove_btn = self.widget.findChild(QPushButton, "remove_button")
        remove_btn.clicked.connect(self.remove_clicked)

        create_report_btn = self.widget.findChild(QPushButton, "create_report_button")
        create_report_btn.clicked.connect(self.create_report_clicked)

        expenses_tbl =  self.widget.findChild(QTableWidget, "expenses_table")

    def get_widget(self):
        return self.widget
    
    def add_clicked(self):
        print("Add clicked")

    def remove_clicked(self):
        print("Remove clicked")

    def create_report_clicked(self):
        print("Create report clicked")