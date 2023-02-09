import sys
import os
from PySide2.QtWidgets import QApplication
from Dialogs.login_dialog import LoginDialog

                                                     

if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../ExpenseTracker/ExpenseTracker'))
    print(sys.path)

    app = QApplication(sys.argv)

    login_dialog = LoginDialog()
    login_dialog.get_widget().show()

    sys.exit(app.exec_())