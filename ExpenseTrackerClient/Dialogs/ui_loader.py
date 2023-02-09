from PySide2 import QtCore, QtUiTools

class UILoader():
    def __init__(self, uifilename):
        self.uifilename = uifilename

    def loadUiWidget(self):
        loader = QtUiTools.QUiLoader()
        uifile = QtCore.QFile(self.uifilename)
        uifile.open(QtCore.QFile.ReadOnly)
        ui = loader.load(uifile)
        uifile.close()
        return ui